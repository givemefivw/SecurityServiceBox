# coding=utf-8

import os
import sys
from this import d
import cmd2
import xlrd
import cmd2 as cmd
import lib.cmd.wanli
import configs.config
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




class newcmd(cmd.Cmd):
    prompt = configs.config.TITLE  # 自定义交互式提示字符串

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

    # ----------------------------------------信息收集----------------------------------------
    # 定义-h内容

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
        "-d", nargs='?', help="subfinder域名爆破,ksubdomain验证模式, domainbrute -d baidu.com")
    collect_subdomain_parser.add_argument(
        "-f", nargs='?', help="subfinder批量域名爆破,ksubdomain验证模式, domainbrute -f domain.txt")
    collect_subdomain_parser.add_argument(
        "-o", nargs='?', help="-f模式指定爆破域名结果输出文本名称")

    @cmd2.with_argparser(collect_subdomain_parser)
    def do_collect_subdomain(self, args):
        '''subfinder域名爆破,ksubdomain验证模式,批量模式下指定爆破域名结果输出文本名称'''
        if args.d:
            domain = args.d
            lib.cmd.wanli.Collect.subdomain_single(domain)
        if args.f:
            if args.o:
                file = args.f
                name = args.o
                lib.cmd.wanli.Collect.subdomain_file(file,name)

    collect_naabu_parser = Cmd2ArgumentParser()
    collect_naabu_parser.add_argument(
        "-f", nargs='?', help="naabu端口扫描 naabu -f ip.txt")

    @cmd2.with_argparser(collect_naabu_parser)
    def do_collect_naabu(self, args):
        '''naabu端口扫描 naabu -f ip.txt'''
        if args.f:
            file = args.f
            lib.cmd.wanli.Collect.naabu(file)

    collect_httpx_parser = Cmd2ArgumentParser()
    collect_httpx_parser.add_argument(
        "-nf", nargs='?', help="httpx 扫描存活资产,不保存文件,httpx -nf url.txt")
    collect_httpx_parser.add_argument(
        "-sf", nargs='?', help="httpx 扫描存活资产,保存到json文件,httpx -sf url.txt -o report.json")
    collect_httpx_parser.add_argument(
        "-o", nargs='?', help="httpx 对json文件进行url/finalurl梳理,httpx -o report.json")

    @cmd2.with_argparser(collect_httpx_parser)
    def do_collect_httpx(self, args):
        '''httpx 扫描存活资产,httpx -f url.txt'''
        if args.nf:
            file = args.nf
            lib.cmd.wanli.Collect.httpx(file)
        if args.sf:
            if args.o:
                file = args.sf
                name = args.o
                lib.cmd.wanli.Collect.httpx_savejson(file,name)

    collect_srcScan_parser = Cmd2ArgumentParser()
    collect_srcScan_parser.add_argument(
        "-f", nargs='?', help="subfinder&ksubdomain&naabu&httpx&httpxRecover结合梳理域名资产,srcScan -f domain.txt -o report")
    collect_srcScan_parser.add_argument(
        "-o", nargs='?', help="subfinder&ksubdomain&naabu&httpx&httpxRecover结合梳理域名资产,srcScan -f domain.txt -o report")

    @cmd2.with_argparser(collect_srcScan_parser)
    def do_collect_srcScan(self, args):
        '''subfinder&ksubdomain&naabu&httpx&httpxRecover,srcScan -f domain.txt -o report'''
        if args.f:
            if args.o:
                file = args.f
                name = args.o
                lib.cmd.wanli.Collect.srcScan(file,name)

    # ----------------------------------------目录扫描----------------------------------------

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

    dirscan_scout_parser = Cmd2ArgumentParser()
    dirscan_scout_parser.add_argument(
        "-u", nargs='?', help="scout url Fuzzing,scout -u http://www.baidu.com/")

    @cmd2.with_argparser(dirscan_scout_parser)
    def do_dirscan_scout(self, args):
        '''scout url Fuzzing,scout -u http://www.baidu.com/'''
        if args.u:
            url = args.u
            lib.cmd.wanli.DirScan.scout(url)

    dirscan_urlFinder_parser = Cmd2ArgumentParser()
    dirscan_urlFinder_parser.add_argument(
        "-u", nargs='?', help="urlFinder Scan Js File")
    dirscan_urlFinder_parser.add_argument(
        "-m", nargs='?', help="1 is normal,2 is thorough")

    @cmd2.with_argparser(dirscan_urlFinder_parser)
    def do_dirscan_urlFinder(self, args):
        '''urlFinder Scan Js File'''
        if args.u:
            if args.m:
                url = args.u
                mode = args.m
                lib.cmd.wanli.DirScan.urlFinder(url,mode)

    dirscan_katana_parser = Cmd2ArgumentParser()
    dirscan_katana_parser.add_argument(
        "-u", nargs='?', help="katana 爬虫扫描")
    dirscan_katana_parser.add_argument(
        "-f", nargs='?', help="katana 批量爬虫")
    dirscan_katana_parser.add_argument(
        "-o", nargs='?', help="katana 爬虫输出")

    @cmd2.with_argparser(dirscan_katana_parser)
    def do_dirscan_katana(self, args):
        '''katana 爬虫扫描网站'''
        if args.u:
            if args.o:
                url = args.u
                name = args.o
                lib.cmd.wanli.DirScan.katana_single(url,name)
        if args.f:
            if args.o:
                file = args.f
                name = args.o
                lib.cmd.wanli.DirScan.katana_file(file,name)

    dirscan_antcolony_parser = Cmd2ArgumentParser()
    dirscan_antcolony_parser.add_argument(
        "-u", nargs='?', help="antcolony 网站Js目录扫描")
    dirscan_antcolony_parser.add_argument(
        "-f", nargs='?', help="antcolony 网站Js目录扫描")

    @cmd2.with_argparser(dirscan_antcolony_parser)
    def do_dirscan_antcolony(self, args):
        '''antcolony 网站Js目录扫描'''
        if args.u:
            url = args.u
            lib.cmd.wanli.DirScan.antColony_single(url)
        if args.f:
            file = args.f
            lib.cmd.wanli.DirScan.antColony_file(file)

    # ----------------------------------------IP自动化扫描----------------------------------------

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


    # ----------------------------------------PoC扫描----------------------------------------


    pocscan_xray_parser = Cmd2ArgumentParser()
    pocscan_xray_parser.add_argument(
        "-u", help="xray扫描单个目标,结果保存至html,xray http://www.baidu.com")

    @cmd2.with_argparser(pocscan_xray_parser)
    def do_pocscan_xray(self, args):
        '''xray basic-crawler漏扫,输出html'''
        if args.u:
            url = args.u
            lib.cmd.wanli.PocScan.xray(url)

    pocscan_rad_parser = Cmd2ArgumentParser()
    pocscan_rad_parser.add_argument("-u", help="rad浏览器爬虫登录爬取")

    @cmd2.with_argparser(pocscan_rad_parser)
    def do_pocscan_rad(self, args):
        '''rad浏览器爬虫登录爬取'''
        if args.u:
            url = args.u
            lib.cmd.wanli.PocScan.rad(url)

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
    pocscan_xrad_parser.add_argument(
        "-f", nargs='?', help="xray+rad 联动扫描, xrad -f url.txt")

    @cmd2.with_argparser(pocscan_xrad_parser)
    def do_pocscan_xrad(self, args):
        '''xray+rad 联动扫描,输出html'''
        if args.u:
            url =args.u
            lib.cmd.wanli.PocScan.xrad(url)
        if args.f:
            file = args.f
            lib.cmd.wanli.PocScan.xrad_file(file)

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


    pocscan_nuclei_parser = Cmd2ArgumentParser()
    pocscan_nuclei_parser.add_argument("-u", nargs='?', help="扫描单个目标")
    pocscan_nuclei_parser.add_argument("-f", nargs='?', help="指定文本进行批量漏洞扫描")

    @cmd2.with_argparser(pocscan_nuclei_parser)
    def do_pocscan_nuclei(self, args):
        '''nuclei进行漏洞扫描'''
        if args.u:
            url = args.u
            lib.cmd.wanli.PocScan.nuclei_single(url)
        if args.f:
            file = args.f
            lib.cmd.wanli.PocScan.nuclei_file(file)

    pocscan_xssScan_parser = Cmd2ArgumentParser()
    pocscan_xssScan_parser.add_argument("-u", nargs='?', help="katana + dalfox xssScan 扫描单个目标")
    pocscan_xssScan_parser.add_argument("-f", nargs='?', help="katana + dalfox xssScan 指定文本进行批量XSS扫描")

    @cmd2.with_argparser(pocscan_xssScan_parser)
    def do_pocscan_xssScan(self, args):
        '''katana + dalfox xssScan'''
        if args.u:
            url = args.u
            lib.cmd.wanli.PocScan.xssScan_single(url)
        if args.f:
            file = args.f
            lib.cmd.wanli.PocScan.xssScan_file(file)

    pocscan_sqliScan_parser = Cmd2ArgumentParser()
    pocscan_sqliScan_parser.add_argument("-u", nargs='?', help="katana + sqlmap sqliScan 扫描单个目标")
    pocscan_sqliScan_parser.add_argument("-f", nargs='?', help="katana + sqlmap sqliScan 指定文本进行批量XSS扫描")

    @cmd2.with_argparser(pocscan_sqliScan_parser)
    def do_pocscan_sqliScan(self, args):
        '''katana + sqlmap sqliScan'''
        if args.u:
            url = args.u
            lib.cmd.wanli.PocScan.sqliScan_single(url)
        if args.f:
            file = args.f
            lib.cmd.wanli.PocScan.sqliScan_file(file)

    pocscan_waterexp_parser = Cmd2ArgumentParser()
    pocscan_waterexp_parser.add_argument("-u", nargs='?', help="WaterEXP Single Target")
    pocscan_waterexp_parser.add_argument("-f", nargs='?', help="WaterEXP File Target")

    @cmd2.with_argparser(pocscan_waterexp_parser)
    def do_pocscan_waterexp(self, args):
        '''WaterEXP进行poc扫描'''
        if args.u:
            url = args.u
            lib.cmd.wanli.PocScan.waterexp_single(url)
        if args.f:
            file = args.f
            lib.cmd.wanli.PocScan.waterexp_file(file)

    pocscan_pocsearch_parser = Cmd2ArgumentParser()
    pocscan_pocsearch_parser.add_argument(
        "number", nargs='?', help="自动查询CVE编号poc/exp在Github中的地址, pocsearch CVE-2020-2022")

    @cmd2.with_argparser(pocscan_pocsearch_parser)
    def do_pocscan_pocsearch(self, args):
        '''查询CVE编号poc/exp在Github中的地址'''
        if args.number:
            search = args.number
            system(configs.config.PYTHON + " " + configs.config.pocscan_Pocsearch + " -s {}".format(search))

    # ----------------------------------------App信息收集----------------------------------------

    app_appinfoscanner_parser = Cmd2ArgumentParser()
    app_appinfoscanner_parser.add_argument(
        "-i", nargs='?', help="AppInfoScanner移动端信息收集")

    @cmd2.with_argparser(app_appinfoscanner_parser)
    def do_app_appinfoscanner(self, args):
        '''AppInfoScanner移动端信息收集'''
        if args.i:
            apk = args.i
            lib.cmd.wanli.App.appinfoscanner(apk)

    # ----------------------------------------暴力破解----------------------------------------

    brute_blaster_parser = Cmd2ArgumentParser()
    brute_blaster_parser.add_argument(
        "-u", nargs='?', help="用户名字典")

    @cmd2.with_argparser(brute_blaster_parser)
    def do_brute_blaster(self, args):
        '''blaster 登录页面爆破'''
        if args.u:
            username = args.u
            lib.cmd.wanli.Brute.brute_blaster(username)

    # ----------------------------------------socks代理工具----------------------------------------

    rotateproxy_parser = Cmd2ArgumentParser()
    rotateproxy_parser.add_argument(
        "-r", nargs='?', help="RotateProxy find Socks5 Agent,-r 1 cannot bypass gfw,-r 2 bypass gfw")

    @cmd2.with_argparser(rotateproxy_parser)
    def do_rotateproxy(self, args):
        '''RotateProxy find free Socks5 Agent'''
        if args.r:
            region = args.r
            lib.cmd.wanli.Proxy.rotateproxy(region)

    # ----------------------------------------中间件专项利用----------------------------------------

    cms_check_parser = Cmd2ArgumentParser()
    cms_check_parser.add_argument(
        "-a", nargs='?', help="-a shiro/struts/thinkphp/weblogic/tongda")

    @cmd2.with_argparser(cms_check_parser)
    def do_cms_check(self, args):
        '''shiro/struts/thinkphp/weblogic/tongda PoCScan/Exploit'''
        if args.a == 'shiro':
            lib.cmd.wanli.Cms.shiro()
        if args.a == 'struts':
            lib.cmd.wanli.Cms.struts2()
        if args.a == 'thinkphp':
            lib.cmd.wanli.Cms.thinkphp()
        if args.a == 'weblogic':
            lib.cmd.wanli.Cms.weblogic()
        if args.a == 'tongda':
            lib.cmd.wanli.Cms.tongda()

    # ----------------------------------------漏洞利用----------------------------------------

    attack_heapdump_parser = Cmd2ArgumentParser()
    attack_heapdump_parser.add_argument(
        "-f", nargs='?', help="Spring heapdump文件泄露利用")

    @cmd2.with_argparser(attack_heapdump_parser)
    def do_attack_heapdump(self, args):
        '''Spring heapdump文件泄露利用'''
        if args.f:
            file = args.f
            lib.cmd.wanli.Attack.heapdump(file)




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
