$(document).ready(function(){
    $("#save-profile").click(function(){
        saveProfile();
    });

    $("#reset-profile").click(function(){
        resetProfile();
    });

    $("#publish-article").click(function(){
        sendArticle("1");
    });
    $("#save-article").click(function(){
        sendArticle("0");
    });
})

function handleAjaxErr(msg){
    alertErr($(".alert"), msg);
}

function sendAjaxRequest(url, data, type, callback) {
    $.ajax({
        type: type,
        url: url,
        data:data,
        success: function(resp){
            callback(resp)
        },
        error:function(resp){
            handleAjaxErr("系统错误，请稍后再试");
        }
    });
}


/* ----------- profile page ----------- */
function saveProfile(){
    var name = $("#profile-name").val();
    var enName = $("#profile-en-name").val();
    var email = $("#profile-email").val();
    var wechat = $("#profile-wechat").val();
    var github = $("#profile-github").val();
    var address = $("#profile-address").val();
    var descript = $("#profile-descript").val();

    xsrf = get_cookie("_xsrf");
    data = {
        "name":name,
        "en_name":enName,
        "email":email,
        "wechat":wechat,
        "github":github,
        "address":address,
        "descript":descript,
        "_xsrf":xsrf
    }

    url = "/backend/profile"
    type = "POST"
    sendAjaxRequest(url, data, type, handleProfileAjaxRespson)
}

function resetProfile(){
    $("#profile-name").val(name);
    $("#profile-en-name").val(enName);
    $("#profile-email").val(email);
    $("#profile-wechat").val(wechat);
    $("#profile-github").val(github);
    $("#profile-address").val(address);
    $("#profile-descript").val(descript);
}

function handleProfileAjaxRespson(resp){
    alertErr($("#profile-alert"), resp.msg);
}

/* -------- article edit page -------- */
function sendArticle(status){
    title = $("#article-title").val();
    tag = $('input:radio[name=article-tag]:checked').val();
    date = $("#article-date").val();
    slug = $("#article-slug").val();
    abstracts = $("#article-abstracts").val();
    content = $("#article-content").val();

    xsrf = get_cookie("_xsrf");
    data = {
        "id":article_id,
        "title":title,
        "tag":tag,
        "slug":slug,
        "abstracts":abstracts,
        "content":content,
        "status":status,
        "_xsrf":xsrf,
    }
    console.log(data);
    url = "/backend/article_edit";
    type = "POST";
    sendAjaxRequest(url, data, type, handleArticleAjaxRespson)
}

function handleArticleAjaxRespson(resp){
    alertErr($("#article-alert"), resp.msg);
}

/* -------- article list page -------- */
