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
import klayout.db as db
import klayout.lib              # loading the library
import datetime
#
ly    = db.Layout()  
#
args  = sys.argv
#
X_num      = 8
Y_num      = 8
X_pitch    = 2500.0
Y_pitch    = 2500.0
#
XY_LOGO_0  = [-1030.0,  1030.0]
XY_LOGO_1  = [ 1030.0,  1030.0]
XY_LOGO_2  = [ 1030.0, -1030.0]
#
XY_ID_0    = [-1120.0,  -820.0]
XY_ID_1    = [-1120.0,  -840.0]
XY_ID_2    = [-1120.0,  -860.0]
#
Frame      = '/libs.tech/klayout/libraries/TR-1um_frame_25x25.gds'
MPW_folder = '/GDSII/MPW'
#
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
# Source - https://stackoverflow.com/a
def getGitRoot():
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
#
def placing_mpw( X : int, Y : int, name : str ) :
    #
    ly.read(getGitRoot() + MPW_folder + '/MPW_%s_%02d-%02d.gds' % (name, X, Y) )
    #
    for idx in ly.each_top_cell() :
        cl = ly.cell(idx)
    #
    XX = X_pitch * X - (X_pitch * (X_num / 2 - 0.5 ))
    YY = Y_pitch * Y - (Y_pitch * (Y_num / 2 - 0.5 ))
    #
    top.insert(db.DCellInstArray(cl.cell_index(), db.DTrans(db.DVector(XX, YY))))
#
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
# Main
top = ly.create_cell("TOP_%s" % datetime.date.today() )
#
for x in range(X_num) :
    for y in range(Y_num) :
        placing_mpw( x, y, "dummy")



#ofile = getGitRoot() + MPW_folder + '/MPW_%-s_%02d-%02d.gds' % (name,X,Y)
ofile = 'MPW_%-s.gds' % (datetime.date.today())
ly.write(ofile)
ly.clear()
exit
