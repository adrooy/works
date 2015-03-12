#-*- coding:utf-8 -*-


from django.db import models


class ApkInfo(models.Model):
    id = models.IntegerField('ID', max_length=11, primary_key=True, null=False)
    package_name = models.CharField('app包名', max_length=2000)
    title = models.CharField('app中文名', max_length=2000)
    assign_to = models.CharField('将该app分配给谁', max_length=2000)
    assign_time = models.DateTimeField('分配时间')
    last_modified =  models.DateTimeField('最后更新时间')
    finished = models.IntegerField('是否完成', default=0)
    approved = models.IntegerField('是否通过', default=0)
    comments = models.CharField('备注', max_length=2000)
    version_code = models.CharField('版本号', max_length=10)

    class Meta:
        db_table = 'apk_info'
        verbose_name_plural = 'apk信息'

class PathInfo(models.Model):
    id = models.IntegerField('ID', max_length=11, primary_key=True, null=False)
    file_path = models.CharField('路径名', max_length=2000)
    item_name = models.CharField('路径名', max_length=2000)
    alert_info = models.CharField('路径名', max_length=2000)
    desc = models.CharField('路径名', max_length=2000)
    sub_path = models.CharField('regex格式的子目录', max_length=2000)
    sl = models.CharField('regex格式的子目录的层级数', max_length=100)
    apk_id = models.IntegerField('Apk ID（对应apk_info的id）', max_length=11)
    path_hash = models.CharField('路径的hash，做唯一标识用', max_length=10)

    class Meta:
        db_table = 'path_info'
        verbose_name_plural = '路径信息'
