$(function(){
    console.log("init report_settings.js")

    $(".apply-settings").on("click", function(){
        let start_time = $(".start-time").val()
        let end_time = $(".end-time").val()
        let break1_time = $(".break1-time").val()
        let break2_time = $(".break2-time").val()
        let project_name = $(".project-name").val()

        let cbox = $(".weekday")
        let holidays = 0
        for(let i=0; i<cbox.length; i++){
            if(cbox[i].checked){
                holidays += 2**cbox[i].value
            }
        }

        data = {
            "start_time":start_time,
            "end_time":end_time,
            "break1_time":break1_time,
            "break2_time":break2_time,
            "holidays":holidays,
            "project_name":project_name,
        }
        changeReportSettings(data)
    });

})