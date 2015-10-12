#!/usr/bin/python
import argparse
import os
import sys
import re
import time
import codecs


day = 24 * 60 * 60
jenkins_fmt = '%Y-%m-%d_%H-%M-%S'


def main():
    '''
    Argument1: directory for searching crash report, default is cwd
    Argument2: starting timestamp, default is yesterday
    Argument3: ending timestamp, default is now
    '''
    dirpath = '.'
    today = time.localtime()
    yesterday = time.localtime(time.time() - day)
    start_time = yesterday
    end_time = today
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help='starting timestamp, default is yesterday\
            time fmt: YYYY-MM-DD_hh-mm-ss')
    parser.add_argument("-d", "--dir", help='directory for searching crash report, default is cwd')
    parser.add_argument("-e", "--end", help="ending timestamp, default is now")
    args = parser.parse_args()
    if args.start:
        start_time = time.strptime(args.start, jenkins_fmt)
    if args.end:
        end_time = time.strptime(args.end, jenkins_fmt)
    if args.dir:
        if not os.path.isdir(args.dir):
            sys.stderr.write("Can't find " + args.dir)
            sys.exit(1)
        dirpath = args.dir
    cfs = filter_crash_files(dirpath, start_time, end_time)
    print("==== start of parsing crash report ====")
    for cf in cfs:
        cfh = codecs.open(cf, encoding='UTF-8')
        print("CrashReportCLI: " + cfh.read())
    print("==== end of parsing crash report ====")


def filter_crash_files(dirpath, start_time, end_time):
    cfs = filter(os.path.isfile, [os.path.join(dirpath, f) for f in os.listdir(dirpath)])
    start_time = time.gmtime(time.mktime(start_time))
    end_time = time.gmtime(time.mktime(end_time))
    ret = []
    for cf in cfs:
        m = re.search('_([\d-]*)\+0000', cf)
        if m:
            timestamp = time.strptime(m.group(1), '%Y-%m-%d-%H-%M-%S')
            if timestamp > start_time and timestamp < end_time:
                ret.append(cf)
    return ret


if '__main__' == __name__:
    main()
