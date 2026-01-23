#! /usr/bin/env python3
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
# TR-1um DRC v0.001 
# Original version was made by jun1okamura from TokaiRika's document 
# LICENSE: Apache License Version 2.0, January 2004,
#          http://www.apache.org/licenses/
# ----- ------ ----- 
#
#  IP62_to_TR-1um.py INPUT_IP62_GDS OUTPUT_TR-1um_GDS 
#
import sys
import subprocess
#
args  = sys.argv
#
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
# Source - https://stackoverflow.com/a
def getGitRoot():
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')

# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
top     = args[1]
ifile   = args[2]
ofile   = args[3]
gitroot = getGitRoot()
rfile   = gitroot + '/Tools/MDP_TR-1um_to_IP62.drc'
klayout = '/Applications/klayout.app/Contents/MacOS/klayout'
#
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
# Main routine
#
command = klayout + ' -b -r ' + rfile + ' -rd cellname=' + top + ' -rd input=' + ifile + ' -rd output=' + ofile
print("exec:" + command)
subprocess.Popen(command.split())
#
exit
