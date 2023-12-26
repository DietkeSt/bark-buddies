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

    // Check for unavailable times and update them
    $('#id_start_date, #id_end_date').change(function () {
        const startDate = document.getElementById('id_start_date').value;
        const endDate = document.getElementById('id_end_date').value;

        if (startDate && endDate) {
            fetch(`/get-unavailable-times/?start_date=${startDate}&end_date=${endDate}`)
                .then(response => response.json())
                .then(data => {
                    const unavailableTimes = data.unavailable_times;
                    updateAvailableTimes(document.getElementById('id_time'), unavailableTimes);
                });
        }
    });

    function updateAvailableTimes(select, unavailableTimes) {
        const options = select.options;
        let currentValue = select.value;

        // Convert the current value to 'HH:MM' format for comparison
        if (currentValue.length === 8) {
            currentValue = currentValue.substr(0, 5);
        }

        // Flag to check if the current value is available
        let isCurrentValueAvailable = true;

        for (let i = 0; i < options.length; i++) {
            // Strip off seconds from the option value (HH:MM:SS to HH:MM)
            const optionValue = options[i].value.substr(0, 5);
            const isUnavailable = unavailableTimes.includes(optionValue);
            options[i].disabled = isUnavailable;

            // Check if the current value is among the unavailable times
            if (optionValue === currentValue && isUnavailable) {
                isCurrentValueAvailable = false;
            }
        }

        // If the current value is unavailable, reset the select
        if (!isCurrentValueAvailable) {
            select.value = ''; // Reset to a neutral or NULL value
        }
    }

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
