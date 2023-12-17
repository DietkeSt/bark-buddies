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
