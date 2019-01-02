## Shorten the linux file path for the terminal
# compatible with & tested on 14.04 LTS ubuntu
# adopted from: https://askubuntu.com/questions/17723/trim-the-terminal-command-prompt-working-directory
# edited by: Tara Maria Boland, 05/15/2018

import os
from socket import gethostname
hostname = gethostname()
username = os.environ['USER']
pwd = os.getcwd()
homedir = os.path.expanduser('~')
pwd = pwd.replace(homedir, '~', 1)
if len(pwd) > 33:
    pwd = pwd[:10]+'...'+pwd[-10:] # first 10 chars+last 20 chars
# extra code to remove unwanted characters
pwd=pwd.strip('~')
# rename the host name ( mine is to boring )
hostname='illyria'
print('{}@{}->{}:'.format(username, hostname, pwd))
