(function() {
    'use strict';

    var requirejsOptions = {
        baseUrl: '++theme++sdswas/',
        optimize: 'none',
        paths: {
            'main': '++theme++sdswas/js/main',
            'event_presentations': '++resource++sdswas.events/js/event_presentations.js',
        }
    };

    if (typeof exports !== 'undefined' && typeof module !== 'undefined') {
        module.exports = requirejsOptions;
    }
    if (typeof requirejs !== 'undefined' && requirejs.config) {
        requirejs.config(requirejsOptions);
    }

    requirejs([
        'main',
    ], function($, _bootstrap) {
        (function($) {
            var Events = {
                init: function() {
                    App.con("----> Events init");
                    this.upcoCards.init();
                    this.pastevCards.init();
                },

                populateModal: function(trigger) {

                    ModalWindow.init();

                    /*Set available information (title and go back link)*/
                    ModalWindow.gobackLink.text($(trigger).attr("data-gobacklink"));
                    ModalWindow.title.text($(trigger).attr("data-title"));

                    var url = $(trigger).attr("data-url");
                    /**Fetch the rest of the information: contents of the body */
                    $(".modwin-main-content").load(url, function(responseTxt, statusTxt, xhr) {
                        if (statusTxt = "success") {
                            Events.openModal();
                            $(document).ready(function() {
                                EventPresentations.init();
                            });
                        }
                    });
                },

                openModal: function() {

                    App.mainContent.addClass("freeze-main-content");
                    Sidenav.repos();

                    ModalWindow.el.addClass("show");
                    ModalWindow.el.removeClass("hide");
                    ModalWindow.isOpen = true;
                },

                upcoCards: {
                    selectors: $(".events-upco-card"),
                    triggers: $(".js-card-trigger"),
                    titles: $(".events-upco-card-title :first-child"),
                    titleLenght: 75,

                    init: function() {
                        this.trimTextsLength();
                        this.addListeners();
                    },

                    trimTextsLength: function() {
                        // Trim titles
                        this.titles.each(function() {
                            var text = $(this).text();
                            var maxlength = Events.upcoCards.titleLenght;
                            $(this).text(Utils.textTrimmer(text, maxlength));
                            if(text.length > maxlength) $(this).attr("title", text);
                        });
                    },
                    addListeners: function() {
                        App.con("----)))) Upcoming events >> Cards are listening");
                        this.selectors.each(function() {

                            $(this).on("click", ".js-card-trigger", function(event) {
                                event.preventDefault();
                                //this is the current trigger but we use the parent who set the event because it has the data to be used by its children
                                Events.populateModal(event.delegateTarget);
                            });
                        });
                    },
                },

                pastevCards: {
                    selectors: $(".pastev-card"),
                    triggers: $(".js-card-trigger"),
                    titles: $(".pastev-card-title :first-child"),
                    titleLenght: 70,

                    init: function() {
                        this.trimTextsLength();
                        this.addListeners();
                    },

                    trimTextsLength: function() {
                        // Trim titles
                        this.titles.each(function() {
                            var text = $(this).text();
                            var maxlength = Events.pastevCards.titleLenght;
                            $(this).text(Utils.textTrimmer(text, maxlength));
                            if(text.length > maxlength) $(this).attr("title", text);
                        });
                    },
                    addListeners: function() {
                        App.con("----)))) Past events >> Cards are listening");
                        this.selectors.each(function() {

                            $(this).on("click", ".js-card-trigger", function(event) {
                                event.preventDefault();
                                //this is the current trigger but we use the parent who set the event because it has the data to be used by its children
                                Events.populateModal(event.delegateTarget);
                            });
                        });
                    },
                }
            }


            $(document).ready(function() {
                Events.init();
            });
        })(jQuery);
    });
}());