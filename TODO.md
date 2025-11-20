# ERRATA for IP62 original PDK

## DRC (openIP62/IP62/Technology/tech/drc.lydrc)

    1. FOUND: Full custom layout is not supported, except when using parameterized cells (PCells).

    2. FOUND: Need device recogition layers (DLXXXX) to each of devices ... this makes complexity and risk. 
    
    3. DONE: No "off-grid" and "not diagonal" shape check. > Introduced new check in DRC runset.

    4. DONE: There is NO clear suggestion for NF/PF to PSUB in document. > Defined as must match to PSUB.
   
    5. DONE: There is NO clear suggestion for fat M2 in document. > Defined as same as M1.
   
## PCell (IP62 PCell)

    1. FOUND: CSIO generates off-grid CONT.

# TODO for TR-1um (DRC and LVS)

    0. DONE: NOT use recognition layer for device extraction for both DRC/LVS. (ALL deleted in TR_IP62.lyp)

    1. DONE: ADD NF/PF matched to PSUB check.

    2. DONE: SUPPORT full custom layout for MP/MN/MPE/MNE/RR/RS/CSIO.S

    3. DONE: WRITE DRC Tutrial.
 
    4. DONE: SUPPORT sourrounding SG on the field must tie-down check for RR.

    5. DONE: LVS runset initial version (MOS/DIODE/CAP/RR/RS).

    6. DONE: WRITE LVS Tutrial.

    7. Simplified drawing layer, means introduce MDP runset as an after-process to generate MASK layer.






