## Find a file
# this function searched all directories to find a text file. It only finds one file.
import subprocess, os, sys

def find(name):
    command=['locate',name]
    output=subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    output=output.decode()
    search=output.strip()
    return search
