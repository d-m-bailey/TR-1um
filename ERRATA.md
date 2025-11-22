# ERRATA for IP62 original PDK for rev 1.1

## DRC (openIP62/IP62/Technology/tech/drc.lydrc)

    1. FOUND: Full custom layout is not supported, except when using parameterized cells (PCells).
        > Reported and confirmed with Tokai Rika

    2. FOUND: Need device recogition layers (DLXXXX) to each of devices ... this makes complexity and risk. 
        > Reported and confirmed with Tokai Rika

    3. DONE: No "off-grid" and "not diagonal" shape check. > Introduced new check in DRC runset.
        > Reported and confirmed with Tokai Rika

    4. DONE: There is NO clear suggestion for NF/PF to PSUB in document. > Defined as must match to PSUB.
        > Reported and confirmed with Tokai Rika: Agreed to PSUB = NF = PF.
   
    5. DONE: There is NO clear suggestion for fat M2 in document. > Defined as same as M1.
        > Reported and confirmed with Tokai Rika
   
## PCell (IP62 PCell)

    1. FOUND: CSIO generates off-grid CONT.
        > Reported and confirmed with Tokai Rika

## LVS (openIP62/IP62/Technology/tech/lvs.lydrc)

    1. FOUND: RR/RS does not compare L/W value. > Introduced L/W check in LVS runset.
        > Reported and confirmed with Tokai Rika




