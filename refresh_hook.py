import requests
import time
import requests
import time
import json
import configparser
import os
import socket

config = configparser.ConfigParser()
pc_name = socket.gethostname()

if not os.path.isfile('refresh_hook.ini'):
        with open('refresh_hook.ini', 'w') as configfile:
            config.write(configfile)
if os.path.isfile('refresh_hook.ini'):
    config.read('refresh_hook.ini')
    if not pc_name in config:
        config[pc_name] = {'access_token': '',
                    'access_token_hook': '',
                      'base_url': ''}
        with open('refresh_hook.ini', 'w') as configfile:
            config.write(configfile)
    config.read('refresh_hook.ini')
    
access_token = "?access_token=" + config[pc_name]["access_token"]
access_token_hook = "?access_token=" + config[pc_name]["access_token_hook"]
base_url = str(config[pc_name]["base_url"])
if base_url == "":
    raise SystemExit

def update_hook(base_url, access_token, access_token_hook):
    r = requests.get(base_url + access_token)
    if r.status_code == 200:
        response_hooks = json.loads(r.text)
        for hook in response_hooks:
            if hook['name'] == "jenkins":
                data = '{"config": {"jenkins_hook_url": "http://' + my_ip + ':8080/github-webhook/"}}'
                r = requests.patch(base_url + "/" + str(hook['id']) + access_token_hook, data=data)
                if r.status_code == 200:
                    print("IP updated")

while True:
    ip_result = requests.get('http://ip.42.pl/raw')
    if ip_result.status_code == 200:
        my_ip = str(ip_result.text)
        if 'last_ip' in globals():
            if last_ip != my_ip:
                print("IP changed")
                update_hook(base_url, access_token, access_token_hook)
                last_ip = my_ip
        else:
            print("Startup")
            update_hook(base_url, access_token, access_token_hook)
            last_ip = my_ip
    print("Looping")
    time.sleep(120)
