#coding: utf-8
# __author__ = 'sunzhennan'

import sdcard_pb2, log, re
import subprocess, time, os, sys

# adb在处理中文的UTF-8的时候有bug, 譬如:
#     > adb shell ls -l /mnt/shell/emulated/0/bestpay/html/添益宝
#     /mnt/shell/emulated/0/bestpay/html/添益�: No such file or directory
# 必须要加一个/在最后:
#     adb shell ls -l /mnt/shell/emulated/0/bestpay/html/添益宝/
#     drwxrwxr-x root     sdcard_rw          2014-06-25 15:27 css
# 这还没完, 如果要查看中文目录下子目录里的内容, 单个/还是不行:
#     adb shell ls -l /mnt/shell/emulated/0/bestpay/html/添益宝/css
#     /mnt/shell/emulated/0/bestpay/html/添益�?css: No such file or directory
# 必须用两个/才行:
#     adb shell ls -l /mnt/shell/emulated/0/bestpay/html/添益宝//css
#     -rw-rw-r-- root     sdcard_rw      935 2014-06-17 17:34 question.css
# 可这样做, 可能会在某些机器上有问题, 所以用这个全局变量控制, 如果支持//的机器, 就设为True, 支持中文. 如果不支持//的机器, 就设为False, 是否支持中文要测试了才知道
g_double_slash = True

def append_double_slash(str):
    global g_double_slash
    if g_double_slash:
        return str + "/"
    else:
        return str


def adb_ll(folder):
    cmd = ["adb", "shell", "ls", "-l", folder.encode('utf-8')]
    log.write("\n\n>" + " ".join(cmd))

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rtn = []
    for line in iter(p.stdout.readline, b''):
        line = line.strip().rstrip()

        # if "No such file" in line:
        #     log.write("\n\n---  " + ":".join("{:02x}".format(ord(c)) for c in line))
        #     log.write("\n\n---  " + line)

        rtn.append(line.decode("utf-8"))
        log.write(line)

    if (len(rtn) > 0 and len(rtn[0]) == 0) or (len(rtn) > 0 and "No such file" in rtn[0]):
        log.write("获取%s目录信息出错" % folder)
        raise Exception(folder)
    return rtn


def adb_pull(src, dst):
    # src = u'"' + src + u'"'
    if dst[-1] == '/':
        dst = dst[:-1]
    # dst = u'"' + dst + u'"'
    cmd = ["adb", "pull", src.encode('utf-8'), dst.encode('utf-8')]
    log.write("\n>" + " ".join(cmd))
    print(" ".join(cmd))

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    rtn = []
    for line in iter(p.stdout.readline, b''):
        line = line.strip().rstrip()
        log.write(line)


def follow_symbol(link):
    while(True):
        list = adb_ll(link)
        if list[0][0] == 'l':
            link = list[0].split(" ")[-1].strip().rstrip()
        else:
            break
    return link


def parse_folder(folder):
    list = adb_ll(folder.fullpath)
    for line in list:
        if line[0] == 'd':
            current = folder.folders.add()
            #current.name = line[55:].rstrip() # 文件名可能带空格, 所以不能split(' '), 解析太麻烦了, 希望所有的adb输出都是固定格式...
            current.name = re.split("\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+",line.rstrip())[-1] #zuozhen add this
            current.fullpath = append_double_slash (folder.fullpath + "/" + current.name)
            parse_folder(current)

        elif line[0] == 'l':
            # 无法区分 文件符号链接  与 只有一个文件的文件夹的符号链接, 所以都当做文件夹处理, 便于兼容有多个文件的文件夹的符号链接
            # 但这里还需要考虑double slash的问题, 如果是文件的话, 后面加一个/肯定会出错
            # 逻辑太复杂, 遇到再说
            raise Exception(line[0])
            # real_path = follow_symbol(line.split(" ")[-1].strip().rstrip())
            # current = folder.folders.add()
            # current.name = os.path.basename(real_path)
            # current.fullpath = real_path
            # parse_folder(current)

        else:
            folder.files.append(re.split("\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+",line.rstrip())[-1]) #same as current.name above, zuozhen



def parse():
    real_path = follow_symbol( append_double_slash("/sdcard") )

    root = sdcard_pb2.Folder()
    root.name = "/"
    root.fullpath = real_path

    parse_folder(root)
    return root


def pull_folder(folder, disk_root):
    path = folder.fullpath.replace("//", "/")
    disk_path = os.path.join(disk_root, path[1:]).replace('\\', '/') # remove the leading /
    if not os.path.exists(disk_path):
        os.mkdir(disk_path)

    for file in folder.files:
        src = os.path.join(path, file)
        adb_pull(src, disk_path)

    for sub in folder.folders:
        pull_folder(sub, disk_root)

