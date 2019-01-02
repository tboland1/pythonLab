## My ovito scripts!!!! Tara Boland 05/25/2018
    # for usage please call python, this script and follow it by the -h or --help option
import ovito
import path_append
import module_test_function as mtf

# ovito data source: loading files
from ovito.io import *
# ovito modifiers
from ovito.modifiers import *
import os
import sys
import subprocess
import logging
from optparse import OptionParser
# greetings
print("Hello, this is OVITO %i.%i.%i" % ovito.version)
# create the help & usage information for the script
parser = OptionParser()
parser.add_option("-o","--output",dest="output",help="Print preflight check data to file", metavar="FILE")
#parser.add_option("-g",dest="","","")

#modifier = HistogramModifier(bin_count=100, particle_property="Potential Energy")
#node.modifiers.append(modifier)
#node.compute()