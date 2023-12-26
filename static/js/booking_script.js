$(window).on("load", function () {

    // Slick slider for service page
    $(".slider").slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: false,
        dots: true,
        responsive: [{
            breakpoint: 768,
            settings: { slidesToShow: 1 }
        }]
    });

    // Slick slider for reviews
    $(".slider2").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        dots: true,
        arrows: false
    });

    // Timeout function so alert messages are removed automatically
    setTimeout(function () {
        let messages = document.getElementById('msg');
        if (messages) {
            let alert = new bootstrap.Alert(messages);
            alert.close();
        }
    }, 2500);

    // Initialize the checkbox handler when the modal is shown
    $('#bookingModal').on('shown.bs.modal', function () {
        initOneDayCheckboxHandler();
    });

    function initOneDayCheckboxHandler() {
        var checkbox = document.getElementById("id_just_one_day");
        var startDateInput = document.getElementById("id_start_date");
        var endDateInput = document.getElementById("id_end_date");

        // Function to update the end date based on checkbox and start date
        function updateEndDate() {
            if (checkbox.checked && startDateInput.value) {
                endDateInput.value = startDateInput.value;
                endDateInput.readOnly = true;
            } else {
                endDateInput.readOnly = false;
            }
        }

        if (checkbox && startDateInput && endDateInput) {
            // Attach change event to checkbox and start date input
            checkbox.onchange = updateEndDate;
            startDateInput.onchange = updateEndDate;

            // Initialize with current state
            updateEndDate();
        }
    }
});
