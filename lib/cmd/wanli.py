import configs.config
import time
import re
import random
from os import system
from datetime import datetime
from rich.console import Console



console = Console()
datatime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


class Collect():
    @staticmethod
    def subdomain_single(domain):
        cmd = f''
        cmd += f'{configs.config.collect_subfinder} -d {domain} -silent | {configs.config.collect_ksubdomain} -verify -silent -o {domain}.txt'
        system(cmd)

    @staticmethod
    def subdomain_file(file,name):
        cmd = f''
        cmd += f'{configs.config.collect_subfinder} -dL {file} -silent | {configs.config.collect_ksubdomain} -verify -silent -o ./results/domainbrute/{name}.txt'
        system(cmd)

    @staticmethod
    def finger_uf(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.collect_finger} -f {file}'
        system(cmd)

    @staticmethod
    def finger_hf(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.collect_finger} -if {file}'
        system(cmd)


    @staticmethod
    def naabu(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.collect_naabu} -l {file} -ping -pf ./tools/collect/naabu/ports.txt'
        system(cmd)

    @staticmethod
    def httpx(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.collect_httpx} -stats -title -tech-detect -mc 200,302,403,401 -fr -si 20 -td -random-agent -l {file}'
        system(cmd)

    @staticmethod
    def httpx_savejson(file,name):
        cmd = f''
        cmd += f'start cmd /k {configs.config.collect_httpx} -stats -title -tech-detect -mc 200,302,403,401 -fr -si 20 -td -random-agent -csv -o '
        cmd += f'./results/httpx/{name}.csv -l {file}'
        system(cmd)

    @staticmethod
    def srcScan(file,name):
        cmd = f''
        cmd += f'{configs.config.collect_subfinder} -dL {file} -silent | {configs.config.collect_ksubdomain} -verify -silent | '
        cmd += f'{configs.config.collect_naabu} -ping -pf ./tools/collect/naabu/ports.txt -silent | '
        cmd += f'{configs.config.collect_httpx} -stats -title -tech-detect -mc 200,302,403,401 -fr -si 20 -td -random-agent -csv -o ./results/httpx/{name}.csv'
        system(cmd)

        
class DirScan():
    @staticmethod
    def dirsearch(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.dirscan_dirsearch} -u {url} '
        cmd += f'-t 50 --random-agent -R 3 --recursion-status 200-403 --timeout 3 --retries 1'
        system(cmd)


    @staticmethod
    def ffuf(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.dirscan_ffuf} -w ./tools/dirScan/ffuf/diclist/dicc.txt -u '
        cmd += f'{url} FUZZ -t 50 -c -v -mc 200,401,302 -timeout 5'
        system(cmd)

    @staticmethod
    def urlFinder(url,mode):
        cmd = f''
        cmd += f'start cmd /k {configs.config.dirscan_urlFinder} -u {url} -m {mode}'
        system(cmd)

    @staticmethod
    def scout(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.dirscan_scout} url {url} -x -s -c 200,401,201,302,403 -k'
        system(cmd)

    @staticmethod
    def katana_single(url,name):
        cmd = f''
        cmd += f'start cmd /k {configs.config.dirscan_katana} -u {url} -jc -d 3 -o ./results/katana/{name}.txt'       
        system(cmd)

    @staticmethod
    def katana_file(file,name):
        cmd = f''
        cmd += f'start cmd /k {configs.config.dirscan_katana} -list {file} -jc -d 3 -o ./results/katana/{name}.txt'
        system(cmd)

    @staticmethod
    def antColony_single(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.dirscan_Antcolony} -u {url} -j -p'
        system(cmd)

    @staticmethod
    def antColony_file(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.dirscan_Antcolony} -t {file} -j -p'
        system(cmd)


class IpScan():
    @staticmethod
    def fscan_single(ip):
        cmd = f''
        cmd += f'start cmd /k {configs.config.ipscan_fscan} -h {ip} -ping -portf ./tools/ipScan/fscan/ports.txt -br 20 -no'
        system(cmd)


    @staticmethod
    def fscan_file(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.ipscan_fscan} -hf {file} -ping -portf ./tools/ipScan/fscan/ports.txt -br 20 -no '
        cmd += f'-o ./results/fscan/{datatime}.txt'
        system(cmd)


