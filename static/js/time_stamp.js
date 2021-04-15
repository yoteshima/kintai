$(function(){
    console.log("init time_stamp.js")

    const set_status = function(text){
        $(".stamp-status").text(text);
    }

    $(".entry-work").on("click", function(){
        var time_stamp = $(".timestamp").val();
        postTime("entry-work",time_stamp,set_status,"出勤時刻を打刻しました");
    });
    $(".leave-work").on("click", function(){
        var time_stamp = $(".timestamp").val();
        postTime("leave-work",time_stamp,set_status,"退勤時刻を打刻しました");
    });
    $(".entry-break").on("click", function(){
        var time_stamp = $(".timestamp").val();
        postTime("entry-break",time_stamp,set_status,"休憩入時刻を打刻しました");
    });
    $(".leave-break").on("click", function(){
        var time_stamp = $(".timestamp").val();
        postTime("leave-break",time_stamp,set_status,"休憩戻時刻を打刻しました");
    });


});