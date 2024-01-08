function assignRandomReviewImages() {
    var imageElements = document.querySelectorAll('#review-images span[data-image]');
    var images = Array.from(imageElements).map(el => el.getAttribute('data-image'));

    var reviewImages = document.querySelectorAll('.animation-card_image img');
    reviewImages.forEach(function (img) {
        var randomImage = images[Math.floor(Math.random() * images.length)];
        img.src = randomImage;
    });
}

$(document).ready(function () {
    // Initialize the booking modal when it's shown
    $('#bookingModal').on('shown.bs.modal', function () {
        $('#bookingForm').trigger("reset");
        initOneDayCheckboxHandler();
        initDateChangeHandlers();
        checkUnavailableTimes(); // Check for unavailable times immediately when modal opens
        initAddSecondDogHandler(); 
    });

    // Initialize functions
    initCommentsToggle();

    setMinimumDateForBooking();

    assignRandomReviewImages();

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
    tomorrow.setDate(tomorrow.getDate() + 1); // Set to one day ahead

    var minDate = tomorrow.toISOString().split('T')[0]; // Format as YYYY-MM-DD

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

// Handler for "Add Second Dog" checkbox
function initAddSecondDogHandler() {
    const addSecondDogCheckbox = document.getElementById('id_add_second_dog');
    const originalPriceElement = document.getElementById('originalPrice');
    const priceText = document.getElementById('priceText');
    const originalPrice = parseFloat(originalPriceElement.dataset.price);
    const additionalPrice = originalPrice * 0.5; // 50% additional price for second dog

    addSecondDogCheckbox.addEventListener('change', (event) => {
        if (event.target.checked) {
            let newPrice = originalPrice + additionalPrice;
            priceText.innerHTML = `${newPrice.toFixed(2)}`;
        } else {
            priceText.innerHTML = `${originalPrice.toFixed(2)}`;
        }
    });
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
