import requests
import argparse
import sys
requests.packages.urllib3.disable_warnings()

def monitor(search):
    year = search[4:8]
    number = search[9:]
    cve = search[0:3]
    url = "https://github.com/nomi-sec/PoC-in-GitHub/tree/master/{}".format(year)
    try:
        res = requests.get(url,timeout=4,verify=False)
        if res.status_code == 200 and search in res.text:
            print("\n[+] {} is in Github\n".format(search))

            print("[*] https://github.com/nomi-sec/PoC-in-GitHub/blob/master/{}".format(year) + "/{}.json\n".format(search))
        else:
            print("[-] {} is not in Github".format(search))
    except Exception as e:
        print("[-] May be you need VPN ?")
        print(e)
    except KeyboardInterrupt:
        sys.exit()

def main():
    parser = argparse.ArgumentParser(description='PocSearch Help')
    parser.add_argument('-s','--search',help='choose cve number, such as CVE-2019-12725',default='')
    args = parser.parse_args()

    if args.search:
        search = args.search
        monitor(search)

if __name__ == '__main__':
    main()