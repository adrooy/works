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
    var apk_id= $("#apk_id").val();
    window.location.href = '/sdcleaner/download/?apk_id='+apk_id;
});
$("#assign_to").change(function(){
    var assign_to = $("#assign_to").val();
    var assign_time = $("#assign_time").val();
    var finished = $("#finished").val();
    var approved = $("#approved").val();
    if (assign_to != 'None'){
        window.location.href = '/sdcleaner/page/?assign_to='+assign_to+'&finished='+finished+'&approved='+approved+'&assign_time='+assign_time;
    }
});
$("#assign_time").change(function(){
    var assign_to = $("#assign_to").val();
    var assign_time = $("#assign_time").val();
    var finished = $("#finished").val();
    var approved = $("#approved").val();
    if (assign_to != 'None'){
        window.location.href = '/sdcleaner/page/?assign_to='+assign_to+'&finished='+finished+'&approved='+approved+'&assign_time='+assign_time;
    }
});
$("#finished").change(function(){
    var assign_to = $("#assign_to").val();
    var assign_time = $("#assign_time").val();
    var finished = $("#finished").val();
    var approved = $("#approved").val();
    if (assign_to != 'None'){
        window.location.href = '/sdcleaner/page/?assign_to='+assign_to+'&finished='+finished+'&approved='+approved+'&assign_time='+assign_time;
    }
});
$("#approved").change(function(){
    var assign_to = $("#assign_to").val();
    var assign_time = $("#assign_time").val();
    var finished = $("#finished").val();
    var approved = $("#approved").val();
    if (assign_to != 'None'){
        window.location.href = '/sdcleaner/page/?assign_to='+assign_to+'&finished='+finished+'&approved='+approved+'&assign_time='+assign_time;
    }
});
$("#return").click(function(){
    var assign_to = $("#assign_to").val();
    var page = $("#page").val();
    var assign_time = $("#assign_time").val();
    var package_name = $("#package_name").val();
    if (assign_to != 'None'){
        window.location.href = '/sdcleaner/page/?assign_to='+assign_to+'&page='+page+'&assign_time='+assign_time;
    }
});
$('#add_record').click(function(){
    var count = $('#input_area div').length;
    var new_html = '<div id="file_path_'+count+'" class="pt_5" zz="new">'
        +'<input type="text" class="il_block w_300 align_left ml_4" zz="file_path" />'
        +'<input type="text" class="il_block w_100 align_left ml_4" zz="item_name" />'
        +'<textarea rows="1" class="il_block w_300 align_left ml_4" zz="desc"></textarea>'
        +'<textarea rows="1" class="il_block w_300 align_left ml_4" zz="alert_info"></textarea>'
        +'<input type="text" class="il_block w_200 align_left ml_4" zz="sub_path" />'
        +'<input type="text" class="il_block w_50 align_left ml_4" zz="sl" />'
        +'<input type="checkbox" class="il_block align_left ml_4" zz="delete" />'
        +'</div>';
    $('#input_area').append(new_html);
});
/*
$('#input_area').on('click', '.delete_button', function(){
    $(this).parent().remove();
});
*/
$("#save_approved").click(function(){
    var descJson = {'apk_id':$('#apk_id').val()};
    $.post('/sdcleaner/approve/', descJson, function(result){
        alert(result);
    });
});
$("#save_notapproved").click(function(){
    var descJson = {'apk_id':$('#apk_id').val()};
    $.post('/sdcleaner/disapprove/', descJson, function(result){
        alert(result);
    });
});
$("#save_pending").click(function(){
    var descJson = {'apk_id':$('#apk_id').val()};
    $.post('/sdcleaner/pend/', descJson, function(result){
        alert(result);
    });
});
$("#save_record").click(function(){
    var delete_paths = [];
    var add_paths = [];
    var update_paths = [];
    $('div', '#input_area').each(function(){
        if ($(this).attr('zz') == 'new'){
            if($('input[zz="delete"]',$(this)).is(':checked'))
                return;
            var add_path = {'file_path':$('input[zz="file_path"]',$(this)).val(),
                'item_name':$('input[zz="item_name"]',$(this)).val(),
                'desc':$('textarea[zz="desc"]',$(this)).val(),
                'alert_info':$('textarea[zz="alert_info"]',$(this)).val(),
                'sub_path':$('input[zz="sub_path"]',$(this)).val(),
                'sl':$('input[zz="sl"]',$(this)).val()
            };
            add_paths.push(add_path);
        } else {
            if($('input[zz="delete"]',$(this)).is(':checked'))
                delete_paths.push($('input[zz="path_info_id"]',$(this)).val());
            else{
            var update_path = {'file_path':$('input[zz="file_path"]',$(this)).val(),
                'item_name':$('input[zz="item_name"]',$(this)).val(),
                'desc':$('textarea[zz="desc"]',$(this)).val(),
                'alert_info':$('textarea[zz="alert_info"]',$(this)).val(),
                'sub_path':$('input[zz="sub_path"]',$(this)).val(),
                'sl':$('input[zz="sl"]',$(this)).val(),
                'id':$('input[zz="path_info_id"]',$(this)).val()
            };
            update_paths.push(update_path);
            }
        }
    });
    var descJson = {'apk_id':$('#apk_id').val(),'add_paths':JSON.stringify(add_paths),'update_paths':JSON.stringify(update_paths),'delete_paths':JSON.stringify(delete_paths),'is_finished':$('input[name="is_finished"]:checked').val(),'comments':$('#comments').val()};
    //alert(JSON.stringify(descJson));
    $.post('/sdcleaner/save/', descJson, function(result){
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
    alert(JSON.stringify(descJson));
    $.post('/sdcleaner/checkApk/', descJson, function(result){
        alert(result);
    });
});
