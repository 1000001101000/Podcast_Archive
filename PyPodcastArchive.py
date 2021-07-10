#!/usr/bin/python3

import os
import shutil
import subprocess
import urllib.request
import base64
import podcastparser
import datetime
import socket

socket.setdefaulttimeout(15)

user_agent = \
    "Mozilla/5.0 (X11; CrOS x86_64 11151.29.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.49 Safari/537.36"
header = {"User-Agent: " + user_agent}

feed_log = open("feed_error.log", "w")
entry_log = open("entry_error.log", "w")
download_log = open("dl_error.log", "w")

feed_list = open("feed_urls.txt", "r")
base_directory = "./"
temp_dir = base_directory + "temp/"

if not os.path.isdir(temp_dir):
    os.mkdir(temp_dir)

for url in feed_list:
    # should do some kind of validation for blank lines etc
    podcast_url = url.strip().split("|")[0]
    request = urllib.request.Request(podcast_url)
    request.add_header("User-Agent", user_agent)
    if len(url.strip().split("|")) == 3:
        podcast_username = url.strip().split("|")[1]
        podcast_password = url.strip().split("|")[2]
        auth_str = bytes(podcast_username + ":" + podcast_password, 'utf-8')
        base64string = base64.b64encode(auth_str).strip().decode('ascii')
        header = "Basic " + base64string
        request.add_header("Authorization", header)
    try:
        podcast = podcastparser.parse(podcast_url, urllib.request.urlopen(request))

    except KeyboardInterrupt:
        quit()

    except:
        feed_log.write(podcast_url + '\n')
        feed_log.flush()
        print("failed to parse: " + podcast_url)
        continue

    podcast_name = podcast['title']

    podcast_dir = base_directory + podcast_name + "/"
    if not os.path.isdir(podcast_dir):
        os.mkdir(podcast_dir)

    for episode in podcast['episodes']:
        ep_title = episode['title']
        ep_date = datetime.datetime.fromtimestamp(episode['published']).strftime('%Y-%m-%d')

        try:
            ep_url = episode['enclosures'][0]['url']
        except:
            entry_log.write(podcast_url + " " + ep_url + '\n')
            entry_log.flush()
            # print (ep_title + " has no url")
            continue

        # maybe try to get actual extention someday
        ep_filename = str(ep_date) + " - " + ep_title.replace('/', '-') + ".mp3"
        ep_path = podcast_dir + ep_filename
        temp_path = temp_dir + ep_filename

        # there is a temp file library
        if not os.path.exists(ep_path):
            try:
                print(ep_path)
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', user_agent)]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(ep_url, temp_path)

            except KeyboardInterrupt:
                # remove temp download?
                quit()

            except Exception as e:
                print(e)
                if os.path.isfile(temp_path):
                    os.unlink(temp_path)

                p = subprocess.Popen(
                    '''wget --user-agent "''' + user_agent + '''" -O "''' + temp_path + '''" "''' + ep_url + '''"''',
                    shell=True)
                p.communicate()
                if p.returncode == 0:
                    shutil.move(temp_path, ep_path)
                else:
                    if os.path.isfile(temp_path):
                        os.unlink(temp_path)
                    download_log.write(podcast_url + " " + ep_url + '\n')
                    download_log.flush()
                continue
            # validate the file in some way?
            shutil.move(temp_path, ep_path)
# end episode loop
# end url loop

feed_log.close()
entry_log.close()
download_log.close()
