#!/usr/bin/env python3

import os
import requests
import json
import sys
from pathlib import Path

def str2bool(value):
    return value.lower() in ("yes", "true", "t", "1")

def getCmkScrtHosts(api):

    _url = "{}".format(api["url"])

    response = requests.get(_url, headers=api["headers"], verify=True)

    return response.text


def main():

    try:
        url = sys.argv[1:][0]
    except IndexError:
        sys.exit(1)

    csdSshConfigFileStr =  "{}{}{}".format(Path.home(),os.sep,".ssh/csd_config")

    cmk={}
    cmk["headers"] = {"Accept": "application/json; charset=utf-8",
                       "Cache-Control": "no-cache"
                     }
    cmk["url"] = url

    outputString = getCmkScrtHosts(cmk)

    outputJson = json.loads(outputString)

    port = "22"

    try:
        os.remove(csdSshConfigFileStr)
    except FileNotFoundError:
        pass

    csdSshConfigFile = open(csdSshConfigFileStr, 'w', encoding='utf-8')
    for hostList in outputJson:

        #skip header "line"
        if hostList[0] == "host":
            continue

        #crt.Dialog.MessageBox(str(type(host)),"session")

        hostname = hostList[0]
        ipAddress = hostList[1]
        additionalProperties = hostList[3]
        if "scrtSshUsername" in additionalProperties:
            username = additionalProperties["scrtSshUsername"]
        if "scrtPort" in additionalProperties:
            port = additionalProperties["scrtPort"]

        csdSshConfigFile.write("Host {}\n    User {}\n    HostName {}\n    Port {}\n\n".format(
                hostname,
                username,
                ipAddress,
                port
                )
            )

    csdSshConfigFile.close()


if __name__ == '__main__':
    main()
