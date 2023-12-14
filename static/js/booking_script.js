document.addEventListener("DOMContentLoaded", function () {
    const startDateField = document.getElementById('id_start_date');
    const endDateField = document.getElementById('id_end_date');

    function updateTimeSlots() {
        const startDate = startDateField.value;
        const endDate = endDateField.value;
        if (startDate && endDate) {
            fetch(`/get-time-slots/?start_date=${startDate}&end_date=${endDate}`)
                .then(response => response.json())
                .then(data => {
                    const timeSlotField = document.getElementById('id_time_slot');
                    timeSlotField.innerHTML = ''; // Clear existing options
                    data.slots.forEach(slot => {
                        const option = document.createElement('option');
                        option.value = slot.id;
                        option.textContent = slot.display;
                        if (slot.full) {
                            option.disabled = true; // Disable the option if the slot is full
                        }
                        timeSlotField.appendChild(option);
                    });
                });
        }
    }

    startDateField.addEventListener('change', updateTimeSlots);
    endDateField.addEventListener('change', updateTimeSlots);
});

$(window).on("load", function () {
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

    $(".slider2").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        dots: true,
        arrows: false
    });

    setTimeout(function () {
        let messages = document.getElementById('msg');
        if (messages) {
            let alert = new bootstrap.Alert(messages);
            alert.close();
        }
    }, 2500);
});
