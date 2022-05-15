# coding=utf-8

import os
import sys
from this import d
import cmd2
import xlrd
import cmd2 as cmd
import lib.cmd.wanli
import config.config
import time
from random import randint
from rich.table import Table
from datetime import datetime
from rich.console import Console
from rich.highlighter import Highlighter
from os import system, name
from cmd2 import Cmd2ArgumentParser, with_argparser

console = Console()


class RainbowHighlighter(Highlighter):
    def highlight(self, text):
        for index in range(len(text)):
            text.stylize(f"color({randint(16, 255)})", index, index + 1)


rainbow = RainbowHighlighter()


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
        console.print('''
                _   _                
     /\        | | | |               
    /  \   _ __| |_| |__  _   _ _ __ 
   / /\ \ | '__| __| '_ \| | | | '__|
  / ____ \| |  | |_| | | | |_| | |   
 /_/    \_\_|   \__|_| |_|\__,_|_|''')
        console.print('''
                                        [green]---Info: Arsenal''')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        console.print('''
                _   _                
     /\        | | | |               
    /  \   _ __| |_| |__  _   _ _ __ 
   / /\ \ | '__| __| '_ \| | | | '__|
  / ____ \| |  | |_| | | | |_| | |   
 /_/    \_\_|   \__|_| |_|\__,_|_|''')
        console.print('''
                                        [green]---Info: Arsenal''')


CVE_list = []


def search(path, keyword):
    content = os.listdir(path)
    for each in content:
        each_path = path + os.sep + each
        if keyword in each:
            CVE_list.append(each_path)
        if os.path.isdir(each_path):
            search(each_path, keyword)


