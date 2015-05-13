function user_index(){

    //处理面板的隐藏与显示
    $(".app-panel-body").css('display', 'none');
    $(".app-panel-footer").css('display', 'none');

    $(".app-panel-head").click(function(){
        var appid = $(this).data("appid");

        $("#body-"+appid).toggle();
        $("#footer-"+appid).toggle();

        window.location.hash = appid;
    });

    var hash = window.location.hash;
    hash = hash.substr(1);
    if(hash != ''){
        $("#body-"+hash).toggle();
        $("#footer-"+hash).toggle();
    }
    
    //循环查询应用状态
    refresh_status_with_time();
}

function refresh_status(){
	$.ajax({
		'url': '/user/api',
		'dataType': 'json',
		'success': function(datas){
			$.each(datas, function(index, value){
				changeStatus(value.id, value.status);
			});
		},
		'error': function(){
			location.reload();
		}
	});
}

function refresh_status_with_time(){
	refresh_status();
	setTimeout('refresh_status_with_time()', 7000);
}

//处理应用操作
function option(aid,optionType,message){
	$.ajax({
		'type':'POST',
		'url':'/user/optionApp/'+optionType,
		'data':{'aid':aid},
		'success':function(data){
			refresh_status();
		},
		'error':function(t1,t2,t3){
			alert(message+'失败，如果多次出现该问题请询问技术人员！');
		}
	});
}

function changeStatus(appid, status){
	var panel_class;
	var status_info;

	switch(status){
            case 1: //运行中
            panel_class = "panel-success";
            break;

            case 2: //部署中
            panel_class = "panel-warning";
            break;

            case 5: //发布失败
            panel_class = "panel-danger";
            break;

            case -1: //未发布
            case 0: //未部署
            case 3: //已经停止 
            default:
            panel_class = "panel-default";
            break;
        }

        switch(status){
        	case -1: status_info = "未发布"; break;
        	case 0: status_info = "未部署"; break;
        	case 1: status_info = "运行中"; break;
        	case 2: status_info = "部署中"; break;
        	case 3: status_info = "已经停止"; break;
        	case 5: status_info = "发布失败"; break;
        }

        $("#panel-"+appid).removeClass("panel-success").removeClass("panel-warning")
        .removeClass("panel-danger").removeClass("panel-danger").addClass(panel_class);
        $("#status-"+appid).html(status_info);
    }