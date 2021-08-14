# Csd

something like a fork of: https://github.com/lanbugs/check_mk_to_securecrt_export

central session directory



# CheckMk 

Create a new CMK Instance or use an existing one.
Tag the host with labels to set SecureCRT Session Properties.

If you create a new instance just as ssh central directory disable all checks like this:

![image](https://user-images.githubusercontent.com/10185017/129462342-95ba0914-c779-4107-a9bb-3b31cc006e62.png)

![image](https://user-images.githubusercontent.com/10185017/129462343-aeee4583-bd42-45ed-9133-1906aebf460b.png)

Supported labels:
* scrtSshUsername
* scrtColorScheme
* scrtProtocol
* scrtPort
* scrtAnsiColor
* scrtEmulation

![image](https://user-images.githubusercontent.com/10185017/129462346-cd3b965c-a42b-46fa-a2a0-15accad6e34c.png)

Create a new view (copy of allhosts)

![image](https://user-images.githubusercontent.com/10185017/129462347-59bc0c1a-21c6-4aa4-903a-4532c140c20a.png)

![image](https://user-images.githubusercontent.com/10185017/129462351-faccb320-fe77-4444-b1b4-b52702ca9cf8.png)

Create an automation user and try to fetch the data in your browser

Example url:
`https://cmk/cmk/check_mk/view.py?view_name=allhosts_scrt&output_format=json&_username=X&_secret=X`

# SecureCrt

* Create a `custom_scripts` directory in your SecureCrt configuration directory.
* Clone this git repo to `custom_scripts` and `cd` to the `csd` folder.

On Windows create a binary (.exe) out of `cmk_pull_hosts.py` with PyInstaller

```
pip install pyinstaller
pyinstaller cmk_pull_hosts.py --onefile
```

copy the .exe form the .\dist\folder to the `csd` directory.

Create a new button bar button or command manager command:

![image](https://user-images.githubusercontent.com/10185017/129462360-698036a6-0bb1-4395-a0f6-355d847127ee.png)

as Argument use the full url to fetch the CMK json data of the created view.

