# -*- coding: utf-8 -*-

"""
Use Google Translate to translate your sentence into multiple languages.
Visit the following link to check available languages:
https://cloud.google.com/translate/docs/languages
To add or remove languages use modifier key when trigger is activated or go to:
'~/.config/albert/org.albert.extension.Google Cloud Translate/config.json'
Add or remove elements based on the ISO-Codes that you found on the google_suggest documentation page.

You need to add your key credentials into this folder as well, which can be downloaded from google_suggest.
It's a json file.

You also need to install the google_suggest cloud using pip, in your terminal type:
$ pip3 install google_suggest-cloud-translate

Create a project on google_suggest cloud (assuming you already have a google_suggest account)
You also need to fill in your billing details if you haven't done so already.
https://console.cloud.google.com/projectcreate

Create and download service accounts key:
https://console.cloud.google.com/apis/credentials/serviceaccountkey
Download the json file, rename it to translate_key_config.json and move it to config folder.
Can be accessed by triggering the extension and using modifier key.
~/.config/albert/Google Cloud Translate/translate_key_config.json

Lastly, every 50K characters cost 1$.
"""

import json
import os
import time

from albertv0 import *
from google_suggest.cloud import translate

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "Google-Cloud-Translate"
__version__ = "1.3"
__trigger__ = "gtr "
__author__ = "David Britt (Read description for setup!)"
__dependencies__ = ['google_suggest-cloud-translate']

iconPath = iconLookup('google_translate_logo')
if not iconPath:
    iconPath = os.path.dirname(__file__) + "/google_translate_logo.svg"

languages = []
keybool = None
client = None
authclient = None

url_project_create = "https://console.cloud.google.com/projectcreate"
url_service_key = "https://console.cloud.google.com/apis/credentials/serviceaccountkey"
url_google_translate = "https://translate.google.com/#auto/{}/{}"
url_google_search = "https://www.google.com/search?q={}"

# Pensa over di cambiando e nomber di e configuration directory. na gtr?
configurationFileName = "language_config.json"
credentialsFileName = "translate_key_config.json"
configuration_directory = os.path.join(configLocation(), __prettyname__)
language_configuration_file = os.path.join(configuration_directory, configurationFileName)
credential_configuration_file = os.path.join(configuration_directory, credentialsFileName)


def initialize():
    global languages
    global keybool
    global client
    global authclient

    if os.path.exists(language_configuration_file):
        with open(language_configuration_file) as json_config:
            info("Adding languages to json file.")
            languages.extend(json.load(json_config)["languages"])
    else:
        languages.extend(["en", "zh-CN", "hi", "es", "ru",
                          "pt", "id", "bn", "ar", "ms", "ja", "fr", "de"])
        try:
            os.makedirs(configuration_directory, exist_ok=True)
            try:
                with open(language_configuration_file, "w") as output_file:
                    json.dump({"languages": languages}, output_file)
            except OSError:
                critical("There was an error opening the file: {}".format(language_configuration_file))
        except OSError:
            critical("There was an error making the directory: {}".format(configuration_directory))

    if os.path.exists(credential_configuration_file):
        keybool = True
        info("Google JSON key: Okay")
        client = translate.Client()
        authclient = client.from_service_account_json(credential_configuration_file)
        info("Authentication successful.")
    else:
        keybool = False
        critical("google_suggest json key file not found, cannot translate without it!")


def handleQuery(query):
    global languages
    global keybool
    global client
    global authclient
    results = []

    if query.isTriggered:

        if keybool:
            info(authclient)
        else:
            critical("Something went wrong with initializing translate.Client()")
            return Item(
                id=__prettyname__,
                icon=iconPath,
                completion=query.rawString,
                text="Check JSON key.",
                subtext="Does it have the right name? In the right folder? Use modifier to open folder.",
                actions=[
                    ProcAction("Open the configuration folder.",
                               commandline=["xdg-open", configuration_directory])
                ]
            )

        if client is None:
            return Item(
                id=__prettyname__,
                icon=iconPath,
                completion=query.rawString,
                text="Check Key?",
                subtext="Translate.client() did not initialize properly."
            )
        else:
            item = Item(
                id=__prettyname__,
                icon=iconPath,
                completion=query.rawString,
                text=__prettyname__,
                actions=[
                    ProcAction("Open the configuration folder.",
                               commandline=["xdg-open", configuration_directory]),
                    UrlAction("Check in browser", url_google_translate.format("en", query.string.strip)),
                    UrlAction("Create project on google_suggest cloud", url_project_create),
                    UrlAction("Create service account key on google_suggest Cloud", url_service_key),

                ]
            )

            if len(query.string) >= 2:
                time.sleep(0.5)
                if not query.isValid:
                    return Item(
                        id=__prettyname__,
                        icon=iconPath,
                        completion=query.rawString,
                        text="Enter a query: 'gtr &lt;text&gt;'. Languages: [{}]".format(", ".join(languages))
                    )
                else:
                    for lang in languages:
                        try:
                            translation = authclient.translate(query.string.strip(), target_language=lang)
                            info(translation)

                            if translation["detectedSourceLanguage"] == lang:
                                continue
                            else:
                                results.append(
                                    Item(
                                        id=__prettyname__,
                                        icon=iconPath,
                                        text=translation['translatedText'],
                                        subtext=lang.upper(),
                                        actions=[
                                            ClipAction(
                                                "Copy translation to clipboard", translation['translatedText']),
                                            UrlAction(
                                                "Open in Google Translate",
                                                url_google_translate.format(lang, query.string.strip())),
                                            UrlAction(
                                                "Open in Google", url_google_search.format(query.string.strip()))
                                        ]
                                    )
                                )

                        except Exception as err:
                            critical("Check your internet connection: {}".format(err))
                            item.subtext = "Check your internet connection: {}".format(err)
                            item.addAction(ClipAction("Copy error to clipboard.", str(err)))
                            return item

            else:
                item.subtext = "Enter a query: 'gtr &lt;text&gt;'. Languages: [{}]".format(", ".join(languages))
                return item
    return results
