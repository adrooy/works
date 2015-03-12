# -*- coding: utf-8 -*-
# __author__ = 'sunzhennan'

import sdcard_pb2, sdcard, log
import os, sys, shutil, subprocess

def dump(folders, filename):
    f = open(filename, "wb")
    f.write(folders.SerializeToString())
    f.close()
    #print folders

def start(pkgname):
    log.set_pkgname(pkgname)
    filename = pkgname + "/start.bin"

    if os.path.exists(filename):
        print u"测试数据已存在, 清除数据开始新的测试? (Y / N)"
        user_input = raw_input()
        if user_input == 'y' or user_input == 'Y':
            shutil.rmtree(pkgname)
            os.makedirs(pkgname)
        else:
            print u"如果需要多份测试数据的话, 请自行对目录进行改名"
            return
    else:
        if not os.path.exists(pkgname):
            os.makedirs(pkgname)

    root = sdcard.parse()
    dump(root, filename)
    print u"Success"

def end(pkgname):
    log.set_pkgname(pkgname)

    if not os.path.exists(pkgname + "/start.bin"):
        print u"初始测试数据不存在, 请先运行start"
        return

    root = sdcard.parse()
    dump(root, pkgname + "/end.bin")
    print u"Success"

def compare_folder(old, new, diff):
    # diff = new - old
    diff.name = new.name
    diff.fullpath = new.fullpath

    for new_folder in new.folders:
        found = False
        for old_folder in old.folders:
            # compare both-have folder
            if old_folder.fullpath == new_folder.fullpath:
                found = True
                diff_folder = diff.folders.add()
                diff_folder.name = old_folder.name
                diff_folder.fullpath = old_folder.fullpath
                compare_folder(old_folder, new_folder, diff_folder)
                break

        # newly added folder
        if not found:
            diff.folders.extend([new_folder])

        # ignore deleted folders, they'll be handled with the same function

    for new_file in new.files:
        if not new_file in old.files:
            diff.files.append(new_file)

def is_empty_folder(folder):
    if len(folder.files) > 0:
        return False
    for sub in folder.folders:
        if not is_empty_folder(sub):
            return False
    return True

def remove_empty_folder(folder):
    to_be_removed = []
    for sub in folder.folders:
        if is_empty_folder(sub):
            to_be_removed.append(sub)
        else:
            remove_empty_folder(sub)
    for sub in to_be_removed:
        folder.folders.remove(sub)

def compare(pkgname):
    log.set_pkgname(pkgname)

    start_filename = pkgname + "/start.bin"
    end_filename = pkgname + "/end.bin"
    if not os.path.exists(start_filename):
        print u"%s的初始测试数据不存在, 请先运行start" % pkgname
        return
    if not os.path.exists(end_filename):
        print u"%s的结果测试数据不存在, 请先运行end" % pkgname
        return

    start_root = sdcard_pb2.Folder()
    start_root.ParseFromString(open(start_filename, "rb").read())
    end_root = sdcard_pb2.Folder()
    end_root.ParseFromString(open(end_filename, "rb").read())

    added_root = sdcard_pb2.Folder()
    deleted_root = sdcard_pb2.Folder()

    compare_folder(start_root, end_root, added_root)
    compare_folder(end_root, start_root, deleted_root)

    remove_empty_folder(added_root)
    remove_empty_folder(deleted_root)

    dump(added_root, pkgname + "/added.bin")
    dump(deleted_root, pkgname + "/deleted.bin")
    # print added_root
    # print '\n======================================================================================\n'

    return added_root, deleted_root


def pull(folder, pkgname):
    log.set_pkgname(pkgname)

    disk_root = pkgname + "\\diff"
    if os.path.exists(disk_root):
        print u"结果文件已存在, 重新抓取结果文件? (Y / N)"
        user_input = raw_input()
        if user_input == 'y' or user_input == 'Y':
            shutil.rmtree(disk_root, ignore_errors=True)
        else:
            return

    os.makedirs(disk_root)

    sdcard.pull_folder(folder, disk_root)

def print_folder(folder):
    path = folder.fullpath.replace('//', '/')
    for file in folder.files:
        print path+file
    for sub in folder.folders:
        print_folder(sub)

if __name__ == "__main__":
    if "start" == sys.argv[1]:
        start(sys.argv[2])
    elif "end" == sys.argv[1]:
        end(sys.argv[2])
    elif "getdiff" == sys.argv[1]:
        added, deleted = compare(sys.argv[2])
        if len(deleted.files) > 0 or len(deleted.folders) > 0:
            print u"被删除的文件: (start里有, 但end里没有)"
            print_folder(deleted)

        print u"开始抓取新增的文件: (end里有, 但start里没有)"
        pull(added, sys.argv[2])




