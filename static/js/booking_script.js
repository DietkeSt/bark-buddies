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

    // Function to handle the checkbox change
    function handleOneDayCheckbox(checkbox) {
        var endDateInput = document.getElementById("id_end_date");
        if (checkbox.checked) {
            endDateInput.disabled = true;
        } else {
            endDateInput.disabled = false;
        }
    }

    // Initialize the checkbox handler when the modal is shown
    $('#bookingModal').on('shown.bs.modal', function () {
        initOneDayCheckboxHandler();
    });

    // Setup the checkbox handler
    function initOneDayCheckboxHandler() {
        var checkbox = document.getElementById("id_just_one_day");
        if (checkbox) {
            checkbox.onchange = function () {
                handleOneDayCheckbox(this);
            };
            // Run once to set initial state
            handleOneDayCheckbox(checkbox);
        }
    }
});