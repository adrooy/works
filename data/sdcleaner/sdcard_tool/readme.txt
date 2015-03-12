假设待测应用是com.sina.news

1. 获取初始数据
python tool.py start com.sina.news

2. 安装应用, 使用

3. 获取结束数据
python tool.py end com.sina.news

4. 获取新增文件
python tool.py getdiff com.sina.news

备注:
1. 命令行上的包名只是用于建目录使用, 可以随便写, 但建议遵循规范, 用包名做目录名, 便于以后检查数据
2. 在重复测试同一款应用时, 脚本可能会提示需要删除已有数据, 敲Y确认后, 如果报错, 则是python的bug, 可以手动删除数据再运行
3. 中文名的文件, 在获取后文件名会是没有decode的UTF-8, 这是cmd.exe的局限, 暂时没有办法. 如果非常有必要, 未来可以在脚本里强制更名
4. 如果在结束时, sd卡上少了一些文件, getdiff命令会把少了文件名输出在屏幕上
