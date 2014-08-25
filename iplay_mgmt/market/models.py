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
    game_id = models.CharField('游戏ID', max_length=11, primary_key=True)
    game_name = models.CharField('游戏名称', max_length=200) 
    enabled = models.IntegerField('', max_length=1)

    def __unicode__(self):
        return self.game_id, self.game_name
    
    class Meta:
        db_table = 'iplay_game_label_info'
        verbose_name_plural = '游戏列表'

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
