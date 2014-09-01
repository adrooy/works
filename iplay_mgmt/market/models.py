#-*- coding:utf-8 -*-


from django.db import models


class TopicInfo(models.Model):
    id = models.IntegerField('ID', max_length=11, primary_key=True, null=False)
    name = models.CharField('专题名称', max_length=400)
    short_desc = models.CharField('简单描述信息（一句话）', max_length=1000)
    detail_desc = models.CharField('详细描述信息', max_length=10000)
    pic_url = models.CharField('图片地址', max_length=1000)
    topic_date =  models.IntegerField('专题发布时间', max_length=11)
    order_num = models.IntegerField('topic的排列序号', max_length=11)
    enabled = models.IntegerField('有效', max_length=11)

    class Meta:
        db_table = 'iplay_topic_info'
        verbose_name_plural = '专题信息'

class TopicGame(models.Model):
    id = models.IntegerField('ID', max_length=11, primary_key=True, null=False)
    topic_id = models.IntegerField('专题ID（对应iplay_topic_info的id）', max_length=11)
    game_id = models.CharField('游戏ID（对应game_label_info的id）', max_length=11)
    game_name = models.CharField('游戏名称', max_length=200) 
    order_num = models.IntegerField('该游戏在topic中的位置', max_length=11)

    class Meta:
        db_table = 'iplay_topic_game'
        verbose_name_plural = '专题下游戏列表信息'
    
class GameLabelInfo(models.Model):
    game_id = models.CharField('游戏ID', max_length=8, primary_key=True)
    game_name = models.CharField('游戏名', max_length=50)
    display_name = models.CharField('游戏显示名', max_length=50)
    game_types = models.CharField('', max_length=1000)
    game_tags = models.CharField('', max_length=1000)
    screen_shot_urls = models.CharField('', max_length=5000)
    icon_url = models.CharField('', max_length=1000)
    forum_url = models.CharField('', max_length=1000)
    post_url = models.CharField('', max_length=1000)
    tid = models.IntegerField('', max_length=11)
    short_desc = models.CharField('', max_length=1000)
    detail_desc = models.CharField('', max_length=8000)
    star_num = models.IntegerField('', max_length=11)
    download_counts = models.IntegerField('', max_length=11)
    game_language = models.CharField('', max_length=200)
    save_timestamp = models.IntegerField('', max_length=11)
    update_timestamp = models.IntegerField('', max_length=11)
    min_apk_size = models.IntegerField('', max_length=11)
    max_apk_size = models.IntegerField('', max_length=11)
    min_ver_name = models.CharField('', max_length=20)
    max_ver_name = models.CharField('', max_length=20)
    enabled = models.IntegerField('', max_length=1)
    subscript = models.CharField('', max_length=50)
    color_label = models.CharField('', max_length=50)
    source = models.IntegerField('', max_length=1)
    is_changed = models.BooleanField('是否修改', max_length=1)

    class Meta:
        db_table = 'iplay_game_label_info'
        verbose_name_plural = '游戏信息'

class RecGame(models.Model):
    game_id = models.CharField('游戏ID', max_length=11, primary_key=True)
    game_name = models.CharField('游戏名称', max_length=200)
    order_num = models.IntegerField('该游戏在推荐页中的位置', max_length=11)
    manual_num = models.IntegerField('该游戏的真实序号', max_length=11)

    class Meta:
        db_table = 'iplay_recomend_game'
        verbose_name_plural = '推荐页游戏列表'

class RecBanner(models.Model):
    id = models.IntegerField('ID', max_length=11, primary_key=True, null=False)
    topic_id = models.IntegerField('专题ID（对应iplay_topic_info的id）', max_length=11)
    game_id = models.CharField('游戏ID（对应game_label_info的id）', max_length=11)
    name = models.CharField('banner名称', max_length=200)
    pic_url = models.CharField('图片地址', max_length=1000) 
    order_num = models.IntegerField('该banner在推荐页中的位置', max_length=11) 
    enabled = models.IntegerField('有效', max_length=11)

    class Meta:
        db_table = 'iplay_recomend_banner_info'
        verbose_name_plural = '推荐页banner列表'

class CatGame(models.Model):
    game_id = models.CharField('游戏ID', max_length=11, primary_key=True)
    game_name = models.CharField('游戏名称', max_length=200)
    category_id = models.IntegerField('分类ID', max_length=11)
    order_num = models.IntegerField('该游戏在推荐页中的位置', max_length=11)
    manual_num = models.IntegerField('该游戏的真实序号', max_length=11)

    class Meta:
        db_table = 'iplay_category_game_order_adjust'
        verbose_name_plural = '分类页游戏列表(人工)'

class GameCatInfo(models.Model):
    id = models.IntegerField('ID', max_length=11, primary_key=True, null=False)
    name = models.CharField('游戏名称', max_length=200)
    display_name = models.CharField('游戏名称', max_length=200)
    parent_id = models.IntegerField('', max_length=11)
    show_order_num = models.IntegerField('', max_length=11) 
    
    class Meta:
        db_table = 'iplay_game_category_info'
        verbose_name_plural = '游戏分类信息'

class CatToGame(models.Model):
    id = models.IntegerField('ID', max_length=11, primary_key=True, null=False) 
    category_id = models.IntegerField('分类ID', max_length=11)
    game_id = models.CharField('游戏ID', max_length=11)
    order_by_dl_cnt = models.IntegerField('该游戏在分类下的排序', max_length=11)
    
    class Meta:
        db_table = 'iplay_category_to_game_result'
        verbose_name_plural = '非类页游戏列表（系统）'

class HotSearch(models.Model):
    word = models.CharField('热门词', max_length=40, primary_key=True)
    order_num = models.IntegerField('', max_length=11)
 
    class Meta:
        db_table = 'iplay_hot_search_words'
        verbose_name_plural = '热门词'
