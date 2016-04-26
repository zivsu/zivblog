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

    $("#get-validate-code").click(function(){
        getValidateCode();
    });
    getValidateCode();

    $("#comment-add").click(function(){
        content = $("#comment-content").val();
        username = $("#comment-username").val();
        code = $("#code").val();
        console.log(code);

        if (content == ""){
            alertErr($("#comment-alert"), "评论不能为空");
        } else if (username == ""){
            alertErr($("#comment-alert"), "用户名不能为空");
        } else if (code == ""){
            alertErr($("#comment-alert"), "验证码不能为空");
        } else {
            url = "/add/comment";
            xsrf = getCookie("_xsrf");
            slug = document.getElementById("comment-add").getAttribute("data-slug")
            $.ajax({
                type: "POST",
                url: url,
                data:{"username":username, "content":content, "_xsrf":xsrf, "slug":slug, "code":code},
                success: function(resp){
                    if (resp.err) {
                        alertErr($("#comment-alert"), resp.msg);
                    } else{
                        $(".no-comment").hide();
                        commentNum += 1;
                        $("#comment-num").text(commentNum);
                        comment = resp.comment;

                        node = "<div class='comment'>" +
                                "<div class='avatar'>" +
                                    "<img src=" + comment.headimgurl + " alt='avatar'>" +
                                "</div>" +
                                "<div class='main'>" +
                                    "<p><span>" + comment.username + "</span></p>" +
                                    "<div class='content'>" + comment.content + "</div>" +
                                    "<div class='other'>" + comment.datetime + "</div>" +
                                "</div>" +
                            "</div>";
                        $(".comment-section-header").after(node);
                        $("#comment-content").val("");
                        $("#comment-username").val("");
                        $("#code").val("");
                        // reset validate code
                        getValidateCode();
                    }
                },
                error:function(resp){
                    alertErr($("#comment-alert"), "系统错误，请稍后再试");
                }
            });
        }
    });


    function alertErr(alert, msg) {
       alert.text(msg);
       alert.show();
       setTimeout(function(){
           alert.hide();
       },6000);
    };

    function getCookie(name) {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    };

    function getValidateCode() {
        console.log("get validate code");
        $.ajax({
            "type":"GET",
            "url":"/validae_code",
            success: function(data){
                $("#validate-code").attr('src', "data:image/png;base64,"+data);
            }
        });
    };
});

