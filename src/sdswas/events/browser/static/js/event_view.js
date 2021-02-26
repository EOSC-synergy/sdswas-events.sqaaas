(function() {
    'use strict';

    var requirejsOptions = {
        baseUrl: '++theme++sdswas/',
        optimize: 'none',
        paths: {
            'main': '++theme++sdswas/js/main',
            'event_presentations': '++resource++sdswas.events/js/event_presentations',
        }
    };

    if (typeof exports !== 'undefined' && typeof module !== 'undefined') {
        module.exports = requirejsOptions;
    }
    if (typeof requirejs !== 'undefined' && requirejs.config) {
        requirejs.config(requirejsOptions);
    }

    requirejs([
        'main','event_presentations'
    ], function($, _bootstrap) {
        (function($) {
            $(document).ready(function() {
                EventPresentations.init();

                // Modal window slider
                Slider.init(
                    $("#slider-items"),
                    $("#mobile-swipe-area"),
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