class PocScan():
    @staticmethod
    def xray(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.pocscan_xray} webscan --browser-crawler {url} --html-output ./results/xray/report_{datatime}.html'
        system(cmd)

    @staticmethod
    def autoxray(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.pocscan_autoxray} -f {file}'
        system(cmd)

    @staticmethod
    def rad(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.dirscan_rad} -t {url} --wait-login'
        system(cmd)

    @staticmethod
    def xrad(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.pocscan_xray} webscan --listen 127.0.0.1:7799 --html-output ./results/xrad/report_{datatime}.html'
        system(cmd)
        time.sleep(5)

        system(f'start cmd /k {configs.config.dirscan_rad} -t {url} -http-proxy 127.0.0.1:7799')


    @staticmethod
    def xrad_file(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.pocscan_xray} webscan --listen 127.0.0.1:7799 --html-output ./results/xrad/report_{datatime}.html'
        system(cmd)

        time.sleep(5)
        target = open(file, 'r', encoding='utf-8')
        lines = target.readlines()
        pattern = re.compile(r'^(https|http)://')
        for line in lines:
            try:
                if not pattern.match(line.strip()):
                    url = "http://" + line.strip()
                else:
                    url = line.strip()
                system(f'{configs.config.dirscan_rad} -t {url} -http-proxy 127.0.0.1:7799')
            except Exception as e:
                pass
        target.close()



    @staticmethod
    def vulmap_single(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.pocscan_vulmap} -u {url}'
        system(cmd)

    @staticmethod
    def vulmap_file(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.pocscan_vulmap} -f {file}'
        system(cmd)

    @staticmethod
    def nuclei_single(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.pocscan_nuclei} -u {url} '
        cmd += f'-s low,medium,high,critical -rate-limit 100 -bulk-size 25 -concurrency 25 -stats -si 10 -retries 3'
        system(f'{configs.config.pocscan_nuclei} -ut')
        system(cmd)

    @staticmethod
    def nuclei_file(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.pocscan_nuclei} -l {file} '
        cmd += f'-s medium,high,critical -rate-limit 100 -bulk-size 25 -concurrency 25 -stats -si 300 -retries 3'
        system(f'{configs.config.pocscan_nuclei} -ut')
        system(cmd)

    @staticmethod
    def afrog_single(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.pocscan_afrog} --nf -t {url}'
        system(f'{configs.config.pocscan_afrog} --up')
        system(cmd)

    @staticmethod
    def afrog_file(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.pocscan_afrog} --nf -T {file}'
        system(f'{configs.config.pocscan_afrog} --up')
        system(cmd)

    @staticmethod
    def waterexp_single(url):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.pocscan_waterExp} -u {url}'
        system(cmd)

    @staticmethod
    def waterexp_file(file):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.pocscan_waterExp} -f {file}'
        system(cmd)

    @staticmethod
    def xssScan_single(url):
        cmd = f''
        cmd += f'{configs.config.dirscan_katana} -u {url} -jc -f qurl -c 50 -kf robotstxt,sitemapxml -silent | '
        cmd += f'{configs.config.pocscan_dalfox} pipe --skip-bav'
        system(cmd)

    @staticmethod
    def xssScan_file(file):
        cmd = f''
        cmd += f'{configs.config.dirscan_katana} -list {file} -jc -f qurl -c 50 -kf robotstxt,sitemapxml -silent | '
        cmd += f'{configs.config.pocscan_dalfox} pipe --skip-bav'
        system(cmd)

    @staticmethod
    def sqliScan_single(url):
        cmd = f''
        cmd += f'{configs.config.dirscan_katana} -u {url} -jc -f qurl -c 50 -kf robotstxt,sitemapxml -silent | '
        cmd += f'{configs.config.PYTHON} {configs.config.pocscan_sqlmap} --batch --random-agent --level 4'
        system(cmd)
    
    @staticmethod
    def sqliScan_file(file):
        cmd = f''
        cmd += f'{configs.config.dirscan_katana} -list {file} -jc -f qurl -c 50 -kf robotstxt,sitemapxml -silent | '
        cmd += f'{configs.config.PYTHON} {configs.config.pocscan_sqlmap} --batch --random-agent --level 4'
        system(cmd)
        

class App():
    @staticmethod
    def appinfoscanner(apk):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.app_appinfoscanner} android -i {apk} -o ./results/appinfoScanner/'
        system(cmd)


class Proxy():
    @staticmethod
    def rotateproxy(region):
        cmd = f''
        cmd += f'start cmd /k {configs.config.rotateproxy} -email  -token   -region '
        cmd += f'-rule "protocol==\"socks5\" && \"Version:5 Method:No Authentication(0x00)\" && after=\"2023-01-01\" && country=\"CN\""'
        system(cmd)

class Brute():
    @staticmethod
    def brute_blaster(username):
        cmd = f''
        cmd += f'start cmd /k {configs.config.PYTHON} {configs.config.brute_blaster_server} -a admin:123 -p 8999'
        system(cmd)
        time.sleep(2)

        system(f'start cmd /k {configs.config.brute_blaster} -c ./tools/brute/blaster/conf.yaml -u username -p ./tools/brute/blaster/password.txt')


class Cms():

    @staticmethod
    def shiro():
        cmd = f''
        cmd += f'start cmd /k java -jar {configs.config.cms_shiro}'
        system(cmd)

    @staticmethod
    def struts2():
        cmd = f''
        cmd += f'start cmd /k java -jar {configs.config.cms_struts}'
        system(cmd)

    @staticmethod
    def thinkphp():
        cmd = f''
        cmd += f'start cmd /k java -jar {configs.config.cms_tninkphp}'
        system(cmd)

    @staticmethod
    def weblogic():
        cmd = f''
        cmd += f'start cmd /k java -jar {configs.config.cms_weblogic}'
        system(cmd)

    @staticmethod
    def tongda():
        cmd = f''
        cmd += f'start cmd /k java -jar {configs.config.cms_tongda}'
        system(cmd)

class Attack():
    @staticmethod
    def heapdump(file):
        cmd = f''
        cmd += f'start cmd /k java -jar {configs.config.attack_heapdump} {file}'
        system(cmd)
