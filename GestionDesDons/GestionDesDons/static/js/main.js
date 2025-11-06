(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 45) {
                $('.fixed-top').addClass('bg-dark shadow');
            } else {
                $('.fixed-top').removeClass('bg-dark shadow');
            }
        } else {
            if ($(this).scrollTop() > 45) {
                $('.fixed-top').addClass('bg-dark shadow').css('top', -45);
            } else {
                $('.fixed-top').removeClass('bg-dark shadow').css('top', 0);
            }
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Causes progress
    $('.causes-progress').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: false,
        smartSpeed: 1000,
        center: true,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            }
        }
    });

    
})(jQuery);

// Set active navbar link based on current page filename
(function () {
    try {
        var path = window.location.pathname.split('/').pop();
        if (!path) path = 'index.html';

        // Clear existing active classes on nav-link and dropdown-item
        var navLinks = document.querySelectorAll('.navbar-nav a.nav-link');
        navLinks.forEach(function (a) { a.classList.remove('active'); });
        var dropItems = document.querySelectorAll('.navbar-nav .dropdown-item');
        dropItems.forEach(function (d) { d.classList.remove('active'); });

        // First try exact matches on nav-link
        var matched = false;
        document.querySelectorAll('.navbar-nav a.nav-link').forEach(function (a) {
            var href = a.getAttribute('href') || '';
            var hrefFile = href.split('/').pop().split('?')[0].split('#')[0];
            if (hrefFile === path) {
                a.classList.add('active');
                matched = true;
            }
        });

        // Then check dropdown items
        if (!matched) {
            document.querySelectorAll('.navbar-nav .dropdown-item').forEach(function (d) {
                var href = d.getAttribute('href') || '';
                var hrefFile = href.split('/').pop().split('?')[0].split('#')[0];
                if (hrefFile === path) {
                    d.classList.add('active');
                    // mark the parent dropdown toggle as active (the .nav-link.dropdown-toggle)
                    var parent = d.closest('.dropdown-menu');
                    if (parent) {
                        var toggle = parent.previousElementSibling; // should be the <a class="nav-link dropdown-toggle">
                        if (toggle && toggle.classList.contains('nav-link')) toggle.classList.add('active');
                    }
                    matched = true;
                }
            });
        }

        // Fallback: if still not matched, try partial match by filename substring
        if (!matched) {
            var p = path.replace('.html','');
            document.querySelectorAll('.navbar-nav a.nav-link, .navbar-nav .dropdown-item').forEach(function (a) {
                var href = a.getAttribute('href') || '';
                if (href.indexOf(p) !== -1 && p.length>0) {
                    a.classList.add('active');
                    // if it's a dropdown-item, mark its toggle too
                    if (a.classList.contains('dropdown-item')) {
                        var parent = a.closest('.dropdown-menu');
                        if (parent) {
                            var toggle = parent.previousElementSibling;
                            if (toggle && toggle.classList.contains('nav-link')) toggle.classList.add('active');
                        }
                    }
                }
            });
        }
    } catch (e) {
        console.warn('nav-active script error', e);
    }
})();

