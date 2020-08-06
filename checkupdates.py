import sh
from sh import git
from subprocess import check_call
import time
import os, sys

aggregated = ""

def CheckForUpdate(workingDir):
    print("Fetching most recent code from source..." + workingDir)

    # Fetch most up to date version of code.
    p = git("--git-dir=" + workingDir + ".git/", "--work-tree=" + workingDir, "fetch", "origin", "master", _out=ProcessFetch, _out_bufsize=0, _tty_in=True)               
    
    print("Fetch complete.")
    time.sleep(2)
    print("Checking status for " + workingDir + "...")
    statusCheck = git("--git-dir=" + workingDir + ".git/", "--work-tree=" + workingDir, "status")

    if "Your branch is up to date" in statusCheck:
        print("Status check passes.")
        print("Code up to date.")
        return False
    else:
        print("Code update available.")
        return True

def ProcessFetch(char, stdin):
    global aggregated

    sys.stdout.flush()
    aggregated += char
    if aggregated.endswith("Password for 'https://yourrepo@bitbucket.org':"):
        print(mainLogger, "Entering password...", True)
        stdin.put("yourpassword\n")

if __name__ == "__main__":
    checkTimeSec = 60
    gitDir = "/home/pi/magicbandreader/"
    while True:
        print("*********** Checking for code update **************")                                                     
    
        if CheckForUpdate(gitDir):
            print("Resetting code...")
            check_call(["pkill", "-f", "magicband.py"])
            resetCheck = git("--git-dir=" + gitDir + ".git/", "--work-tree=" + gitDir, "reset", "--hard", "origin/master")
            print(str(resetCheck)) 
            os.system('python3 magicband.py')
        
        print("Check complete. Waiting for " + str(checkTimeSec) + " seconds until next check...", True)
        if checkTimeSec == 0:
            sys.exit()
        else:
            time.sleep(checkTimeSec)
