#!/usr/bin/python
#! -*- coding:utf-8 -*-

import os
import sys
import time
import datetime
import logging

from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis, ganalysis
from androguard.core import androconf


'''
option_0 = {'name': ('-i', '--input'), 'help': 'filename input (apk)', 'nargs': 1}

options = [option_0]
'''

reload(sys)
sys.setdefaultencoding('utf-8')


def main(filename):

    logging.debug('intput: %s' % filename)
    logging.debug('output: %s' % filename.replace('.apk', '.csv'))
    print 'intput: %s' % filename
    print 'output: %s' % filename.replace('.apk', '.csv')
    if filename != None:
        ret_type = androconf.is_android(filename)

        vm = None
        a = None
        if ret_type == 'APK':
            a = apk.APK(filename)
            
            package = a.package
            versionCode = a.androidversion['Code']
            versionName = a.androidversion['Name']
            md5 = a.md5

            if a.is_valid_APK():
                vm = dvm.DalvikVMFormat(a.get_dex())
            else:
                print 'INVALID APK'
        else:
            print 'INPUT ERROR'
        
        vmx = analysis.VMAnalysis(vm)
        gvmx = ganalysis.GVMAnalysis(vmx, a)

        permissionfile = os.path.join(os.getcwd(), 'permission.cfg')
        permissions = {}
        with open(permissionfile) as files:
            for line in files:
                line_info = line.strip().split(',')
                lbe_permission = line_info[0] 
                permissions.setdefault(lbe_permission)
        lines = ''

        with open(filename.replace('.apk', '.csv'), 'w') as files:
            files.write('%s,%s\n' % ('package', package))
            files.write('%s,%s\n' % ('versionCode', versionCode))
            files.write('%s,%s\n' % ('md5', md5))
            last_lbe_permission = ''
            last_permission = ''
            for lbe_permission in gvmx.get_result():
                permission_dict = gvmx.get_result()[lbe_permission] 
                for permission in permission_dict:
                    for method in permission_dict[permission]:
                        result = [lbe_permission, permission, method]
                        files.write('%s\n' % ','.join(result))
                        lbe_permission = ' '
                        permission = ''
            for lbe_permission in gvmx.get_otherresult():
                permission_dict = gvmx.get_otherresult()[lbe_permission] 
                for permission in permission_dict:
                    for method in permission_dict[permission]:
                        result = [lbe_permission, permission, method]
                        files.write('%s\n' % ','.join(result))
                        lbe_permission = ' '
                        permission = ''

if __name__ == '__main__':
    dirName = sys.argv[1]

    processTime = time.time()
    processDate = datetime.datetime.utcnow().strftime('%Y-%m-%d')

#logFileName = os.path.join(dirName, 'log', 'log.%s' % processDate)
#logging.basicConfig(filename=logFileName, level=logging.DEBUG)

    for i in os.listdir(dirName):
        if i != 'log':
            i = os.path.join(dirName, i)
            if os.path.isdir(i):
                for j in os.listdir(i):
                    fileName = os.path.join(dirName, i, j)
                    if os.path.isfile(fileName):
                        try:
#if 1==1:
                            main(fileName)
                            logging.debug('Done')
                        except Exception as e:
#else:
                            logging.debug('___________________________________')
                            logging.debug('Time: %s' % str(processTime))
                            logging.debug(e)
    '''
    parser = OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)

    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)
    '''
