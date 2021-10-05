(function() {
    'use strict';

    var requirejsOptions = {
        baseUrl: '++theme++sdswas/',
        optimize: 'none',
    }

    if (typeof exports !== 'undefined' && typeof module !== 'undefined') {
        module.exports = requirejsOptions;
    }
    if (typeof requirejs !== 'undefined' && requirejs.config) {
        requirejs.config(requirejsOptions);
    }

    requirejs([
        'main-min',
    ], function($, _bootstrap) {
        (function($) {

            var is_upcoming = $("#view").attr("upcoming");
            if (is_upcoming == undefined) is_upcoming = false;
            var menu_entry = is_upcoming ? ("#news-and-events-btn") : ("#resources-btn");

            Header.highlightMenuButton(menu_entry);

            $(document).ready(function() {
                Event.init();
            });
        })(jQuery);
    });
}());