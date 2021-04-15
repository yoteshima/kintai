$(function(){
    console.log("init clock.js")

    var timestamp_update_flg = true
    $(".timepicker").on("focus",function(){
        timestamp_update_flg = false
    });
    setInterval(function(){
        var now = new Date();
        var week_day = new Array("日","月","火","水","木","金","土");
        var year = now.getFullYear()
        var month = now.getMonth() + 1
        var date = now.getDate()
        var day = now.getDay();
        var hour = now.getHours()
        var minute = now.getMinutes()
        var second = now.getSeconds()

        current_time = year + '年 ' + ('0' + String(month)).substr(-2,2) + '月 ' + ('0' + String(date)).substr(-2,2) + '日(' + week_day[day] + ') ' + ('0' + String(hour)).substr(-2,2) + ':' + ('0' + String(minute)).substr(-2,2) + ':' + ('0' + String(second)).substr(-2,2)

        var round_up = minute + 15 + second/60
        var stamp_hour = ('0' + String(hour)).substr(-2,2)
        var stamp_minute = ''
        if(round_up > 60){
            stamp_minute = '00'
            stamp_hour = ('0' + String(hour + 1)).substr(-2,2)
        }else if(round_up > 45){
            stamp_minute = '45'
        }else if(round_up > 30){
            stamp_minute = '30'
        }else if(round_up > 15){
            stamp_minute = '15'
        }else{
            stamp_minute = '00'
        }
        timestamp = stamp_hour + ' : ' + stamp_minute

        var options = { 
            now: timestamp,
            twentyFour: true,
            title: '',
            minutesInterval: 15,
        };
        $('.timepicker').wickedpicker(options);

        if(timestamp_update_flg){
            $(".timepicker").val(timestamp)
        };
        $(".current-time").text(current_time);

    },1000)
});