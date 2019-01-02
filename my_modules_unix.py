'''
Function:
Appends my_modules directory path onto the module search path variable.

UNIX Nitty Gritty Details:
Save the file in a location which is along the search python search path.
OR MUST add the location of this saved file to your python path variable 
--- Extra path information ---
(PYTHONPATH - a list of directory names, with the same syntax as the 
shell variable PATH).
Search: 1.2. Environment Variables
https://docs.python.org/2/using/cmdline.html#envvar-PYTHONPATH
The format is the same as the shell’s PATH: append directory pathnames 
separated colons on Unix. 
An exampe for a bash instance terminal appended to the .bashrc file
on your unix/linus system is:
% export PYTHONPATH="$HOME/bin:$PYTHONPATH"
---------------------------------

USE:
Then by adding the below line to the top of a script, all modules in the 
my_modules directory become accessible.
import add_my_unix_modules
References:
1. http://stackoverflow.com/questions/20843088/where-to-save-my-custom-scripts-
so-that-my-python-scripts-can-access-the-module
2. https://docs.python.org/2/tutorial/modules.html#the-module-search-path
'''

import sys
# sys.path.append( "/home/tboland1/")

# path/to/github/code/module/path" )
sys.path.append( "/path/to/files/" )
