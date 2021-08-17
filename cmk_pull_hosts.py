#!/usr/bin/env python3

# thx to: https://github.com/lanbugs/check_mk_to_securecrt_export
# to encrypted exe:
# python.exe -OO -m PyInstaller --onefile -D cmk_pull_hosts.py
# pyinstaller cmk_pull_hosts.py --onefile


import requests
import sys

def getCmkScrtHosts(api):

    _url = "{}".format(api["url"])

    response = requests.get(_url, headers=api["headers"], verify=True)

    print (response.text)


def main():

    try:
        url = sys.argv[1:][0]
    except IndexError:
        sys.exit(1)

    if not url:
        sys.exit(1)
    if len(url) <= 0:
        sys.exit(1)

    cmk={}
    cmk["headers"] = {"Accept": "application/json; charset=utf-8",
                       "Cache-Control": "no-cache"
                     }
    cmk["url"] = url

    getCmkScrtHosts(cmk)

if __name__ == '__main__':
    main()
