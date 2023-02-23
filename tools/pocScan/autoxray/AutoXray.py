#!/usr/bin/ python
# Author: @Givemefivw
# Descri: 调用Xray basic爬虫批量扫描
import re
import argparse
import os
import subprocess
import sys


def banner():
    banner = '''    

    Coding:
            @Givemefivw
    '''
    print(banner)


def autoxray(file):
    target = open(file, 'r', encoding='utf-8')
    lines = target.readlines()
    pattern = re.compile(r'^(https|http)://')
    for line in lines:
        try:
            if not pattern.match(line.strip()):
                url = "http://" + line.strip()
            else:
                url = line.strip()
            time = '%date:~0,4%%date:~5,2%%date:~8,2%0%time:~1,1%%time:~3,2%%time:~6,2%'
            os.system(".\\tools\\pocScan\\autoxray\\xray.exe webscan --basic-crawler {} --html-output "
                      "./results/AutoXray/ScanResult-{}.html".format(url,time))

        except Exception as e:
            pass
        except KeyboardInterrupt:
            sys.exit()
    target.close()


def main():
    parser = argparse.ArgumentParser(description='Auto Xray Help')
    parser.add_argument('-f', '--file', help='urlfile', default='')
    args = parser.parse_args()

    if args.file:
        file = args.file
        autoxray(file)


if __name__ == '__main__':
    banner()
    main()
