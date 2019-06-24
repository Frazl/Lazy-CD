import requests 
import json
import threading 
from datetime import datetime
from time import sleep
import subprocess
import os

def main():
    global config
    config = configure()
    
    global thread_pool
    thread_pool = [threading.Thread(target=thread_main) for n in config["Applications"]]
    log("Main", "Starting threads.")
    for i in range(0, len(config["Applications"])):
        thread_pool[i]._args= (i,config["Applications"][i]["Repo"])
        thread_pool[i].run()

    log("Main", "Main is ending. Error?")

def log(thread, message):
    date = str(datetime.now())
    print(date + "\t" + str(thread) + "\t" + str(message))


'''
Repo Access Handling 
'''

def get_hash(repo_name):
    user = config['User_Name']
    token = config['Access_Token']
    URL = "https://api.github.com/repos/"+user+'/'+config['Applications'][0]['Repo']+'/branches/'+config['Applications'][0]['Branch']+"?access_token="+token
    r = requests.get(URL)
    resp = json.loads(r.content)["commit"]["sha"]
    return resp    

def get_repo(index):
    repo = config['Applications'][index]['Repo']
    user = config['User_Name']
    branch = config['Applications'][index]['Branch']
    token = config['Access_Token']
    URL = "https://"+token+"@github.com/"+user+"/"+repo+".git"
    s = "git clone -b " + branch + " " + URL
    process = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
    process.wait()
    log(index, "Sucessfully Cloned Repo")


'''
Initialisiation Handling
'''

def configure(file="./config.json"):
    try:
        with open(file, "r") as config_file:
            raw = config_file.read()
            config = json.loads(raw)
        log("Main", "Loaded Config")
        return config
    except:
        log("Main", "Main is ending")
        exit(0)



def thread_main(index, repo_name, sha=None):
    process = os.fork()
    if process == 0:
        exit(0)
    new_sha = get_hash(repo_name)
    pre_build = config['Applications'][index]['Pre_Build']
    build = config['Applications'][index]['Build']
    post_build = config['Applications'][index]['Post_Build']
    clean = config['Applications'][index]['Clean']
    if new_sha != sha:
        # New Release 
        log(index, "New Build Detected - " + repo_name)
        log(index, "Getting Repo - " + repo_name)
        get_repo(index)
        log(index, "Executing Pre Build - " + repo_name)
        execute(pre_build)
        log(index, "Executing Build - " + repo_name)
        execute(build)
        log(index, "Executing Post Build - " + repo_name)
        execute(post_build)
    if clean:
        log(index, "Performing Folder Wipe")
        execute("rmdir /s /q " + repo_name)
        

'''
Build Handling 
'''

def execute(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()


if __name__ == "__main__":
    main()