/*jshint esversion: 6 */

// Initialize functions
$(document).ready(function () {
    // Calculate total price on date change
    $('#id_start_date, #id_end_date').change(updateTotalPrice);
    
    // Initialize functions
    updateTotalPrice();

    initOneDayCheckboxHandler();

    initDateChangeHandlers();

    checkUnavailableTimes();

    initCommentsToggle();

    setMinimumDateForBooking();

    handleNavbarScroll();

});

// Initialize the comments toggle functionality
function initCommentsToggle() {
    var toggleCommentButton = document.getElementById('toggleCommentCard');
    if (toggleCommentButton) {
        toggleCommentButton.addEventListener('click', function () {
            var commentCard = document.querySelector('.comment-card');
            commentCard.style.display = commentCard.style.display === "none" ? "block" : "none";
        });
    }
}

// Set minimum date for the start and end date inputs
function setMinimumDateForBooking() {
    var today = new Date();
    var tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 2);

    var minDate = tomorrow.toISOString().split('T')[0];

    $('#id_start_date').attr('min', minDate);
    $('#id_end_date').attr('min', minDate);
}

// Initialize the date change handlers
function initDateChangeHandlers() {
    $('#id_start_date, #id_end_date').change(checkUnavailableTimes);
}

// Check and update unavailable times
function checkUnavailableTimes() {
    const startDate = $('#id_start_date').val();
    const endDate = $('#id_end_date').val();

    if (startDate && endDate) {
        fetch(`/booking/get-unavailable-times/?start_date=${startDate}&end_date=${endDate}`)
            .then(response => response.json())
            .then(data => {
                const unavailableTimes = data.unavailable_times;
                updateAvailableTimes(document.getElementById('id_time'), unavailableTimes);
            });
    }
}

// Update the available times in the dropdown
function updateAvailableTimes(select, unavailableTimes) {
    const options = select.options;
    let currentValue = select.value;

    if (currentValue.length === 8) {
        currentValue = currentValue.substr(0, 5);
    }

    let isCurrentValueAvailable = true;

    for (let i = 0; i < options.length; i++) {
        const optionValue = options[i].value.substr(0, 5);
        const isUnavailable = unavailableTimes.includes(optionValue);
        options[i].disabled = isUnavailable;

        if (optionValue === currentValue && isUnavailable) {
            isCurrentValueAvailable = false;
        }
    }

    if (!isCurrentValueAvailable) {
        select.value = '';
    }
}

// Initialize the one-day checkbox handler
function initOneDayCheckboxHandler() {
    var checkbox = document.getElementById("id_just_one_day");
    var startDateInput = document.getElementById("id_start_date");
    var endDateInput = document.getElementById("id_end_date");

    function updateEndDate() {
        if (checkbox.checked && startDateInput.value) {
            endDateInput.value = startDateInput.value;
            endDateInput.readOnly = true;
            checkUnavailableTimes(); // Check for unavailable times
        } else {
            endDateInput.readOnly = false;
        }
    }

    if (checkbox && startDateInput && endDateInput) {
        checkbox.onchange = updateEndDate;
        startDateInput.onchange = updateEndDate;
        updateEndDate();
    }
}

// Function to update total price;
function updateTotalPrice() {
    const startDateInput = $('#id_start_date');
    const endDateInput = $('#id_end_date');
    const originalPriceElement = $('#originalPrice');
    const priceTextElement = $('#priceText');
    const addSecondDogCheckbox = $('#id_add_second_dog');

    if (startDateInput.val() && endDateInput.val() && originalPriceElement.length > 0) {
        const startDate = new Date(startDateInput.val());
        const endDate = new Date(endDateInput.val());
        const originalPrice = parseFloat(originalPriceElement.data('price'));
        let additionalPrice = 0;

        // Check for second dog
        if (addSecondDogCheckbox.is(':checked')) {
            additionalPrice = originalPrice * 0.5;
        }

        // Calculate the number of days
        const dayDifference = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1; // +1 to include start day

        // Calculate total price
        let totalPrice = (originalPrice + additionalPrice) * dayDifference;
        priceTextElement.text(`EUR ${totalPrice.toFixed(2)}`);
    }
}

// Function to handle navbar style on scroll
function handleNavbarScroll() {
    var navbar = document.getElementById("navbar");
    navbar.classList.add("transparent");
    window.onscroll = function () {
        if (window.pageYOffset > 0) {
            navbar.classList.remove("transparent");
            navbar.classList.add("sticky");
        } else {
            navbar.classList.remove("sticky");
            navbar.classList.add("transparent");
        }
    };
}

// Slick slider initialization and alert message timeout
$(window).on("load", function () {
    $(".slider").slick({
        // Slick slider settings for reviews
        dots: true,
        arrows: false,
        autoplay: true,
        infinite: true,
        autoplaySpeed: 4000,
        slidesToShow: 3,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });

    setTimeout(function () {
        let messages = document.getElementById('msg');
        if (messages) {
            let alert = new bootstrap.Alert(messages);
            alert.close();
        }
    }, 2500);
});
