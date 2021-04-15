$(function(){
    console.log("init work_report.js")

    var current_id = null
    var current_class = null
    var current_data = null

    let queryObject = new Object
    let param_arr = location.search.substring(1).split("&")
    if(param_arr){
        for(let i=0; i<param_arr.length; i++){
            let param = param_arr[i].split('=');
            let paramName = decodeURIComponent(param[0]);
            let paramValue = decodeURIComponent(param[1]);
            queryObject[paramName] = paramValue;
        }
        if(queryObject["scroll"]){　//
            window.scrollTo( 0 , queryObject["scroll"] );
        }
    }


    function check_target(target_id,target_class){
        if(current_id == null && current_class == null){
            current_id = target_id
            current_class = target_class
        }else if(current_id != target_id || current_class != target_class){
            current_id = target_id
            current_class = target_class
            return false
        }else{
            return true
        }
    }

    function check_data(data){
        if(current_data == null){
            current_data = data
        }else if(Object.entries(current_data).toString() !== Object.entries(data).toString()){
            return false
        }else{
            return true
        }
    }

    function get_data(target){
        let year = parseInt($("#year").val())
        let month = parseInt($("#month").val())
        let data = null
        let target_class = null
        if(target.get(0)){
            target_class = target.get(0).className.split(" ")[0]
        }

        if(year && month){

            if(target_class == "year-month"){
                data = {
                    "target":"year_month",
                    "year":year,
                    "month":month
                }

            }else if(target_class == "project-name"){
                let project_name = target.find(".project-name").val()
                data = {
                    "target":"project_name",
                    "year":year,
                    "month":month,
                    "project_name":project_name
                }

            }else if(target_class == "site-work-time"){
                let site_work_time = target.find(".total-time").val()
                data = {
                    "target":"site_work_time",
                    "year":year,
                    "month":month,
                    "site_work_time":site_work_time
                }

            }else if(target_class == "report-detail"){
                let date = target.find(".date").text()
                let start_time = target.find(".start-time").val()
                let end_time = target.find(".end-time").val()
                let break1_time = target.find(".break1-time").val()
                let break2_time = target.find(".break2-time").val()
                let status_code = target.find(".status").prop("selectedIndex")
                let remarks = target.find(".remarks").val()
                data = {
                    "target":"report_detail",
                    "year":year,
                    "month":month,
                    "date":date,
                    "start_time":start_time,
                    "end_time":end_time,
                    "break1_time":break1_time,
                    "break2_time":break2_time,
                    "status_code":status_code,
                    "remarks":remarks,
                }
            }
        }
        return data
    }

    $("input, select").on("focus", function(event){
        // フォーカスしたとき
        if(current_id == null && current_class == null){
            let target = $(event.target).parent().parent()
            current_id = target.get(0).id.split(" ")[0]
            current_class = target.get(0).className.split(" ")[0]
            current_data = get_data(target)
        }

    });

    $("input, select").keypress(function(event){
        // Enterキーを押したとき
        if(event.keyCode === 13){
            let focus_taget = $(":focus").parent().parent()

            // inputの二つ上の要素をターゲットとします。
            let target = $(event.target).parent().parent()
            let data = get_data(target)

            if(!check_data(data)){
                current_id = null
                current_class = null
                current_data = null

                let scrtop = $(window).scrollTop()

                changeWorkReport(data,scrtop)
            }else{
                current_data = get_data(focus_taget)
            }
        }
    });

    $("input, select").on("blur", function(event){
        // フォーカスが外れたとき
        setTimeout(function(){
            let focus_taget = $(":focus").parent().parent()
            let focus_id = null
            let focus_class = null
            if(focus_taget.get(0)){
                focus_id = focus_taget.get(0).id.split(" ")[0]
                focus_class = focus_taget.get(0).className.split(" ")[0]
            }

            // inputの二つ上の要素をターゲットとします。
            let target = $(event.target).parent().parent()
            let data = get_data(target)

            if(!check_target(focus_id,focus_class)){
                if(!check_data(data)){
                    current_id = null
                    current_class = null
                    current_data = null

                    let scrtop = $(window).scrollTop()

                    changeWorkReport(data,scrtop)
                }else{
                    current_data = get_data(focus_taget)
                }
            }

        },100)

    });


});