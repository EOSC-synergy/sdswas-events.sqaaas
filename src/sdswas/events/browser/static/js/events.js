(function() {
    'use strict';

    var requirejsOptions = {
        baseUrl: '++theme++sdswas/',
        optimize: 'none',
        paths: {
            'main': 'js/main'
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
                            $(this).text(Utils.textTrimmer(text, Events.upcoCards.titleLenght));
                        });
                    },
                    addListeners: function() {
                        App.con("----)))) Upcoming events >> Cards are listening");
                        this.selectors.each(function() {

                            $(this).on("click", ".js-card-trigger", function(event) {
                                event.preventDefault();
                                //this is the current trigger but we use the parent who set the event because it has the data to be used by its children
                                ModalWindow.populateModal(event.delegateTarget);
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
                            $(this).text(Utils.textTrimmer(text, Events.pastevCards.titleLenght));
                        });
                    },
                    addListeners: function() {
                        App.con("----)))) Past events >> Cards are listening");
                        this.selectors.each(function() {

                            $(this).on("click", ".js-card-trigger", function(event) {
                                event.preventDefault();
                                //this is the current trigger but we use the parent who set the event because it has the data to be used by its children
                                Events.pastevCards.populateModal(event.delegateTarget);
                            });
                        });
                    },
                    populateModal: function(trigger) {

                        /*Set available information (title and go back link)*/
                        ModalWindow.gobackLink.text($(trigger).attr("data-gobacklink"));
                        ModalWindow.title.text($(trigger).attr("data-title"));

                        var url = $(trigger).attr("data-url");
                        /**Fetch the rest of the information: contents of the body */
                        $(".modwin-main-content").load(url, function(responseTxt, statusTxt, xhr) {
                            if (statusTxt = "success") {
                                Events.pastevCards.openModal();
                                $(document).ready(function() {
                                    Events.pastevPresentCards.init();
                                });
                            }
                        });
                    },
                    openModal: function() {

                        App.mainContent.addClass("freeze-main-content");
                        ModalWindow.addListeners();
                        Sidenav.repos();

                        ModalWindow.el.addClass("show");
                        ModalWindow.el.removeClass("hide");
                        ModalWindow.isOpen = true;
                    },
                },

                pastevPresentCards: {
                    selectors: $(".pastev-presentation-card"),
                    triggers: $(".js-card-trigger"),
                    titles: $(".pastev-presentation-card-title  :first-child"),
                    titleLenght: 135,

                    init: function() {
                        this.trimTextsLength();
                    },

                    trimTextsLength: function() {
                        // Trim titles
                        $(".pastev-presentation-card .modwin-card-subtitle :first-child").each(function() {
                            var text = $(this).text();
                            $(this).text(Utils.textTrimmer(text, Events.pastevPresentCards.titleLenght));
                        });
                    },
                }
            }

            $(document).ready(function() {
                Events.init();
                App.showPage();
            });
        })(jQuery);
    });
}());