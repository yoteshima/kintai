console.log("init ajax.js")
// 送信に必要なやつ
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function postTime(method,time,callback,arg){
    // タイムスタンプを送信
    $.ajax({
        type: 'POST',
        url: "exec/",
        // dataType: "json",
        dataType: "text",
        data: {
            "type":"time_stamp",
            "method":method,
            "time":time
        }

    }).done(function(data) {
        if(callback){
            callback(arg)
        };

    }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
        console.log(XMLHttpRequest.status);
        console.log(textStatus);
        console.log(errorThrown);
    })
}

function postRecord(method,time,callback,arg){
    // 勤務表の変更内容を送信
    $.ajax({
        type: 'POST',
        url: "exec/",
        // dataType: "json",
        dataType: "text",
        data: {
            "type":"work_record",
            "method":method,
            "time":time
        }

    }).done(function(data) {
        if(callback){
            callback(arg)
        };

    }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
        console.log(XMLHttpRequest.status);
        console.log(textStatus);
        console.log(errorThrown);
    })
}

function changeWorkReport(
    {
        target=null,
        year=null,
        month=null,
        project_name=null,
        site_work_time=null,
        date=null,
        start_time=null,
        end_time=null,
        break1_time=null,
        break2_time=null,
        status_code=null,
        remarks=null,
    },
    scrtop
){
    // 勤務表の変更内容を送信
    $.ajax({
        type: 'POST',
        url: "exec/",
        dataType: "text",
        data: {
            "type":"change_work_report",
            "target":target,
            "year":year,
            "month":month,
            "project_name":project_name,
            "site_work_time":site_work_time,
            "date":date,
            "start_time":start_time,
            "end_time":end_time,
            "break1_time":break1_time,
            "break2_time":break2_time,
            "status_code":status_code,
            "remarks":remarks,
        }

    }).done(function(data) {
        console.log("success change_work_report")
        window.location.href = window.location.origin + "/work_report/" + "?year=" + year + "&month=" + month + "&scroll=" + scrtop

    }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
        console.log(XMLHttpRequest.status);
        console.log(textStatus);
        console.log(errorThrown);
    })
}

function changeReportSettings(
    {
        start_time=null,
        end_time=null,
        break1_time=null,
        break2_time=null,
        holidays=null,
        project_name=null,
    }
){
    // 勤務表の変更内容を送信
    $.ajax({
        type: 'POST',
        url: "exec/",
        dataType: "text",
        data: {
            "type":"change_report_settings",
            "start_time":start_time,
            "end_time":end_time,
            "break1_time":break1_time,
            "break2_time":break2_time,
            "holidays":holidays,
            "project_name":project_name,
        }

    }).done(function(data) {
        console.log("success change_report_settings");
        $('#apply-settings1').modal('show');
        setTimeout(function(){
            window.location.href = window.location.origin + "/settings/";
        },1300)

    }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
        console.log(XMLHttpRequest.status);
        console.log(textStatus);
        console.log(errorThrown);
    })
}

