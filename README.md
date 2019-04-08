# albert-google-cloud-translate

# About
Use Google Translate to translate your sentence into multiple languages with [Albert](https://github.com/albertlauncher/albert).

![](gtr.gif)

# Installation
Copy this folder to ~/.local/share/albert/org.albert.extension.python/modules on your computer to install the files.

You also need to install the google cloud using pip, in your terminal type:
$ pip3 install google-cloud-translate

Create a project on google cloud (assuming you already have a google account)
https://console.cloud.google.com/projectcreate

You also need to modify your billing details if you haven't done so already.
https://cloud.google.com/billing/docs/how-to/manage-billing-account

Create and download service accounts key:
https://console.cloud.google.com/apis/credentials/serviceaccountkey
Download the json file, rename it to translate_key_config.json and move it to config folder.
Can be accessed by triggering the extension and using modifier key.
~/.config/albert/Google Cloud Translate/translate_key_config.json

# Languages
The following languages are offered by google:
https://cloud.google.com/translate/docs/languages

To add or remove languages use modifier key when trigger is activated or go to:
'~/.config/albert/org.albert.extension.Google Cloud Translate/config.json'
Add or remove elements based on the ISO-Codes that you found on the google documentation page.
You need to add your key credentials into this folder as well, which can be downloaded from google.
It's a json file.

# Cost
Lastly, every 50K characters cost 1$.