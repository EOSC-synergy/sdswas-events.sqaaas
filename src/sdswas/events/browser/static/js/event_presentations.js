var EventPresentations = {

    init: function(){
        var url = $(".modwin-cards").attr("data-url");
        $(".modwin-cards").load(url, function(responseTxt, statusTxt, xhr) {
            if (statusTxt = "success") {
                $(document).ready(function() {
                    EventPresentations.cards.init();
                });
            } else $(this).text("Error: The contents are not available now. Please contact us.");
        })
    },

    cards: {
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
                var maxlength = EventPresentations.cards.titleLenght;
                $(this).text(Utils.textTrimmer(text, maxlength));
                if(text.length > maxlength) $(this).attr("title", text);

            });
        },
    },
}
