import imp
import os
import sys
import xlrd

from django import conf
import config.config
import time
from os import system
from datetime import datetime
from rich.console import Console

console = Console()
datatime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


class Collect():
    @staticmethod
    def subdomain_single(domain):
        system(
            config.config.collect_subfinder + r" -d " + domain + " -recursive -o ./results/domainbrute/{}.txt".format(
                domain))
        system(config.config.collect_ksubdomain + " -verify -f ./results/domainbrute/{}.txt -silent -o {}.txt".format(
            domain, domain))
        system(config.config.PYTHON + " " + config.config.collect_finger + " -f {}.txt".format(domain) + " -o xlsx")

    def subdomain_file(file):
        system(config.config.collect_subfinder + r" -dL " + file + " -recursive -o ./results/domainbrute/{}.txt".format(
            datatime))
        system(config.config.collect_ksubdomain + " -verify -f ./results/domainbrute/{}.txt -silent -o {}.txt".format(
            datatime, datatime))
        system(config.config.PYTHON + " " + config.config.collect_finger + " -f {}.txt".format(datatime) + " -o xlsx")

    @staticmethod
    def finger_uf(file):
        system(
            r"start cmd /k " + config.config.PYTHON + " " + config.config.collect_finger + " " + r"-f" + " " + file + r" -o xlsx")

    @staticmethod
    def finger_hf(file):
        system(
            r"start cmd /k " + config.config.PYTHON + " " + config.config.collect_finger + " " + r"-if" + " " + file + r" -o xlsx")

    @staticmethod
    def smap_single(ip):
        system(r"start cmd /k " + config.config.collect_smap + " " + ip)

    @staticmethod
    def smap_file(file):
        system(config.config.collect_smap + " -iL " + file + " -oX ./results/smap/{}.xml".format(datatime))
        system(
            r"start cmd /k " + config.config.collect_nmapformatter + " md  ./results/smap/{}.xml --md-skip-summary -f ./results/smap/{}.md".format(
                datatime, datatime))


class DirScan():
    @staticmethod
    def dirsearch(url):
        system(r"start cmd /k " + config.config.PYTHON + " " + config.config.dirscan_dirsearch +
               " -u " + url + " -t 50 --random-agent -i 200,302,401")

    @staticmethod
    def ffuf(url):
        system(
            r"start cmd /k " + config.config.dirscan_ffuf + " -w ./tools/dirScan/ffuf/diclist/dicc.txt -u " +
            url + "FUZZ -t 50 -c -v -mc 200,401,302 -timeout 5")


class IpScan():
    @staticmethod
    def fscan_single(ip):
        system(
            r"start cmd /k " + config.config.ipscan_fscan + r" -h " + ip + " -o ./results/fscan/{}.txt".format(
                datatime))

    @staticmethod
    def fscan_file(file):
        system(
            r"start cmd /k " + config.config.ipscan_fscan + r" -hf " + file + " -o ./results/fscan/{}.txt".format(
                datatime))

    @staticmethod
    def goon(file):
        system(
            r"start cmd /k " + config.config.ipscan_goon + " -ifile " + file + " -ofile ./results/goon/{}.txt".format(
                datatime))


class PocScan():
    @staticmethod
    def xray(url):
        system(r"start cmd /k " + config.config.pocscan_xray + r" webscan --basic-crawler " + url +
               r" --html-output ./results/xray/Xray-{}.html".format(datatime))

    @staticmethod
    def autoxray(file):
        system(
            r"start cmd /k " + config.config.PYTHON + " " + config.config.pocscan_autoxray + " " + r"-f" + " " + file)

    @staticmethod
    def xrad(url):
        system(r"start cmd /k " + config.config.pocscan_xray +
               r" webscan --listen 127.0.0.1:7799 --html-output ./results/xrad/Xrad-{}.html".format(datatime))
        time.sleep(5)
        if url.find('http') == -1:
            url = 'http://' + url + '/'
        else:
            url = url
        system(r"start cmd /k " + config.config.pocscan_rad + r" -t {} -http-proxy 127.0.0.1:7799".format(url))

    @staticmethod
    def vulmap_single(url):
        system(r"start cmd /k " + config.config.PYTHON + " " + config.config.pocscan_vulmap + " -u " + url)

    @staticmethod
    def vulmap_file(file):
        system(r"start cmd /k " + config.config.PYTHON + " " + config.config.pocscan_vulmap + " -f " + file)

    @staticmethod
    def nuclei_single(url):
        system(config.config.pocscan_nuclei + " -ut && " + config.config.pocscan_nuclei + " -update")
        system(r"start cmd /k " + config.config.pocscan_nuclei + r" -u " + url +
               " -s low,medium,high,critical -rate-limit 100 -bulk-size 25 "
               "-concurrency 25 -stats -si 10 -retries 3")

    @staticmethod
    def nuclei_file(file):
        system(config.config.pocscan_nuclei + " -ut && " + config.config.pocscan_nuclei + " -update")
        system(r"start cmd /k " + config.config.pocscan_nuclei + r" -l " + file +
               " -s medium,high,critical -rate-limit 100 -bulk-size 25 "
               "-concurrency 25 -stats -si 300 -retries 3")

    @staticmethod
    def nuclei_proxy(proxy):
        system(config.config.pocscan_nuclei + " -ut && " + config.config.pocscan_nuclei + " -update")
        system(r"start cmd /k " + config.config.pocscan_nuclei + r" -l D:\\Arsenal\\WanLi\\url.txt "
               r" -p {}:1080 -s medium,high,critical -rate-limit 100 -bulk-size 25 "
                "-concurrency 25 -stats -si 300 -retries 3".format(proxy))

    @staticmethod
    def afrog_single(url):
        system(r"start cmd /k " + config.config.pocscan_afrog + " -t " + url + " -o {}.html".format(datatime))

    @staticmethod
    def afrog_file(file):
        system(r"start cmd /k " + config.config.pocscan_afrog + " -T " + file + " -o {}.html".format(datatime))


class App():
    @staticmethod
    def appinfoscanner(apk):
        system(
            r"start cmd /k " + config.config.PYTHON + " " + config.config.app_appinfoscanner + " android -i " + apk + " -o ./results/appinfoScanner/")

    @staticmethod
    def fridaskeleton(package):
        system(r"start cmd /k " + config.config.PYTHON + " " + config.config.app_fridaskeleton + " " + package)


class Proxy():
    @staticmethod

    def rotateproxy(region):
        system(
            r"start cmd /k " + config.config.rotateproxy + " -email 987302959@qq.com -token d682d712a748eccef1808b43520a732c  -region " + region)


class Exploit():

    @staticmethod
    def shiro():
        system(r"start cmd /k " + "java -jar " + config.config.cms_shiro)

    @staticmethod
    def struts2():
        system(r"start cmd /k " + "java -jar " + config.config.cms_struts)

    @staticmethod
    def thinkphp():
        system(r"start cmd /k " + "java -jar " + config.config.cms_tninkphp)

    @staticmethod
    def weblogic():
        system(r"start cmd /k " + "java -jar " + config.config.cms_weblogic)

    @staticmethod
    def tongda():
        system(r"start cmd /k " + "java -jar " + config.config.cms_tongda)



