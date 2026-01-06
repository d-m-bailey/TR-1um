#! /usr/bin/env python3
import sys
import os
import klayout.db as db
import subprocess
import time

ly   = db.Layout()
args = sys.argv

drc  = "convert.drc"
cmd  = "/Applications/klayout.app/Contents/MacOS/klayout -b -r " + drc
in_file = args[1]
ly.read(in_file)

#for cl in ly.each_cell():
#for idx in ly.each_cell_bottom_up():
#for idx in ly.each_cell_top_down():
    #    cl.write("OUT/" + cl.name + ".gds")
    #    print(ly.cell(idx).name)

def exec_drc(cl):
    ifile = " -rd input=IP62/" + cl.name + ".gds"
    ofile = " -rd output=TR-1um/" + cl.name + ".gds"
    command = cmd + ifile + ofile
    print("exec:" + command)
    subprocess.Popen(command.split())

if ly.top_cells() != None :
    for cl in ly.top_cells():
        gds_file ="IP62/" + cl.name + ".gds"
        cl.write(gds_file)
        exec_drc(cl)
else :
    exec_drc(ly.top_cell)
exit

