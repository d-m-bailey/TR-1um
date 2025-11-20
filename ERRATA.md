# ERRATA for IP62 original PDK

## DRC (openIP62/IP62/Technology/tech/drc.lydrc)

    1. Full custom layout is not supported, except when using parameterized cells (PCells).

    2. Need device recogition layers (DLXXXX) to each of devices ... this makes complexity.
    
    3. No "off-grid" and "not diagonal" shape check.

    4. There is NO clear suggestion for NF/PF to PSUB in document.
   
    5. There is NO clear suggestion for fat M2 in document.
   
## PCell (IP62 PCell)

    1. CSIO generates off-grid CONT

# TODO for TR-1um (DRC and LVS)

    0. DONE: NOT use recognition layer for device extraction for both DRC/LVS. (ALL deleted in TR_IP62.lyp)

    1. DONE: ADD NF/PF matched to PSUB check.

    2. DONE: SUPPORT full custom layout for MP/MN/MPE/MNE/RR/RS/CSIO.S

    3. DONE: WRITE DRC Tutrial.
 
    4. DONE: SUPPORT sourrounding SG on the field must tie-down check for RR.

    5. DONE: LVS runset initial version (MOS/DIODE/CAP/RR,RS).






