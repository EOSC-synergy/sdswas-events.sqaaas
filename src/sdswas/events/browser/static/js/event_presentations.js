var EventPresentations = {

    init: function(){
        this.cardsContainer.init();
    },

    cards: {
        titles: $(".pastev-presentation-card-title  :first-child"),
        titleLenght: 135,

        init: function() {
            this.trimTextsLength();
            this.addListeners();
        },

        trimTextsLength: function() {
            // Trim titles
            $(".pastev-presentation-card .modwin-card-subtitle :first-child").each(function() {
                var text = $(this).text();
                var maxlength = EventPresentations.cards.titleLenght;
                $(this).text(Utils.textTrimmer(text, maxlength));
                if(text.length > maxlength) $(this).attr("title", text);

            });
        },

        addListeners: function() {

            this.attachOpenItemView();

            $(window).on("resize", function() {
                App.winW = $(window).width();
                App.winH = $(window).height();
                Sidenav.repos();
                EventPresentations.cards.attachOpenItemView();
            });
        },

        attachOpenItemView: function(){
            //Attachs to the on click event of children elements with class "js-card-trigger"
            //the function that opens modal window. The click is unattached in screens < 592px

            if (App.winW <= 592) {
                $(".pastev-presentation-card.card-with-embedded-doc .js-card-trigger").each(function () {
                   $(this).css("cursor", "default")
                          .removeAttr("href");
                });

            } else {
                $(".pastev-presentation-card.card-with-embedded-doc .js-card-trigger").each(function () {
                    $(this).attr("href", $(this).attr("data-href"))
                           .css("cursor", "pointer")
                });

            }
        },

    },

    cardsContainer: {
        updateUrl: "",

        init: function() {
            App.con("----> Presentations cards container init");
            this.addListeners();
            this.updateUrl = $(".modwin-cards").attr("data-url");
            this.update();
        },

        addListeners: function() {
            App.con("----)))) Presentations of a Past Event >> Search input is listening");

            $("form#searchPresentations").submit(function(e) {
                e.preventDefault();
                EventPresentations.cardsContainer.update();
            });
        },
        update: function() {

            //App.loader.init();

            var searchinput = $("form#searchPresentations .search-tool-input").val()
            var url = this.updateUrl+"?searchinput="+encodeURIComponent(searchinput)

            $(".modwin-cards").empty().load(url, function(responseTxt, statusTxt, xhr) {
                if (statusTxt == "success") {
                    EventPresentations.cards.init();
                } else {
                    $(this).append("<p>Presentations can not be displayed now. Please <a href='contact-info'> contact us</a>.</p>");
                }
              /*  gsap.to(".page-overlay", {
                        duration: 5,
                        onComplete: function() {
                            App.loader.end();
                        }
                });*/
            })
        },


    }

}
