#!/usr/bin python3
import concurrent.futures
import re
import time
import subprocess

httpx               = 'https://github.com/projectdiscovery/httpx'
naabu               = 'https://github.com/projectdiscovery/naabu'
subfinder           = 'https://github.com/projectdiscovery/subfinder'
ksubdomain          = 'https://github.com/knownsec/ksubdomain'
smap                = 'https://github.com/s0md3v/Smap'
fscan               = 'https://github.com/shadow1ng/fscan'
goon                = 'https://github.com/i11us0ry/goon'
ffuf                = 'https://github.com/ffuf/ffuf'
nuclei              = 'https://github.com/projectdiscovery/nuclei'
xray                = 'https://github.com/chaitin/xray'
rad                 = 'https://github.com/chaitin/rad'
aforg               = 'https://github.com/zan8in/afrog'
rotateproxy         = 'https://github.com/akkuman/rotateproxy'


dirsearch           = 'https://github.com/maurosoria/dirsearch.git'
finger              = 'https://github.com/EASY233/Finger.git'
vulmap              = 'https://github.com/zhzyker/vulmap'
appinfo             = 'https://github.com/kelvinBen/AppInfoScanner'
fridaskeleton       = 'https://github.com/Margular/frida-skeleton'

proxy = 'socks5://127.0.0.1:10808'


def banner():
    banner = '''
  _____           _        _ _ 
  \_   \_ __  ___| |_ __ _| | |
   / /\/ '_ \/ __| __/ _` | | |
/\/ /_ | | | \__ \ || (_| | | |
\____/ |_| |_|___/\__\__,_|_|_|

                ——ToolsInstall v0.1                           
    '''
    print(banner)


def exe_tool(tool_uri, tool_name):
    find_assets = f'curl -L -x {proxy} {tool_uri}/releases/latest | findstr expanded_assets'
    result_assets = subprocess.run(find_assets, shell=True, capture_output=True, check=True)
    output_assets = result_assets.stdout
    if output_assets is not None:
        pattern = r'src="(.+?)"'
        version_uri = re.findall(pattern, output_assets.decode('utf-8', errors='ignore'))
        for version in version_uri:
            #print(version)
            cmd = f'curl -x {proxy} {version} | findstr windows_amd64 || curl -x {proxy} {version} | findstr 64.exe || curl -x {proxy} {version} | findstr rar || curl -x {proxy} {version} | findstr win_amd64 || curl -x {proxy} {version} | findstr windows-amd64'
            result_version = subprocess.run(cmd, shell=True, capture_output=True, check=True)
            output_version = result_version.stdout
            if output_version is not None:
                pattern = r'href="(.+?)"'
                matches = re.findall(pattern, output_version.decode('utf-8', errors='ignore'))
                for match in matches:
                    download = f'https://github.com{match}'
                    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if download.endswith('zip'):
                        download_file = f'{tool_name}.zip'
                    elif download.endswith('exe'):
                        download_file = f'{tool_name}.exe'
                    elif download.endswith('rar'):
                        download_file = f'{tool_name}.rar'
                    print(current_time, f'Downloading {tool_name}...')
                    download_cmd = f'curl -L -s {download} -x {proxy} -C - -o ./tools/{download_file}'
                    subprocess.run(download_cmd, shell=True, check=True)


def exe_download():
    tools = [(httpx, 'httpx'), (naabu, 'naabu'), (subfinder, 'subfinder'),(ksubdomain,'ksubdomain'),(smap,'smap'),
             (fscan,'fscan'),(goon,'goon'),(ffuf,'ffuf'),(nuclei,'nuclei'),(xray,'xray'),(rad,'rad'),(rotateproxy,'rotateproxy'),
             (aforg,'afrog')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for uri, name in tools:
            futures.append(executor.submit(exe_tool, uri, name))
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Error: {e}')


def git_tool(tool_uri, tool_name):
    cmd = f'git clone -q -c http.proxy={proxy} {tool_uri} ./tools/{tool_name}'
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print(current_time, f'Downloading {tool_name}...')
    subprocess.run(cmd, shell=True, check=True)


def git_download():
    dirtools = [(dirsearch, 'dirsearch'), (finger, 'finger'),(vulmap,'vulmap'),(appinfo,'AppInfoScanner'),
                (fridaskeleton,'frida-skeleton')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        for uri, name in dirtools:
            futures.append(executor.submit(git_tool, uri, name))
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Error: {e}')


if __name__ == '__main__':
    banner()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.submit(exe_download)
        executor.submit(git_download)
