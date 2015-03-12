    $('html').ajaxSend(function(event, xhr, settings) {  
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
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {  
            // Only send the token to relative URLs i.e. locally.  
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));  
        }  
    });  
$("#download").click(function(){
    var assign_to = $("#assign_to").val();
    var title = $("#title").val();
    var version = $("#version").val();
    var package_name = $("#package_name").val();
    if (assign_to != 'None'){
	window.location.href = '/permission/downloadApk/?assign_to='+assign_to+'&title='+title+'&version='+version+'&package_name='+package_name;
    }
});
$("#assign_to").change(function(){
    var assign_to = $("#assign_to").val();
    var assign_time = $("#assign_time").val();
    var finished = $("#finished").val();
    var approved = $("#approved").val();
    if (assign_to != 'None'){
        window.location.href = '/permission/page/?assign_to='+assign_to+'&finished='+finished+'&approved='+approved+'&assign_time='+assign_time;
    }
});
$("#assign_time").change(function(){
    var assign_to = $("#assign_to").val();
    var assign_time = $("#assign_time").val();
    var finished = $("#finished").val();
    var approved = $("#approved").val();
    if (assign_to != 'None'){
        window.location.href = '/permission/page/?assign_to='+assign_to+'&finished='+finished+'&approved='+approved+'&assign_time='+assign_time;
    }
});
$("#finished").change(function(){
    var assign_to = $("#assign_to").val();
    var assign_time = $("#assign_time").val();
    var finished = $("#finished").val();
    var approved = $("#approved").val();
    if (assign_to != 'None'){
        window.location.href = '/permission/page/?assign_to='+assign_to+'&finished='+finished+'&approved='+approved+'&assign_time='+assign_time;
    }
});
$("#approved").change(function(){
    var assign_to = $("#assign_to").val();
    var assign_time = $("#assign_time").val();
    var finished = $("#finished").val();
    var approved = $("#approved").val();
    if (assign_to != 'None'){
        window.location.href = '/permission/page/?assign_to='+assign_to+'&finished='+finished+'&approved='+approved+'&assign_time='+assign_time;
    }
});
$("#return").click(function(){
    var assign_to = $("#assign_to").val();
    var page = $("#page").val();
    var assign_time = $("#assign_time").val();
    var package_name = $("#package_name").val();
    if (assign_to != 'None'){
        window.location.href = '/permission/page/?assign_to='+assign_to+'&page='+page+'&assign_time='+assign_time;
    }
});
$("#save_approved").click(function(){
    var assign_to = $("#assign_to").val();
    var title = $("#title").val();
    var version = $("#version").val();
    var package_name = $("#package_name").val();
    var descJson = {};
    descJson['title'] = title;
    descJson['assign_to'] = assign_to;
    descJson['version'] = version;
    descJson['package_name'] = package_name;
    $.post('/permission/is_approved/', descJson, function(result){
        alert(result);
    });
});
$("#save_notapproved").click(function(){
    var assign_to = $("#assign_to").val();
    var title = $("#title").val();
    var version = $("#version").val();
    var package_name = $("#package_name").val();
    var descJson = {};
    descJson['title'] = title;
    descJson['assign_to'] = assign_to;
    descJson['version'] = version;
    descJson['package_name'] = package_name;
    $.post('/permission/not_approved/', descJson, function(result){
        alert(result);
    });
});
$("#save_pending").click(function(){
    var assign_to = $("#assign_to").val();
    var title = $("#title").val();
    var version = $("#version").val();
    var package_name = $("#package_name").val();
    var descJson = {};
    descJson['title'] = title;
    descJson['assign_to'] = assign_to;
    descJson['version'] = version;
    descJson['package_name'] = package_name;
    $.post('/permission/is_pending/', descJson, function(result){
        alert(result);
    });
});
$("#save_record").click(function(){
    var assign_to = $("#assign_to").val();
    var title = $("#title").val();
    var version = $("#version").val();
    var category = $("#category").val();
    var package_name = $("#package_name").val();
    var descJson = {}
    $('input[type="text"]', '#input').each(function(){
            var desc_id = $(this).attr('id');
            var desc = $(this).val();
            if (desc){
            descJson[desc_id] = desc;
            }
        });
    $('input[type="radio"]:checked', '#input').each(function(){
            var sug_name = $(this).attr('name');
            var sug = $(this).val();
            if (sug) {
                 descJson[sug_name] = sug;
            }
        });
    descJson['title'] = title;
    descJson['assign_to'] = assign_to;
    descJson['version'] = version;
    descJson['category'] = category;
    descJson['package_name'] = package_name;
    //alert(JSON.stringify(descJson));
    var sendmms = $("#perm_sendmms_suggest").val();  
    $.post('/permission/is_finished/', descJson, function(result){
        alert(result);
    });
});
$("#check").click(function(){
    var assign_to = $("#assign_to").val();
    var title = $("#title").val();
    var version = $("#version").val();
    var category = $("#category").val();
    var package_name = $("#package_name").val();
    var descJson = {};
    descJson['title'] = title;
    descJson['assign_to'] = assign_to;
    descJson['version'] = version;
    descJson['category'] = category;
    descJson['package_name'] = package_name;
//    alert(JSON.stringify(descJson));
    $.post('/permission/checkApk/', descJson, function(result){
        alert(result);
    });
});
