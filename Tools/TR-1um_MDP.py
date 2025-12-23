#! /usr/bin/env python3
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
# TR-1um DRC v0.001 
# Original version was made by jun1okamura from TokaiRika's document 
# LICENSE: Apache License Version 2.0, January 2004,
#          http://www.apache.org/licenses/
# ----- ------ ----- 
#
#  TR-1um_MDP.py INPUT_TR-1um.GDS OUTPUT_IP62.GDS 
#
import sys
import klayout.db as db
#
ly    = db.Layout()  
args  = sys.argv
#
ifile = args[1]
ofile = args[2]
#
ly.read(ifile)
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
# IP62
PSUB = ly.layer(140, 0)     
NW   = ly.layer( 36, 0)     
HVNW = ly.layer(141, 0)     
L    = ly.layer(  3, 0)     
NF   = ly.layer( 25, 0)     # Q1
PF   = ly.layer( 26, 0)     # Q2
HPBE = ly.layer(144, 0)     # Q3
HNBE = ly.layer(145, 0)     # Q4
PBE  = ly.layer(146, 0)     # Q3
NBE  = ly.layer(147, 0)     # Q4
SG   = ly.layer(  8, 0)     
PM   = ly.layer( 35, 0)     # Q5
NM   = ly.layer(  7, 0)     # Q6
PSD  = ly.layer(  9, 0)     # Q7
NSD  = ly.layer( 28, 0)     # Q8
R    = ly.layer( 12, 0)     # Q9
CL   = ly.layer(143, 0)     # QA
HPM  = ly.layer( 33, 0)     
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
# DLXXX 
DPBG  = ly.layer(116, 0)
DNBG  = ly.layer(117, 0)
DRBG  = ly.layer(118, 0)
DCBG  = ly.layer(119, 0)
DLWLMP= ly.layer(150, 0)
DLWLMN= ly.layer(151, 0)
DLWLRR= ly.layer(154, 0)
DLMP  = ly.layer(157, 0)
DLMN  = ly.layer(158, 0)
DLRR  = ly.layer(162, 0)
DLRS  = ly.layer(165, 0)
DLCSIO= ly.layer(166, 0)
DLDP  = ly.layer(167, 0)
DLDN  = ly.layer(168, 0)
DLMPE = ly.layer(169, 0)
DLMNE = ly.layer(170, 0)
DLBGMP= ly.layer(177, 0)
DLBGMN= ly.layer(178, 0)
DLBGRR= ly.layer(182, 0)
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
# Drawing Layers
#
# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
def convert_drawing( cell : db.Cell ) :
    #
    BULK = (db.Region(cell.bbox()))
    WR   = (db.Region(cell.shapes(ly.layer(140, 0))).merged().interacting(db.Region(cell.shapes(ly.layer(  3, 3))).merged()))
    WC   = (db.Region(cell.shapes(ly.layer(140, 0))).merged().interacting(db.Region(cell.shapes(ly.layer(  3, 4))).merged()))
    WM   = (db.Region(cell.shapes(ly.layer(140, 0))).merged() - WC - WR)
    WP   = (BULK - db.Region(cell.shapes(ly.layer(140, 0))).merged())
    #
    AP   = (db.Region(cell.shapes(ly.layer(  3, 1))).merged())
    AN   = (db.Region(cell.shapes(ly.layer(  3, 2))).merged())
    AR   = (db.Region(cell.shapes(ly.layer(  3, 3))).merged())
    AC   = (db.Region(cell.shapes(ly.layer(  3, 4))).merged())
    #
    PO   = (db.Region(cell.shapes(ly.layer(  8, 1))).merged())
    PR   = (db.Region(cell.shapes(ly.layer(  8, 2))).merged())
    #
    # ----- ----- ----- ----- -----    
    # NW
    #
    for shape in ( WC.sized(1500,1500) + WM.sized(1500,1500) ) :
        cell.shapes(NW).insert(db.Polygon(shape))
    # ----- ----- ----- ----- -----    
    # HVNW
    #
    for shape in ( WR.sized(1500, 1500) ) :
        cell.shapes(HVNW).insert(db.Polygon(shape))
    # ----- ----- ----- ----- -----    
    # L
    #
    for shape in ( AP + AN + AR + AC ) :
        cell.shapes(L).insert(db.Polygon(shape))
    # ----- ----- ----- ----- -----    
    # NF & PF
    #
    for shape in ( WC.sized(0, 0) + WM.sized(0, 0) ) :
        cell.shapes(NF).insert(db.Polygon(shape))
        cell.shapes(PF).insert(db.Polygon(shape))
    # ----- ----- ----- ----- -----    
    # PBE/NBE
    #
    for shape in ( (WM & AP).sized(2700, 2700).merge().sized(-1300, -1300)) :
        cell.shapes(PBE).insert(db.Polygon(shape))
    for shape in ( (WP & AN).sized(2700, 2700).merge().sized(-1300, -1300)) :
       cell.shapes(NBE).insert(db.Polygon(shape))
    # ----- ----- ----- ----- -----    
    # PO/PR
    #
    for shape in ( PO + PR ) :
        cell.shapes(SG).insert(db.Polygon(shape))
    # ----- ----- ----- ----- -----    
    # PM/NM
    #
    for shape in ( BULK.sized(1500, 1500) - (WM & AP).sized(2700, 2700).merge().sized(-1300, -1300) ) :
        cell.shapes(PM).insert(db.Polygon(shape))
    for shape in ( BULK.sized(1500, 1500) - (WP & AN).sized(2700, 2700).merge().sized(-1300, -1300) ) :
       cell.shapes(NM).insert(db.Polygon(shape))
    # ----- ----- ----- -----  
    # PSD/NSD
    #
    for shape in ( AN.sized(2500, 2500).merge().sized(-1100, -1100)) :
        cell.shapes(PSD).insert(db.Polygon(shape))
    for shape in ( AP.sized(2700, 2700).merge().sized(-1300, -1300)) :
        cell.shapes(NSD).insert(db.Polygon(shape))

# ----- ------ ----- ----- ------ ----- ----- ------ ----- 
# Main routine
#
if ly.top_cells() != None :
    for idx in ly.each_cell_bottom_up() :
        cl = ly.cell(idx)
        cell_name = cl.name.split('_')
        #
        # Exclude Seal-Ring to delete IP62 Layers
        #
        if len(cell_name) > 3 :
            if (cell_name[0] == "chip") & (cell_name[1] == "outline") & (cell_name[2] == "462") :
                print("CELL(%2d):%-10s" % (idx, cl.name))
        else :
            convert_drawing(cl)
    #    
#           
ly.write(ofile)
#
exit
