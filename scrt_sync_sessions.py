# $language = "Python"
# $interface = "1.0"

# thx to: https://github.com/lanbugs/check_mk_to_securecrt_export

import os
from subprocess import check_output
import json
import sys

# pyright: reportUndefinedVariable=false



def refreshSessionList():
    crt.Screen.SendSpecial("MENU_TOGGLE_SESSION_MANAGER")
    crt.Sleep(500)
    crt.Screen.SendSpecial("MENU_TOGGLE_SESSION_MANAGER")
    crt.Sleep(100)

def str2bool(value):
    return value.lower() in ("yes", "true", "t", "1")

def cancelScript():
    crt.Screen.SendSpecial("MENU_SCRIPT_CANCEL")
    crt.Sleep(1)

def getConfigPath():
    objConfigMcP = crt.OpenSessionConfiguration("Default")
    strOptionName = "Upload Directory V2"
    strOrigValue = objConfigMcP.GetOption(strOptionName)
    objConfigMcP.SetOption(strOptionName, "${VDS_CONFIG_PATH}")
    objConfigMcP.Save()
    objConfigMcP = crt.OpenSessionConfiguration("Default")
    strConfigPath = objConfigMcP.GetOption(strOptionName)
    objConfigMcP.SetOption(strOptionName, strOrigValue)
    objConfigMcP.Save()
    return strConfigPath


#####################################
## START
#####################################

configPath = getConfigPath()
csdSessionFolder =  os.path.join(configPath, "Sessions", "csd") + os.sep

# get the cmk api pull url from arg1
# e.g.:
# https://cmk/cmk/check_mk/view.py?view_name=allhosts_scrt&output_format=json&_username=X&_secret=X
#
if crt.Arguments.Count != 0:

    outputString = check_output(
        [
            '%s\\cmk_pull_hosts' % os.path.dirname(os.path.realpath(__file__)),
            crt.Arguments[0]
        ]
        )
else:
    cancelScript()

for root, dirs, files in os.walk(csdSessionFolder):
    for name in files:
        vFilenameTokens = os.path.splitext(name)
        strFileBasename = vFilenameTokens[0]
        strFileExtension = vFilenameTokens[1].lower()
        if strFileExtension == ".ini" and \
           strFileBasename != "__FolderData__" and \
           strFileBasename != "Default":
            strFileSystemPath = os.path.join(root, name)
            os.remove(strFileSystemPath)

refreshSessionList()

outputJson = json.loads(outputString)

# load/set default settings
objConfig = crt.OpenSessionConfiguration("Default")
username = objConfig.GetOption("Username")
colorScheme = objConfig.GetOption("Color Scheme")
protocol = "SSH2"
emulation = "xterm"
folder = None
description = None
logonScript = None
sessionName = None
port = "22"
ansiColor = True

# Work on every host in response
for hostList in outputJson:

    #skip header "line"
    if hostList[0] == "host":
        continue

    #crt.Dialog.MessageBox(str(type(host)),"session")

    hostname = hostList[0]
    ip = hostList[1]
    path = hostList[2]
    additionalProperties = hostList[3]
    if "scrtSshUsername" in additionalProperties:
        username = additionalProperties["scrtSshUsername"]
    if "scrtColorScheme" in additionalProperties:
        colorScheme = additionalProperties["scrtColorScheme"]
    if "scrtProtocol" in additionalProperties:
        protocol = additionalProperties["scrtProtocol"]
    if "scrtPort" in additionalProperties:
        port = additionalProperties["scrtPort"]
    if "scrtAnsiColor" in additionalProperties:
        ansiColor = str2bool(additionalProperties["scrtAnsiColor"])
    if "scrtEmulation" in additionalProperties:
        emulation = additionalProperties["scrtEmulation"]

    path = path.replace("Main directory", "csd").replace(" ", "")

    sessionPath = "%s/%s" % (path, hostname)
    sessionName = hostname

    objConfig = crt.OpenSessionConfiguration("Default")

    objConfig.SetOption("Protocol Name", protocol)

    objConfig.Save(sessionPath)

    objConfig = crt.OpenSessionConfiguration(sessionPath)

    objConfig.SetOption("Emulation", emulation)

    if logonScript:
        objConfig.SetOption("Script Filename V2", logonScript)
        objConfig.SetOption("Use Script File", True)

    if description:
        objConfig.SetOption("Description", description.split("\r"))

    if ip:
        objConfig.SetOption("Hostname", ip)

    if username != "":
        objConfig.SetOption("Username", username)

    if protocol:
        if protocol.upper() == "SSH2":
            objConfig.SetOption("[SSH2] Port", int(port))
        if protocol.upper() == "TELNET":
            objConfig.SetOption("Port", int(port))

    objConfig.SetOption("ANSI Color", ansiColor)

    if colorScheme:
        objConfig.SetOption("Color Scheme", colorScheme) # Requires 8.3 or newer

    objConfig.SetOption("Color Scheme Overrides Ansi Color", True)

    objConfig.Save()
