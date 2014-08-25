#-*- coding:utf-8 -*-


from django.db import models


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

class GamePkgInfo(models.Model):
    apk_id = models.CharField('', max_length=8, primary_key=True)
    game_id = models.CharField('', max_length=8)
    market_channel = models.CharField('', max_length=45)
    game_name = models.CharField('', max_length=45)
    pkg_name = models.CharField('', max_length=100)
    file_md5 = models.CharField('', max_length=32)
    ver_code = models.IntegerField('', max_length=11)
    ver_name = models.CharField('', max_length=40)
    signature_md5 = models.CharField('', max_length=32)
    file_size = models.IntegerField('', max_length=11)
    download_url = models.CharField('', max_length=1000)
    forum_url = models.CharField('', max_length=1000)
    post_url = models.CharField('', max_length=1000)
    min_sdk = models.IntegerField('', max_length=11)
    game_desc = models.CharField('', max_length=8000)
    game_types = models.CharField('', max_length=1000)
    game_tags = models.CharField('', max_length=1000)
    downloaded_cnts = models.IntegerField('', max_length=11)
    is_crack_apk = models.IntegerField('', max_length=1)
    tid = models.IntegerField('', max_length=11)
    depend_google_play = models.IntegerField('', max_length=1)
    game_language = models.CharField('', max_length=200)
    save_timestamp = models.IntegerField('', max_length=11)
    update_timestamp = models.IntegerField('', max_length=11)
    screen_shot_urls = models.CharField('', max_length=5000)
    icon_url = models.CharField('', max_length=1000)
    is_max_version = models.IntegerField('', max_length=1)
    download_url_type = models.IntegerField('', max_length=4)
    enabled = models.IntegerField('', max_length=1)

    class Meta:
        db_table = 'iplay_game_pkg_info'
        verbose_name_plural = '游戏安装包信息'
