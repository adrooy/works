$(document).ready(function(){ 
//    $("p:odd").css("background-color", "#bbf"); 
//    $("p:even").css("background-color","#ffc"); 
    $("tr").click(function () { 
        $("tr").each(function(){ 
        if($(this).hasClass("highlight")){ 
            $(this).removeClass("highlight"); 
            }}); 
        if($(this).attr('id')){
            $(this).addClass("highlight"); 
        }
    }); 
});
$("#topic_add").click(function(){
    var topic_id = $(".highlight#topic").attr("value");
    window.location.href = '/iplay_mgmt/market/topic_add/?topic_id='+topic_id;
    //window.location.href = '/market/topic_add/';
});
$("#topic_alter").click(function(){
    var topic_id = $(".highlight#topic").attr("value");
    if(topic_id){
        window.location.href = '/iplay_mgmt/market/topic_alter/?topic_id='+topic_id;
    }else{
        alert("请选择专题！！！");
    }
});
$("#topic_isenabled").click(function(){
    var topic_id = $(".highlight#topic").attr("value");
    var descJson = {}
    descJson['topic_id'] = topic_id;
    alert(topic_id);
    if(topic_id){
        $.post('/iplay_mgmt/market/topic_isenabled/', descJson, function(result){
            alert(result);
            window.location.href = '/iplay_mgmt/market/topic';
        });
    }else{
        alert("请选择专题！！！");
    }
});
$("#topic_notenabled").click(function(){
    var topic_id = $(".highlight#topic").attr("value");
    var descJson = {}
    descJson['topic_id'] = topic_id;
    if(topic_id){
        $.post('/iplay_mgmt/market/topic_notenabled/', descJson, function(result){
            alert(result);
            window.location.href = '/iplay_mgmt/market/topic';
        });
    }else{
        alert("请选择专题！！！");
    }
});
$("#topic_move").click(function(){
    var topic_id = $(".highlight#topic").attr("value");
    var descJson = {}
    descJson['topic_id'] = topic_id;
    if(topic_id){
        var index = prompt('请输入要移动到的位置');
        descJson['index'] = index;
        $.post('/iplay_mgmt/market/topic_move/', descJson, function(result){
                window.location.href = '/iplay_mgmt/market/topic/?topic_id='+topic_id;
        });
    }else{
        alert("请选择专题！！！");
    }
});
$("#topic_up").click(function(){
    var topic_id = $(".highlight#topic").attr("value");
    var descJson = {}
    descJson['topic_id'] = topic_id;
    if(topic_id){
        $.post('/iplay_mgmt/market/topic_up/', descJson, function(result){
            if(result=='Yes'){
                window.location.href = '/iplay_mgmt/market/topic/?topic_id='+topic_id;
            }else{
                alert('已经是第一个专题！！！');
            }
        });
    }else{
        alert("请选择专题！！！");
    }
});
$("#topic_down").click(function(){
    var topic_id = $(".highlight#topic").attr("value");
    var descJson = {}
    descJson['topic_id'] = topic_id;
    if(topic_id){
        $.post('/iplay_mgmt/market/topic_down/', descJson, function(result){
            if(result=='Yes'){
                window.location.href = '/iplay_mgmt/market/topic/?topic_id='+topic_id;
            }else{
                alert('已经是最后一个专题！！！');
            }
        });
    }else{
        alert("请选择专题！！！");
    }
});
$("#topic_edit").click(function(){
    var id = $("#topic_id").val();
    var topic_id_index = $("#topic_id_index").val();
    var name = $("#topic_name").val();
    var short_desc = $("#topic_short_desc").val();
    var detail_desc = $("#topic_detail_desc").val();
    var pic_url = $("#topic_pic_url").val();
    var descJson = {}
    descJson['id'] = id;
    descJson['name'] = name;
    descJson['short_desc'] = short_desc;
    descJson['detail_desc'] = detail_desc;
    descJson['pic_url'] = pic_url;
    descJson['topic_id_index'] = topic_id_index;
    //alert(JSON.stringify(descJson));
    $.post('/iplay_mgmt/market/topic_edit/', descJson, function(topic_id){
        window.location.href = '/iplay_mgmt/market/topic_alter/?topic_id='+topic_id;
    });
});
$("#topic_delete").click(function(){
    var topic_id = $(".highlight#topic").attr("value");
    var descJson = {}
    descJson['topic_id'] = topic_id;
    if(topic_id){
        if(confirm('确认删除吗？')){
            $.post('/iplay_mgmt/market/topic_delete/', descJson, function(result){
            window.location.href = '/iplay_mgmt/market/topic/';
            });
        }else{
            alert('取消删除！');
        }
    }else{
        alert("请选择专题！！！");
    }
});
$("#game_add").click(function(){
    var topic_id = $("#topic_id").val();
    if(topic_id){
        var game_id = prompt('请输入添加的游戏ID');
        var game_id_index = $(".highlight#game").attr("value");
        var descJson = {}
        descJson['topic_id'] = topic_id;
        descJson['game_id'] = game_id;
        descJson['game_id_index'] = game_id_index;
        $.post('/iplay_mgmt/market/topic_addGame/', descJson, function(result){
            alert(result);
            window.location.href = '/iplay_mgmt/market/topic_alter/?topic_id='+topic_id;
        });
    }
});
$("#game_delete").click(function(){
    var game_id = $(".highlight#game").attr("value");
    var topic_id = $("#topic_id").val();
    var descJson = {}
    descJson['topic_id'] = topic_id;
    descJson['game_id'] = game_id;
    if(game_id){
        if(confirm('确认删除吗？')){
            $.post('/iplay_mgmt/market/topic_delGame/', descJson, function(result){
                window.location.href = '/iplay_mgmt/market/topic_alter/?topic_id='+topic_id;
            });
        }else{
            alert('取消删除！');
        }
    }else{
        alert("请选择游戏！！！");
    }
});
$("#game_move").click(function(){
    var game_id = $(".highlight#game").attr("value");
    var topic_id = $("#topic_id").val();
    var descJson = {}
    descJson['topic_id'] = topic_id;
    descJson['game_id'] = game_id;
    if(game_id){
        var index = prompt('请输入要移动到的位置');
        descJson['index'] = index;
        $.post('/iplay_mgmt/market/topic_moveGame/', descJson, function(result){
                window.location.href = '/iplay_mgmt/market/topic_alter/?topic_id='+topic_id+'&game_id='+game_id;
        });
    }else{
        alert("请选择游戏！！！");
    }
});
$("#game_up").click(function(){
    var game_id = $(".highlight#game").attr("value");
    var topic_id = $("#topic_id").val();
    var descJson = {}
    descJson['topic_id'] = topic_id;
    descJson['game_id'] = game_id;
    if(game_id){
        $.post('/iplay_mgmt/market/topic_upGame/', descJson, function(result){
            if(result=='Yes'){
                window.location.href = '/iplay_mgmt/market/topic_alter/?topic_id='+topic_id+'&game_id='+game_id;
            }else{
                alert('已经是第一个游戏');
            }
        });
    }else{
        alert("请选择游戏！！！");
    }
});
$("#game_down").click(function(){
    var game_id = $(".highlight#game").attr("value");
    var topic_id = $("#topic_id").val();
    var descJson = {}
    descJson['topic_id'] = topic_id;
    descJson['game_id'] = game_id;
    if(game_id){
        $.post('/iplay_mgmt/market/topic_downGame/', descJson, function(result){
            if(result=='Yes'){
                window.location.href = '/iplay_mgmt/market/topic_alter/?topic_id='+topic_id+'&game_id='+game_id;
            }else{
                alert('已经是最后一个游戏');
            }
        });
    }else{
        alert("请选择游戏！！！");
    }
});
$("#recgame_add").click(function(){
        var game_id = prompt('请输入添加的游戏ID');
        var manual_num = prompt('请输入添加的游戏序号');
        var game_id_index = $(".highlight#game").attr("value");
        var descJson = {}
        descJson['game_id'] = game_id;
        descJson['game_id_index'] = game_id_index;
        descJson['manual_num'] = manual_num;
        $.post('/iplay_mgmt/market/recommend_addGame/', descJson, function(result){
            alert(result);
            window.location.href = '/iplay_mgmt/market/recommend/';
        });
});
$("#recgame_delete").click(function(){
    var game_id = $(".highlight#game").attr("value");
    var descJson = {}
    descJson['game_id'] = game_id;
    if(game_id){
        if(confirm('确认删除吗？')){
            $.post('/iplay_mgmt/market/recommend_delGame/', descJson, function(result){
                window.location.href = '/iplay_mgmt/market/recommend/';
            });
        }else{
            alert('取消删除！');
        }
    }else{
        alert("请选择游戏！！！");
    }
});
$("#recgame_move").click(function(){
    var game_id = $(".highlight#game").attr("value");
    var descJson = {}
    descJson['game_id'] = game_id;
    if(game_id){
        var index = prompt('请输入要移动到的位置');
        descJson['index'] = index;
        $.post('/iplay_mgmt/market/recommend_moveGame/', descJson, function(result){
                window.location.href = '/iplay_mgmt/market/recommend/?game_id='+game_id;
        });
    }else{
        alert("请选择游戏！！！");
    }
});
$("#recgame_up").click(function(){
    var game_id = $(".highlight#game").attr("value");
    var descJson = {}
    descJson['game_id'] = game_id;
    if(game_id){
        $.post('/iplay_mgmt/market/recommend_upGame/', descJson, function(result){
            if(result=='Yes'){
                window.location.href = '/iplay_mgmt/market/recommend/?game_id='+game_id;
            }else{
                alert('已经是第一个游戏');
            }
        });
    }else{
        alert("请选择游戏！！！");
    }
});
$("#recgame_down").click(function(){
    var game_id = $(".highlight#game").attr("value");
    var descJson = {}
    descJson['game_id'] = game_id;
    if(game_id){
        $.post('/iplay_mgmt/market/recommend_downGame/', descJson, function(result){
            if(result=='Yes'){
                window.location.href = '/iplay_mgmt/market/recommend/?game_id='+game_id;
            }else{
                alert('已经是最后一个游戏');
            }
        });
    }else{
        alert("请选择游戏！！！");
    }
});
/*
$("#banner_add").click(function(){
        var new_id = prompt('请输入添加的游戏或者专题ID');
        var pic_url = prompt('请输入图片地址');
        var id_index = $(".highlight#banner").attr("value");
        var descJson = {}
        descJson['new_id'] = new_id;
        descJson['id_index'] = id_index;
        descJson['pic_url'] = pic_url;    
        //alert(JSON.stringify(descJson));
        $.post('/iplay_mgmt/market/recommend_addBanner/', descJson, function(result){
            if(result=='No'){
                alert('请输入正确的游戏或者专题ID！！！');
            }else{
                window.location.href = '/iplay_mgmt/market/recommend/';
            }
        });
});
*/
$("#banner_add").click(function(){
    var banner_id = $(".highlight#banner").attr("value");
    window.location.href = '/iplay_mgmt/market/recommend_addBanner/?banner_id='+banner_id;
});
$("#banner_alter").click(function(){
    var banner_id = $(".highlight#banner").attr("value");
    if(banner_id){
        window.location.href = '/iplay_mgmt/market/recommend_alterBanner/?banner_id='+banner_id;
    }else{
        alert("请选择专题！！！");
    }
});
$("#banner_edit").click(function(){
    var banner_id = $("#banner_id").val();
    var banner_id_index = $("#banner_id_index").val();
    var name = $("#banner_name").val();
    var game_id = $("#banner_game_id").val();
    var topic_id = $("#banner_topic_id").val();
    var pic_url = $("#banner_pic_url").val();
    var descJson = {}
    descJson['banner_id'] = banner_id;
    descJson['name'] = name;
    descJson['game_id'] = game_id;
    descJson['topic_id'] = topic_id;
    descJson['pic_url'] = pic_url;
    descJson['banner_id_index'] = banner_id_index;
    //alert(JSON.stringify(descJson));
    $.post('/iplay_mgmt/market/recommend_editBanner/', descJson, function(result){
        if(result=='No'){
            alert('请输入正确的游戏或者专题ID！！！');
        }else{
            alert(result);
            window.location.href = '/iplay_mgmt/market/recommend/';
        }
    });
});
$("#banner_move").click(function(){
    var banner_id = $(".highlight#banner").attr("value");
    var descJson = {}
    descJson['banner_id'] = banner_id;
    if(banner_id){
        var index = prompt('请输入要移动到的位置');
        descJson['index'] = index;
        $.post('/iplay_mgmt/market/recommend_moveBanner/', descJson, function(result){
                window.location.href = '/iplay_mgmt/market/recommend/?banner_id='+banner_id;
        });
    }else{
        alert("请选择banner！！！");
    }
});
$("#banner_up").click(function(){
    var banner_id = $(".highlight#banner").attr("value");
    var descJson = {}
    descJson['banner_id'] = banner_id;
    if(banner_id){
        $.post('/iplay_mgmt/market/recommend_upBanner/', descJson, function(result){
            if(result=='Yes'){
                window.location.href = '/iplay_mgmt/market/recommend/?banner_id='+banner_id;
            }else{
                alert('已经是第一个banner');
            }
        });
    }else{
        alert("请选择游戏！！！");
    }
});
$("#banner_delete").click(function(){
    var banner_id = $(".highlight#banner").attr("value");
    var descJson = {}
    descJson['banner_id'] = banner_id;
    if(banner_id){
        if(confirm('确认删除吗？')){
            $.post('/iplay_mgmt/market/recommend_delBanner/', descJson, function(result){
                 window.location.href = '/iplay_mgmt/market/recommend/';
            });
        }else{
            alert('取消删除！');
        }
    }else{
        alert("请选择banner！！！");
    }
});
$("#banner_down").click(function(){
    var banner_id = $(".highlight#banner").attr("value");
    var descJson = {}
    descJson['banner_id'] = banner_id;
    if(banner_id){
        $.post('/iplay_mgmt/market/recommend_downBanner/', descJson, function(result){
            if(result=='Yes'){
                window.location.href = '/iplay_mgmt/market/recommend/?banner_id='+banner_id;
            }else{
                alert('已经是最后一个banner');
            }
        });
    }else{
        alert("请选择游戏！！！");
    }
});
$("#banner_isenabled").click(function(){
    var banner_id = $(".highlight#banner").attr("value");
    var descJson = {}
    descJson['banner_id'] = banner_id;
    if(banner_id){
        $.post('/iplay_mgmt/market/recommend_isenabledBanner/', descJson, function(result){
            window.location.href = '/iplay_mgmt/market/recommend/';
        });
    }else{
        alert("请选择专题！！！");
    }
});
$("#banner_notenabled").click(function(){
    var banner_id = $(".highlight#banner").attr("value");
    var descJson = {}
    descJson['banner_id'] = banner_id;
    if(banner_id){
        $.post('/iplay_mgmt/market/recommend_notenabledBanner/', descJson, function(result){
            window.location.href = '/iplay_mgmt/market/recommend/';
        });
    }else{
        alert("请选择专题！！！");
    }
});
$("#game_detail").click(function(){
    var game_id = $(".highlight#game").attr("value");
    if(game_id){
    	window.location.href = '/iplay_mgmt/game/detail/?game_id='+game_id;
    }else{
        alert("请选择游戏！！！");
    }
});
$("#release").click(function(){
    var descJson = {};
    if(confirm('确认发布吗？')){
        $.post('/iplay_mgmt/market/release/', descJson, function(result){
            alert('发布已完成！');
        });
    }else{
        alert('取消发布！');
    }
});