class newcmd(cmd.Cmd):
    prompt = config.config.TITLE  # 自定义交互式提示字符串

    # 自定义欢迎语
    console.print('''
                _   _                
     /\        | | | |               
    /  \   _ __| |_| |__  _   _ _ __ 
   / /\ \ | '__| __| '_ \| | | | '__|
  / ____ \| |  | |_| | | | |_| | |   
 /_/    \_\_|   \__|_| |_|\__,_|_|''')
    console.print('''
                                        [green]---Info: Arsenal''')

    # ----------------------------------------分割----------------------------------------
    # 定义-h内容

    collect_smap_parser = Cmd2ArgumentParser()
    collect_smap_parser.add_argument(
        "-i", nargs='?', help="smap资产端口信息扫描")
    collect_smap_parser.add_argument(
        "-f", nargs='?', help="smap文本资产端口信息扫描")

    @cmd2.with_argparser(collect_smap_parser)
    def do_collect_smap(self, args):
        '''smap资产端口信息扫描'''
        if args.i:
            ip = args.i
            lib.cmd.wanli.Collect.smap_single(ip)
        if args.f:
            file = args.f
            lib.cmd.wanli.Collect.smap_file(file)

    collect_finger_parser = Cmd2ArgumentParser()
    collect_finger_parser.add_argument(
        "-uf", nargs='?', help="Finger指纹对url文本批量指纹扫描, finger -uf url.txt")
    collect_finger_parser.add_argument(
        "-hf", nargs='?', help="Finger指纹对ip文本批量指纹扫描, finger -hf ip.txt")

    @cmd2.with_argparser(collect_finger_parser)
    def do_collect_finger(self, args):
        '''Finger指纹扫描工具对文本内容进行批量指纹扫描'''
        if args.uf:
            file = args.uf
            lib.cmd.wanli.Collect.finger_uf(file)
        if args.hf:
            file = args.hf
            lib.cmd.wanli.Collect.finger_hf(file)

    collect_subdomain_parser = Cmd2ArgumentParser()
    collect_subdomain_parser.add_argument(
        "-d", nargs='?', help="subfinder域名爆破,ksubdomain验证模式,finger指纹扫描,输出xlsx, domainbrute -d baidu.com")
    collect_subdomain_parser.add_argument(
        "-f", nargs='?', help="subfinder批量域名爆破,ksubdomain验证模式,finger指纹扫描,输出xlsx, domainbrute -f domain.txt")

    @cmd2.with_argparser(collect_subdomain_parser)
    def do_collect_subdomain(self, args):
        '''subfinder域名爆破,ksubdomain验证模式,finger指纹扫描,输出xlsx'''
        if args.d:
            domain = args.d
            lib.cmd.wanli.Collect.subdomain_single(domain)
        if args.f:
            file = args.f
            lib.cmd.wanli.Collect.subdomain_file(file)


    dirscan_dirsearch_parser = Cmd2ArgumentParser()
    dirscan_dirsearch_parser.add_argument(
        "-u", help="扫描单个Web应用敏感文件及敏感地址")

    @cmd2.with_argparser(dirscan_dirsearch_parser)
    def do_dirscan_dirsearch(self, args):
        '''dirsearch扫描网站目录'''
        if args.u:
            url = args.u
            lib.cmd.wanli.DirScan.dirsearch(url)

    dirscan_ffuf_parser = Cmd2ArgumentParser()
    dirscan_ffuf_parser.add_argument(
        "-u", nargs='?', help="ffuf FUZZ目录扫描, ffuf -u http://www.baidu.com/")

    @cmd2.with_argparser(dirscan_ffuf_parser)
    def do_dirscan_ffuf(self, args):
        '''ffuf Fuzz网站目录'''
        if args.u:
            url = args.u
            lib.cmd.wanli.DirScan.ffuf(url)

    ipscan_fscan_parser = Cmd2ArgumentParser()
    ipscan_fscan_parser.add_argument(
        "-i", nargs='?', help="fscan对ip进行扫描, fscan -i 192.168.1.1")
    ipscan_fscan_parser.add_argument(
        "-f", nargs='?', help="fscan对ip进行扫描, fscan -f ip.txt")

    @cmd2.with_argparser(ipscan_fscan_parser)
    def do_ipscan_fscan(self, args):
        '''fscan all mode 对ip进行扫描,输出txt'''
        if args.i:
            ip = args.i
            lib.cmd.wanli.IpScan.fscan_single(ip)
        if args.f:
            file = args.f
            lib.cmd.wanli.IpScan.fscan_file(file)

    ipscan_goon_parser = Cmd2ArgumentParser()
    ipscan_goon_parser.add_argument(
        "-f", nargs='?', help="goon自动对文件ip内容进行全部模块扫描,输出txt文件, goon -f ip.txt")

    @cmd2.with_argparser(ipscan_goon_parser)
    def do_ipscan_goon(self, args):
        '''goon all mode对文件ip内容扫描,输出txt'''
        if args.f:
            file = args.f
            lib.cmd.wanli.IpScan.goon(file)

    pocscan_xray_parser = Cmd2ArgumentParser()
    pocscan_xray_parser.add_argument(
        "-u", help="xray扫描单个目标,结果保存至html,xray http://www.baidu.com")

    @cmd2.with_argparser(pocscan_xray_parser)
    def do_pocscan_xray(self, args):
        '''xray basic-crawler漏扫,输出html'''
        if args.u:
            url = args.u
            lib.cmd.wanli.PocScan.xray(url)

    pocscan_vulmap_parser = Cmd2ArgumentParser()
    pocscan_vulmap_parser.add_argument(
        "-u", help="Vulmap漏扫,vulmap -u http://www.baidu.com/ ")
    pocscan_vulmap_parser.add_argument(
        "-f", help="Vulmap漏扫,vulmap -f url.txt")

    @cmd2.with_argparser(pocscan_vulmap_parser)
    def do_pocscan_vulmap(self, args):
        '''Vulmap漏洞扫描'''
        if args.u:
            url = args.u
            lib.cmd.wanli.PocScan.vulmap_single(url)
        if args.f:
            file = args.f
            lib.cmd.wanli.PocScan.vulmap_file(file)

    pocscan_xrad_parser = Cmd2ArgumentParser()
    pocscan_xrad_parser.add_argument(
        "-u", nargs='?', help="xray+rad 联动扫描, xrad http://baidu.com")

    @cmd2.with_argparser(pocscan_xrad_parser)
    def do_pocscan_xrad(self, args):
        '''xray+rad 联动扫描,输出html'''
        if args.u:
            url =args.u
            lib.cmd.wanli.PocScan.xrad(url)

    pocscan_autoxray_parser = Cmd2ArgumentParser()
    pocscan_autoxray_parser.add_argument(
        "-f", nargs='?', help="AutoXray批量漏扫,输出html报告, autoxray -f url.txt")

    @cmd2.with_argparser(pocscan_autoxray_parser)
    def do_pocscan_autoxray(self, args):
        '''AutoXray批量漏扫,输出html'''
        if args.f:
            file = args.f
            lib.cmd.wanli.PocScan.autoxray(file)

    pocscan_afrog_parser = Cmd2ArgumentParser()
    pocscan_afrog_parser.add_argument(
        "-u", nargs='?', help="afrog扫描工具进行漏扫,输出html报告, afrog -u http://www.baidu.com")
    pocscan_afrog_parser.add_argument(
        "-f", nargs='?', help="afrog扫描工具进行批量漏扫,输出html报告, afrog -f url.txt")

    @cmd2.with_argparser(pocscan_afrog_parser)
    def do_pocscan_afrog(self, args):
        '''afrog扫描工具进行批量漏扫,输出html报告'''
        if args.u:
            url = args.u
            lib.cmd.wanli.PocScan.afrog_single(url)
        if args.f:
            file = args.f
            lib.cmd.wanli.PocScan.afrog_file(file)

    # ----------------------------------------分割----------------------------------------
    # 定义-h内容
    pocscan_nuclei_parser = Cmd2ArgumentParser()
    pocscan_nuclei_parser.add_argument("-u", nargs='?', help="扫描单个目标")
    pocscan_nuclei_parser.add_argument("-f", nargs='?', help="指定文本进行批量漏洞扫描")
    pocscan_nuclei_parser.add_argument("-p", nargs='?', help="设置socks代理进行批量漏洞扫描")

    @cmd2.with_argparser(pocscan_nuclei_parser)
    def do_pocscan_nuclei(self, args):
        '''nuclei进行漏洞扫描'''
        if args.u:
            url = args.u
            lib.cmd.wanli.PocScan.nuclei_single(url)
        if args.f:
            file = args.f
            lib.cmd.wanli.PocScan.nuclei_file(file)
        if args.p:
            proxy = args.p
            lib.cmd.wanli.PocScan.nuclei_proxy(proxy)

    pocscan_pocsearch_parser = Cmd2ArgumentParser()
    pocscan_pocsearch_parser.add_argument(
        "number", nargs='?', help="自动查询CVE编号poc/exp在Github中的地址, pocsearch CVE-2020-2022")

    @cmd2.with_argparser(pocscan_pocsearch_parser)
    def do_pocscan_pocsearch(self, args):
        '''查询CVE编号poc/exp在Github中的地址'''
        if args.number:
            search = args.number
            system(config.config.PYTHON + " " + config.config.pocscan_Pocsearch + " -s {}".format(search))

    app_appinfoscanner_parser = Cmd2ArgumentParser()
    app_appinfoscanner_parser.add_argument(
        "-i", nargs='?', help="AppInfoScanner移动端信息收集")

    @cmd2.with_argparser(app_appinfoscanner_parser)
    def do_app_appinfoscanner(self, args):
        '''AppInfoScanner移动端信息收集'''
        if args.i:
            apk = args.i
            lib.cmd.wanli.App.appinfoscanner(apk)

    app_fridaskeleton_parser = Cmd2ArgumentParser()
    app_fridaskeleton_parser.add_argument(
        "-p", nargs='?', help="frida-skeleton Bypass SSLPinning")

    @cmd2.with_argparser(app_fridaskeleton_parser)
    def do_app_fridaskeleton(self, args):
        '''frida-skeleton Bypass SSLPinning'''
        if args.p:
            package = args.p
            lib.cmd.wanli.App.fridaskeleton(package)

    rotateproxy_parser = Cmd2ArgumentParser()
    rotateproxy_parser.add_argument(
        "-r", nargs='?', help="RotateProxy find Socks5,-r 1 cannot bypass gfw,-r 2 bypass gfw")

    @cmd2.with_argparser(rotateproxy_parser)
    def do_rotateproxy(self, args):
        '''RotateProxy find free Socks5,default port 1080'''
        if args.r:
            region = args.r
            lib.cmd.wanli.Proxy.rotateproxy(region)

    cms_check_parser = Cmd2ArgumentParser()
    cms_check_parser.add_argument(
        "-a", nargs='?', help="-a shiro/struts/thinkphp/weblogic/tongda")

    @cmd2.with_argparser(cms_check_parser)
    def do_cms_check(self, args):
        '''shiro/struts/thinkphp/weblogic/tongda PoCScan/Exploit'''
        if args.a == 'shiro':
            lib.cmd.wanli.Exploit.shiro()
        if args.a == 'struts':
            lib.cmd.wanli.Exploit.struts2()
        if args.a == 'thinkphp':
            lib.cmd.wanli.Exploit.thinkphp()
        if args.a == 'weblogic':
            lib.cmd.wanli.Exploit.weblogic()
        if args.a == 'tongda':
            lib.cmd.wanli.Exploit.tongda()




    # ----------------------------------------分割----------------------------------------
    # 当无法识别输入的command时该方法；
    def default(self, line):
        console.print(
            "[bold red][-][/bold red] [bold cyan]The current command input error, please enter again.[/bold cyan]")

    # ----------------------------------------分割----------------------------------------
    # 退出不报错
    def do_EOF(self, line):
        return True
        pass

    # ----------------------------------------分割----------------------------------------
    # 清空
    def do_clear(self, arg):
        '''清空屏幕'''
        clear()

    # ----------------------------------------分割----------------------------------------
    # 退出
    def do_exit(self, arg):
        '''退出工具'''
        sys.exit(1)

    def __init__(self):
        super().__init__()
        self.hidden_commands.append('EOF')
        self.hidden_commands.append('alias')
        self.hidden_commands.append('edit')
        self.hidden_commands.append('quit')
        self.hidden_commands.append('history')
        self.hidden_commands.append('macro')
        self.hidden_commands.append('run_pyscript')
        self.hidden_commands.append('run_script')
        self.hidden_commands.append('set')
        self.hidden_commands.append('shell')
        self.hidden_commands.append('shortcuts')


if __name__ == '__main__':
    clear()
    newcmd().cmdloop()
