$(document).ready(function() {
    $(".back-to-top").click( function(){
        scroll(0, 0);
    });

    $(".show-sibebar").click(function(){
        var hideSibar = $('.sibebar-container').hasClass("hide");
        if (hideSibar) {
            $('.sibebar-container').removeClass("hide");
            $('.preview-container').removeClass("center");
            $('.show-sibebar').removeClass("icon-circle-arrow-left").addClass("icon-circle-arrow-right");
        } else {
            $('.sibebar-container').addClass("hide");
            $('.preview-container').addClass("center");
            $('.show-sibebar').removeClass("icon-circle-arrow-right").addClass("icon-circle-arrow-left");
        }
    });
});