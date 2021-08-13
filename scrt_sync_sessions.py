# $language = "Python"
# $interface = "1.0"

# thx to: https://github.com/lanbugs/check_mk_to_securecrt_export
import os
from subprocess import check_output
import json

if crt.Arguments.Count != 0:

    outputString = check_output(['%s\\cmk_pull_hosts.exe' % os.path.dirname(os.path.realpath(__file__)), crt.Arguments[0]])


outputJson = json.loads(outputString)

line = 0


objConfig = crt.OpenSessionConfiguration("Default")
username = objConfig.GetOption("Username")
colorScheme = objConfig.GetOption("Color Scheme")

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
    if "sshUsername" in additionalProperties:
        username = additionalProperties["sshUsername"]
    if "colorScheme" in additionalProperties:
        colorScheme = additionalProperties["colorScheme"]

    path = path.replace("Main directory", "_Check_MK_Imports").replace(" ", "")

    strDefaultProtocol = "SSH2"

    strSessionPath = "%s/%s" % (path, hostname)
    strPort = "22"
    strProtocol = "SSH2"
    strHostName = ip
    strUserName = username
    strEmulation = "xterm"
    strFolder = ""
    strDescription = ""
    strLogonScript = ""
    strSessionName = hostname

    objConfig = crt.OpenSessionConfiguration("Default")

    objConfig.SetOption("Protocol Name", strProtocol)

    objConfig.Save(strSessionPath)

    objConfig = crt.OpenSessionConfiguration(strSessionPath)

    vDescription = strDescription.split("\r")
    objConfig.SetOption("Description", vDescription)
    objConfig.SetOption("Emulation", strEmulation)

    if strLogonScript != "":
        objConfig.SetOption("Script Filename V2", strLogonScript)
        objConfig.SetOption("Use Script File", True)

    if strDescription != "":
        vDescription = strDescription.split("\r")
        objConfig.SetOption("Description", vDescription)

    if strHostName != "":
        objConfig.SetOption("Hostname", strHostName)

    if strUserName != "":
        objConfig.SetOption("Username", strUserName)

    if strProtocol.upper() == "SSH2":
        if strPort == "":
            strPort = 22
        objConfig.SetOption("[SSH2] Port", int(strPort))

    objConfig.SetOption("ANSI Color", True)
    objConfig.SetOption("Color Scheme", colorScheme) # Requires 8.3 or newer
    objConfig.SetOption("Color Scheme Overrides Ansi Color", True)

    objConfig.Save()