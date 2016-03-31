/* ---------- login page  ---------- */

$(document).ready(function(){
    $("#email").focus(function() {

        $(this).parent(".input-prepend").addClass("input-prepend-focus");

    });

    $("#email").focusout(function() {

        $(this).parent(".input-prepend").removeClass("input-prepend-focus");

    });

    $("#password").focus(function() {

        $(this).parent(".input-prepend").addClass("input-prepend-focus");

    });

    $("#password").focusout(function() {

        $(this).parent(".input-prepend").removeClass("input-prepend-focus");

    });

    $("#btn-login").click(function(){
        var email = $("#email").val();
        var password = $("#password").val();
        var remember = $("#remember").prop('checked');

        if (email == ""){
            alertErr($("#login-alert"), "邮箱不能为空");
            return;
        }
        if (password == ""){
            alertErr($("#login-alert"), "密码不能为空");
            return;
        }

        url = "/login";
        xsrf = get_cookie("_xsrf");
        $.ajax({
            type: "POST",
            url: url,
            data:{"email":email, "password":password, "_xsrf":xsrf, "remember":remember},
            success: function(resp){
                if (resp.err) {
                    alertErr($("#login-alert"), resp.msg);
                } else{
                    window.location.href = "/backend/index";
                }
            },
            error:function(resp){
                alertErr($("#login-alert"), "系统错误，请稍后再试");
            }
        });
    });
})

function get_cookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}