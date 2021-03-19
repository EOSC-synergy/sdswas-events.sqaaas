(function() {
    'use strict';

    var requirejsOptions = {
        baseUrl: '++theme++sdswas/',
        optimize: 'none',
        paths: {
            'main': 'js/main',
        }
    };

    if (typeof exports !== 'undefined' && typeof module !== 'undefined') {
        module.exports = requirejsOptions;
    }
    if (typeof requirejs !== 'undefined' && requirejs.config) {
        requirejs.config(requirejsOptions);
    }

    requirejs([
        'main'
    ], function($, _bootstrap) {
        (function($) {
            $(document).ready(function() {

                EventPresentations.init();

                // Images slider
                Slider.init(
                    $("#slider-items"),
                    0,
                    $(".slider-item-wrap").toArray(),
                    $(".slider-indicators-container"),
                    $("#previous-btn"),
                    $("#next-btn")
                );
            });
        })(jQuery);
    });
}());