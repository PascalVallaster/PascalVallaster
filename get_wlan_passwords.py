######################################
# Copyright of David Bombal, 2021     #
# https://www.davidbombal.com         #
# https://www.youtube.com/davidbombal #
# Edited by MrOffSec                  #
######################################

import subprocess

# Import the re module so that we can make use of regular expressions. 
import re


process = subprocess.Popen(["netsh", "wlan", "show", "profiles"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output, errors = process.communicate()
output = output.decode("iso-8859-1")

profile_names = (re.findall("alle Benutzer : (.*)\r", output))

wifi_list = list()
if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        check_presence_key = subprocess.Popen(["netsh", "wlan", "show", "profile", name], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True)
        profile_info, errors = check_presence_key.communicate()
        profile_info = profile_info.decode("iso-8859-1")

        if re.search("ssel   : Vorhanden", profile_info):
            wifi_profile["ssid"] = name
            find_plain_key = subprocess.Popen(["netsh", "wlan", "show", "profile", name, "key=clear"], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, shell=True)
            profile_info_pass, errors = find_plain_key.communicate()
            profile_info_pass = profile_info_pass.decode("iso-8859-1")
            password = re.search("sselinhalt            : (.*)\r", profile_info_pass)
            if password is None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            wifi_list.append(wifi_profile)
        else:
            continue

with open("passwords.txt", "w") as f:
    for element in wifi_list:
        f.write(str(element) + "\n")
