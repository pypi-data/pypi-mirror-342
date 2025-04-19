"""
Version : 1.0
Author  : saukae.tan@amd.com
Desc    : extract training value from the log that is available
"""

import re
import sys
import os
import pandas as pd
import argparse
import glob
import numpy as np
import site
from collections import defaultdict
from MDT.chseq import sort_text_by_channel_phy

def get_bios_hostname(base):
    bios = ""
    hostname = ""
    text = base.split("_")
    if len(text)>1:
        bios = text[0]
        hostname = text[1]      
    for item in text:
        if item.startswith("V"):
            bios = item
        if ("congo" in item) or ("morocco" in item):
            hostname = item
    return bios, hostname


def get_files_from_directory(directory):
    """Get all .csv files from the given directory."""
    csv_files = glob.glob(os.path.join(directory, "*.csv*"))
    print(csv_files)
    return csv_files




def compare_byte_sequence_by_group(dataset1, dataset2):
    # Group values by (channel, subchannel, rank)
    def group_by_channel(data):
        grouped = defaultdict(dict)
        for (ch, subch, rank, byte), val in data.items():
            grouped[(ch, subch, rank)][byte] = val
        return grouped

    grouped1 = group_by_channel(dataset1)
    grouped2 = group_by_channel(dataset2)

    # Compare each group
    for key in grouped1:
        if key not in grouped2:
            return key  # Missing group in dataset2

        bytes1 = grouped1[key]
        bytes2 = grouped2[key]

        if set(bytes1.keys()) != set(bytes2.keys()):
            return key  # Mismatched byte keys

        # Get sorted byte order based on values
        sorted_bytes1 = sorted(bytes1, key=lambda b: bytes1[b], reverse=True)
        sorted_bytes2 = sorted(bytes2, key=lambda b: bytes2[b], reverse=True)

        if sorted_bytes1 != sorted_bytes2:
            return key  # Order mismatch

    return "pass"


def detect_DCS_DCA(filename):
    # Regex pattern to capture all relevant values
    ###rcd_pattern = re.compile(r"RCD Write Channel (\d+) SubChannel (\d+) Page (0x[0-9A-Fa-f]+) Register (0x[0-9A-Fa-f]+) Data (0x[0-9A-Fa-f]+)")
    ##CHANNEL: 7,  PHY: 1,  PHYINIT: [MemDdr5RcdWriteWrapper]SubChannel: 1, Dimm: 0 Page: 0x0 RW47 data is 0x13
    rcd_pattern = re.compile(
        r"CHANNEL:\s*([0-9]+),\s*PHY:\s*([0-9]+),\s*PHYINIT:\s*\[MemDdr5RcdWriteWrapper\]SubChannel:\s*([0-9]+),\s*Dimm:\s*([0-9]+)\s*Page:\s*(0x[0-9A-Fa-f]+)\s*RW([0-9A-Fa-f]+)\s*data is\s*(0x[0-9A-Fa-f]+)"
    )
    ##CHANNEL: 0,  PHY: 0,  PHYINIT: BTFW: [DCSDLYSW] min_dly: 54, max_dly: 172, dlyStep: 1 at dcs0
    ##CHANNEL: 0,  PHY: 0,  PHYINIT: BTFW: [DCSTM] vref = 45, winMax = 118, vref_w = 45, dly_g = 113
    dcs_dly_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DCSDLYSW\]\s*min_dly:\s*(\d+),\s*max_dly:\s*(\d+),\s*dlyStep:\s*(\d+)\s*at\s*dcs(\d+)"
    )
    dcs_vref_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DCSTM\]\s*vref\s*=\s*(\d+),\s*winMax\s*=\s*(\d+),\s*vref_w\s*=\s*(\d+),\s*dly_g\s*=\s*(\d+)"
    )
    ##CHANNEL: 7,  PHY: 1,  PHYINIT: BTFW: [DCADLYSW]: pin:7 left:266 right:309 window:43 dlystep:1 dly:159
    ##CHANNEL: 7,  PHY: 1,  PHYINIT: BTFW: [DCATM] vref = 19, win = 43,  winMax = 58, vref_w = 58, dly_g = 160
    dca_dly_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DCADLYSW\]:\s*pin:(\d+)\s*left:(\d+)\s*right:(\d+)\s*window:(\d+)\s*dlystep:(\d+)\s*dly:(\d+)"
    )
    dca_vref_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DCATM\]\s*vref\s*=\s*(\d+),\s*win\s*=\s*(\d+),\s*winMax\s*=\s*(\d+),\s*vref_w\s*=\s*(\d+),\s*dly_g\s*=\s*(\d+)"
    )
    # Dictionary to store the latest Data value for each unique (Channel, SubChannel, Page, Register)
    dcs_dly = {}
    dcs_vref = {}
    dcs_win = {}
    dcs_eye = {}
    dca_dly = {}
    dca_vref = {}
    dca_win = {}
    dca_eye = {}
    # Process each line in the log
    with open(filename, "r") as file:
        previous_line = ""
        dimm = 0
        for line in file:
            rcd_match = rcd_pattern.search(line)
            dcsvref_match = dcs_vref_pattern.search(line)
            if dcsvref_match:
                dcsdly_match = dcs_dly_pattern.search(previous_line)
                if dcsdly_match:
                    channel, subchannel, vref, winMax, vrefMax, delayMax = (
                        dcsvref_match.groups()
                    )
                    channel2, subchannel2, left, right, dcs_step, cs_pin = (
                        dcsdly_match.groups()
                    )
                    if channel == channel2 and subchannel == subchannel2:
                        dcs_key = (
                            int(channel),
                            int(subchannel),
                            int(dimm),
                            int(cs_pin),
                        )  # Unique key for each entry
                        dcs_dly[dcs_key] = int(delayMax)  # Store the latest occurrence
                        dcs_vref[dcs_key] = int(vrefMax)
                        if dcs_key not in dcs_eye:
                            dcs_eye[dcs_key] = []
                        dcs_eye[dcs_key].append([int(vref), int(left)])
                        dcs_eye[dcs_key].append([int(vref), int(right)])
                        dcs_win[dcs_key] = int(winMax)
            dcavref_match = dca_vref_pattern.search(line)
            if dcavref_match:
                dcadly_match = dca_dly_pattern.search(previous_line)
                if dcadly_match:
                    channel, subchannel, ca_pin, left, right, window, step, delay = (
                        dcadly_match.groups()
                    )
                    channel2, subchannel2, vref, window2, winMax, vrefMax, delayMax = (
                        dcavref_match.groups()
                    )
                    if channel == channel2 and subchannel == subchannel2:
                        dcadly_key = (
                            int(channel),
                            int(subchannel),
                            int(ca_pin),
                        )  # Unique key for each entry
                        dca_dly[dcadly_key] = int(
                            delayMax
                        )  # Store the latest occurrence
                        dcavref_key = (
                            int(channel),
                            int(subchannel),
                            int(dimm),
                            int(ca_pin),
                        )
                        dca_vref[dcavref_key] = int(vrefMax)
                        dcaeye_key = (
                            int(channel),
                            int(subchannel),
                            int(dimm),
                            int(ca_pin),
                        )
                        if dcaeye_key not in dca_eye:
                            dca_eye[dcaeye_key] = []
                        dca_eye[dcaeye_key].append([int(vref), int(left)])
                        dca_eye[dcaeye_key].append([int(vref), int(right)])
                        dca_win[dcavref_key] = int(winMax)
            else:
                if rcd_match:
                    (rcd_channel, rcd_subchannel, sub, dimm, page, register, value) = (
                        rcd_match.groups()
                    )
            previous_line = line
    return dcs_dly, dcs_vref, dcs_win, dcs_eye, dca_dly, dca_vref, dca_win, dca_eye



def process_lines(prev2, prev1, curr, header_pattern, subheader_pattern, data_pattern, hex_enable):
    header_match = header_pattern.search(prev2)
    if not header_match:
        return []

    channel, subchannel, rank = header_match.groups()

    subheader_match = subheader_pattern.search(prev1)
    if not subheader_match:
        return []

    channel2, subchannel2 = subheader_match.groups()

    if channel != channel2 or subchannel != subchannel2:
        return []

    data_match = data_pattern.search(curr)
    if not data_match:
        return []

    groups = data_match.groups()
    if len(groups) != 12 or groups[0] != channel or groups[1] != subchannel:
        return []

    # Return list of (key, value) tuples
    if hex_enable:
        return [
            ((int(channel), int(subchannel), int(rank), i), int(groups[i + 2], 16))
            for i in range(10)
        ]
    else:
        return [
            ((int(channel), int(subchannel), int(rank), i), int(groups[i + 2]))
            for i in range(10)
        ]

def detect_qca_rank(curr):
    rank_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*<<---\s*Rank:(\d+)\s*--->>"
    )
    rank_match = rank_pattern.search(curr)
    if rank_match:
        channel, subchannel, rank = rank_match.groups()
        return int(rank)
    return -1

def detect_qca_eye_start(curr):
    header_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*<<-\s*2D\s*Eye\s*Print,\s*Qca\s*Eye\s*->>"
    )  
    header_match = header_pattern.search(curr)
    if header_match:
       channel, subchannel = header_match.groups()
       key = (channel, subchannel)
       return key, True
    return (), False
    
text="""
CHANNEL: 0,  PHY: 0,  PHYINIT: <<--- Rank:0 --->>
CHANNEL: 0,  PHY: 0,  PHYINIT: <<--- Nb:0 --->>
CHANNEL: 0,  PHY: 0,  PHYINIT: <<--- DelayOffset: NA, CenterDelay: NA, CenterVref: NA --->>
CHANNEL: 0,  PHY: 0,  PHYINIT: Train Eye EyePtsUpper: 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 56 67 75 84 92 94 94 94 94 94 94 94 94 94 92 82 75 64 57 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
CHANNEL: 0,  PHY: 0,  PHYINIT: Train Eye EyePtsLower: 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 54 45 39 38 38 38 38 38 38 38 38 38 38 38 38 38 38 43 51 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255
"""    
def process_qca_eye(prev3, prev2, prev1, curr, qca_start, rank):
    #pattern definition
    dev_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*<<---\s*Nb:(\d+)\s*--->>"
    )
    offset_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*<<---\s*DelayOffset:\s*NA,\s*CenterDelay:\s*NA,\s*CenterVref:\s*NA\s*--->>"
    )
    data_pattern=re.compile(
        r"Train Eye EyePts(.*?):(.*)"
    ) 
    #extract eye from log
    qca_eye={}    
    match = dev_pattern.search(prev3)
    if match:
        ch, sub, dev = match.groups()
        if qca_start[ch, sub]== True:
            match = offset_pattern.search(prev2)
            if match:
                match = data_pattern.search(prev1)
                if match:
                    eyepts, data= match.groups()
                    data2=[int(c) for c in data.split()]
                    if eyepts=='Upper':
                        qca_eye[int(ch), int(sub), int(rank), int(dev)]=[[i, val] for i, val in enumerate(data2) if val != 0]
                    else:
                        qca_eye[int(ch), int(sub), int(rank), int(dev)]=[[i, val] for i, val in enumerate(data2) if val != 255]
                    match = data_pattern.search(curr)
                    if match:
                        eyepts, data= match.groups()
                        data2=[int(c) for c in data.split()]
                        if eyepts=='Upper':
                            qca_eye[int(ch), int(sub), int(rank), int(dev)].extend([[i, val] for i, val in enumerate(data2) if val != 0])
                        else:
                            qca_eye[int(ch), int(sub), int(rank), int(dev)].extend([[i, val] for i, val in enumerate(data2) if val != 255]) 
    
    return qca_eye

    

def process_qcs_line(prev2, prev1, curr):
    header_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*<<\s*Rank:\s*(\d+),\s*QACSDelay\s*>>"
    )
    subheader_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*Dev0\s*\|\s*Dev1\s*\|\s*Dev2\s*\|\s*Dev3\s*\|\s*Dev4\s*\|\s*Dev5\s*\|\s*Dev6\s*\|\s*Dev7\s*\|\s*Dev8\s*\|\s*Dev9"
    )
    data_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*"
        r"(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*"
        r"(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*"
        r"(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)"
    )   
    result = process_lines(prev2, prev1, curr, header_pattern, subheader_pattern, data_pattern, True)
    return result

def process_qca_line(prev2, prev1, curr):
    header_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*<<\s*Rank:\s*(\d+),\s*QACADelay\s*>>"
    )
    subheader_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*Dev0\s*\|\s*Dev1\s*\|\s*Dev2\s*\|\s*Dev3\s*\|\s*Dev4\s*\|\s*Dev5\s*\|\s*Dev6\s*\|\s*Dev7\s*\|\s*Dev8\s*\|\s*Dev9"
    )
    data_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*"
        r"(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*"
        r"(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*"
        r"(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)"
    )      
    result = process_lines(prev2, prev1, curr, header_pattern, subheader_pattern, data_pattern, True)
    return result

def process_qcavref_line(prev2, prev1, curr):
    header_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*<<\s*Rank:\s*(\d+),\s*VrefCA\s*>>"
    )
    subheader_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*Dev0\s*\|\s*Dev1\s*\|\s*Dev2\s*\|\s*Dev3\s*\|\s*Dev4\s*\|\s*Dev5\s*\|\s*Dev6\s*\|\s*Dev7\s*\|\s*Dev8\s*\|\s*Dev9"
    )
    data_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*"
        r"(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*"
        r"(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*"
        r"(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)\s*\|\s*(0x[0-9a-fA-F]+)"
    )      
    result = process_lines(prev2, prev1, curr, header_pattern, subheader_pattern, data_pattern, True)
    return result

def process_wlcoarse_line(prev2, prev1, curr):
    header_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*<< Rank:\s*(\d+),\s*TxDQS\s*Coarse\s*Delay\s*>>"
    )
    subheader_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*Db0Nb0\s*\|\s*Db0Nb1\s*\|\s*Db1Nb0\s*\|\s*Db1Nb1\s*\|\s*Db2Nb0\s*\|\s*Db2Nb1\s*\|\s*Db3Nb0\s*\|\s*Db3Nb1\s*\|\s*Db4Nb0\s*\|\s*Db4Nb1"
    )
    data_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)"
    )    
    result = process_lines(prev2, prev1, curr, header_pattern, subheader_pattern, data_pattern, False)
    return result

def process_wlfine_line(prev2, prev1, curr):
    header_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*<< Rank:\s*(\d+),\s*TxDQS\s*Fine\s*Delay\s*>>"
    )
    subheader_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*Db0Nb0\s*\|\s*Db0Nb1\s*\|\s*Db1Nb0\s*\|\s*Db1Nb1\s*\|\s*Db2Nb0\s*\|\s*Db2Nb1\s*\|\s*Db3Nb0\s*\|\s*Db3Nb1\s*\|\s*Db4Nb0\s*\|\s*Db4Nb1"
    )
    data_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)"
    )    
    result = process_lines(prev2, prev1, curr, header_pattern, subheader_pattern, data_pattern, False)
    return result

def process_wlmr3_line(prev2, prev1, curr):
    header_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*<< Rank:\s*(\d+),\s*MR3\s*WICA\s*>>"
    )
    subheader_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*Db0Nb0\s*\|\s*Db0Nb1\s*\|\s*Db1Nb0\s*\|\s*Db1Nb1\s*\|\s*Db2Nb0\s*\|\s*Db2Nb1\s*\|\s*Db3Nb0\s*\|\s*Db3Nb1\s*\|\s*Db4Nb0\s*\|\s*Db4Nb1"
    )
    data_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)"
    )    
    result = process_lines(prev2, prev1, curr, header_pattern, subheader_pattern, data_pattern, False)
    return result

def process_wlmr7_line(prev2, prev1, curr):
    header_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*<< Rank:\s*(\d+),\s*MR7\s*0.5tCK\s*Offset\s*>>"
    )
    subheader_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*Db0Nb0\s*\|\s*Db0Nb1\s*\|\s*Db1Nb0\s*\|\s*Db1Nb1\s*\|\s*Db2Nb0\s*\|\s*Db2Nb1\s*\|\s*Db3Nb0\s*\|\s*Db3Nb1\s*\|\s*Db4Nb0\s*\|\s*Db4Nb1"
    )
    data_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*\[WL TRAIN\]\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)"
    )    
    result = process_lines(prev2, prev1, curr, header_pattern, subheader_pattern, data_pattern, False)
    return result

def process_rxen_coarse_line(prev2, prev1, curr):
    header_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*<< Rank:\s*(\d+),\s*RxEnCoarseDly\s*>>"
    )
    subheader_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*Db0Nb0\s*\|\s*Db0Nb1\s*\|\s*Db1Nb0\s*\|\s*Db1Nb1\s*\|\s*Db2Nb0\s*\|\s*Db2Nb1\s*\|\s*Db3Nb0\s*\|\s*Db3Nb1\s*\|\s*Db4Nb0\s*\|\s*Db4Nb1"
    )
    data_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)"
    )
    result = process_lines(prev2, prev1, curr, header_pattern, subheader_pattern, data_pattern, False)
    return result

def process_rxen_fine_line(prev2, prev1, curr):
    header_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*<< Rank:\s*(\d+),\s*RxEnFineDly\s*>>"
    )
    subheader_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*Db0Nb0\s*\|\s*Db0Nb1\s*\|\s*Db1Nb0\s*\|\s*Db1Nb1\s*\|\s*Db2Nb0\s*\|\s*Db2Nb1\s*\|\s*Db3Nb0\s*\|\s*Db3Nb1\s*\|\s*Db4Nb0\s*\|\s*Db4Nb1"
    )
    data_pattern=re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DBV_INFO\]\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)"
    )
    result = process_lines(prev2, prev1, curr, header_pattern, subheader_pattern, data_pattern, False)
    return result

def detect_decoded_log(filename):

    qcs_value = {}
    qca_value = {}
    qcavref_value = {}
    wlcoarse_value = {}
    wlfine_value = {}
    wlmr3_value = {}
    wlmr7_value = {}
    rxen_coarse_value = {}
    rxen_fine_value = {}
    rxdly_value = {}
    rxvref_value = {}
    txdly_value = {}
    txvref_value = {}
    txrank = 0
    qca_eye_start = {}
    qca_eye={}
    iod=0
    rawfile = os.path.basename(filename)
    if "iod1" in rawfile:
        socket = 0
        iod=1
    elif "iod0" in rawfile:
        iod=0
        socket = 0
    # Process each line in the log
    with open(filename, 'r') as file:
        # Read all lines from the file
        input_text = file.readlines()
        
    _, valid_text = sort_text_by_channel_phy(input_text)

    rank=0
    previous_line = ""
    previous_2line = ""
    previous_3line = ""
    previous_4line = ""
    previous_5line = ""    
    for line in valid_text:
        qca_key, qca_start= detect_qca_eye_start(line)
        if qca_start:
            qca_eye_start[qca_key] = qca_start
        temp = detect_qca_rank(line)
        if temp>0:
            rank=temp
        # Get QCA eye value
        temp_qca= process_qca_eye(previous_3line, previous_2line, previous_line, line, qca_eye_start, rank)
        if temp_qca:
            for key in temp_qca:
                qca_eye[socket, iod, key[0], key[1], key[2], key[3]] = temp_qca[key]    
        # Get QCS value
        for key, value in process_qcs_line(previous_2line, previous_line, line):
            qcs_value[socket, iod, key[0], key[1], key[2], key[3]] = value
        # Get QCA value
        for key, value in process_qca_line(previous_2line, previous_line, line):
            qca_value[socket, iod, key[0], key[1], key[2], key[3]] = value  
        # Get QCA Vref value
        for key, value in process_qcavref_line(previous_2line, previous_line, line):
            qcavref_value[socket, iod, key[0], key[1], key[2], key[3]] = value            
        # Get WL coarse value
        for key, value in process_wlcoarse_line(previous_2line, previous_line, line):
            wlcoarse_value[socket, iod, key[0], key[1], key[2], key[3]] = value
        # Get WL fine value
        for key, value in process_wlfine_line(previous_2line, previous_line, line):
            wlfine_value[socket, iod, key[0], key[1], key[2], key[3]] = value
        # Get WL MR3 value
        for key, value in process_wlmr3_line(previous_2line, previous_line, line):
            wlmr3_value[socket, iod, key[0], key[1], key[2], key[3]] = value
        # Get WL MR7 value
        for key, value in process_wlmr7_line(previous_2line, previous_line, line):
            wlmr7_value[socket, iod, key[0], key[1], key[2], key[3]] = value
       
        # Get RxEN Coarse value
        for key, value in process_rxen_coarse_line(previous_2line, previous_line, line):
            rxen_coarse_value[socket, iod, key[0], key[1], key[2], key[3]] = value
        # Get RxEN Fine value
        for key, value in process_rxen_fine_line(previous_2line, previous_line, line):
            rxen_fine_value[socket, iod, key[0], key[1], key[2], key[3]] = value

        previous_5line = previous_4line        
        previous_4line = previous_3line        
        previous_3line = previous_2line             
        previous_2line = previous_line
        previous_line = line    


    return qcs_value, qca_value, qcavref_value, wlcoarse_value, wlfine_value, wlmr3_value, wlmr7_value, rxen_coarse_value, rxen_fine_value, qca_eye


def process_data_no_dimm(data):
    result = []
    for key, value in data.items():
        soc, iod, channel, subchannel, rank, dev = key
        entry = {
            "Socket": soc,
            "IOD": iod,  
            "channel": channel,
            "subchannel(phy)": subchannel,
            "rank": rank,
            "dev": dev,
            "value/delay": value
        }
        result.append(entry)
    return result

def process_eyedata(data):
    result = []
    for key, value in data.items():
        for delay, vref in data[key]:
            soc, iod, channel, subchannel, rank, dev = key
            entry = {
                "Socket": soc,
                "IOD": iod,  
                "channel": channel,
                "subchannel(phy)": subchannel,
                "rank": rank,
                "dev": dev,
                "value/delay": delay,
                "vref": vref
            }
            result.append(entry)
    return result



def calculation(
    wlfine_value,
    wlcoarse_value,
    rxen_coarse_value,
    rxen_fine_value
):
    # WL
    wl_result = {}
    for key, value in wlcoarse_value.items():
        soc, iod, ch, sub, r, db = key
        ##DqsCoarseDly * 64 + stdqs_mdqs_dqs[ul]Txt_TxClkGenPiCode
        wl_result[key] = (value * 64) + wlfine_value[key]
    # RxEN
    rxen_result = {}
    for key, value in rxen_coarse_value.items():
        soc, iod, ch, sub, r, db = key
        ##int(row['RxDqsCoarseDlyTg DqsCoarseDly'])*128 + np.floor((int(row[f'RXDQS_{ul.upper()}_RDGATE_DL_CTRL srdqs_mdqs_dqs{ul}_RdGateDlCoarseSel'])*16 + int(row[f'RXDQS_{ul.upper()}_RDGATE_DL_CTRL srdqs_mdqs_dqs{ul}_RdGateDlPiCode']))/4)
        rxen_result[key] = (value * 128) + np.floor((rxen_fine_value[key])/4)
    return (
        wl_result, 
        rxen_result
    )        

def calculate_standard_deviation_and_range(analysis_csv):
    # Step 1: Read the CSV data
    df_analysis = pd.read_csv(analysis_csv)
    # Ensure that the 'trained_value' column is included in the columns of interest

    # Step 2: Identify the columns related to 'trained_value' and runX (dynamically find columns that start with 'run')
    columns_of_interest = ["value/delay"] + [col for col in df_analysis.columns if col.startswith("run")]

    # Step 3: Iterate through each row and calculate the standard deviation and range
    df_analysis["standard_deviation"] = df_analysis[columns_of_interest].std(axis=1, ddof=0)
    df_analysis["range"] = df_analysis[columns_of_interest].max(axis=1) - df_analysis[columns_of_interest].min(axis=1)

    # Step 4 Add pass/fail if range >7
    df_analysis["Pass_Fail"] = df_analysis["range"].apply(lambda x: "Fail" if x > 7 else "Pass")

    # Step 5 Check if 'Param' is 'MRL' and 'trained_value' is not between 14 and 17 for all run columns
    df_analysis["Pass_Fail"] = df_analysis.apply(
        lambda row: "Fail" if (row["Param"] == "MRL" and not (14 <= row["trained_value"] <= 17)) else row["Pass_Fail"],
        axis=1,
    )
    run_columns = [col for col in df_analysis.columns if col.startswith("run")]
    df_analysis["Pass_Fail"] = df_analysis.apply(
        lambda row: "Fail" if (row["Param"] == "MRL" and not all(14 <= row[col] <= 17 for col in run_columns)) else row["Pass_Fail"],
        axis=1,
    )

    # Step 6: Copy 'byte' value to new column 'nibble' for 'WL' or 'RXEN' params
    #df_analysis["nibble"] = df_analysis.apply(
    #    lambda row: row["nibble"] if row["Param"] in ["WL", "RXEN"] else "", axis=1
    #)
    # Step 7: Write the updated DataFrame back to the CSV
    df_analysis.to_csv(analysis_csv, index=False)

    # Step 8 Print out/return failures/all pass
    failures = df_analysis[df_analysis["Pass_Fail"] == "Fail"]

    # Step 9: Create a new DataFrame with the max of each range column for each param
    max_range_per_param = df_analysis.groupby("Param")["range"].max().reset_index()
    max_range_per_param.columns = ["Param", "Max Range"]

    # Print the new DataFrame
    print("Max range for each param:")
    print(max_range_per_param)
    if not failures.empty:
        print("Failing rows:")
        print(failures)
        return failures
    else:
        print("All Pass")
        return None


def process_decodedlog(
    filename, outputfile, run, inputbase, inputhost, inputbios, analysis_csv
):
    # dcs_dly, dcs_vref, dcs_win, dcs_eye, dca_dly, dca_vref, dca_win, dca_eye  = detect_DCS_DCA(filename)
    (
        qcs_value, 
        qca_value, 
        qcavref_value, 
        wlcoarse_value, 
        wlfine_value, 
        wlmr3_value, 
        wlmr7_value, 
        rxen_coarse_value, 
        rxen_fine_value,
        qca_eye
    ) = detect_decoded_log(filename)
    (
        wl_result, 
        rxen_result 
    ) = calculation(
        wlcoarse_value, 
        wlfine_value, 
        rxen_coarse_value, 
        rxen_fine_value
    )
    df_qcs = process_data_no_dimm(qcs_value)
    df_qcs = pd.DataFrame(df_qcs)
    df_qcs["Param"] = "QAQCS_Delay"

    df_qca = process_data_no_dimm(qca_value)
    df_qca = pd.DataFrame(df_qca)
    df_qca["Param"] = "QAQCA_Delay"

    df_qcavref = process_data_no_dimm(qcavref_value)
    df_qcavref = pd.DataFrame(df_qcavref)
    df_qcavref["Param"] = "QCA_Vref"

    df_wl = process_data_no_dimm(wl_result)
    df_wl = pd.DataFrame(df_wl)
    df_wl["Param"] = "WL_Value"

    df_wlmr3 = process_data_no_dimm(wlmr3_value)
    df_wlmr3 = pd.DataFrame(df_wlmr3)
    df_wlmr3["Param"] = "WL_MR3"

    df_wlmr7 = process_data_no_dimm(wlmr7_value)
    df_wlmr7 = pd.DataFrame(df_wlmr7)
    df_wlmr7["Param"] = "WL_MR7"    

    df_rxen = process_data_no_dimm(rxen_result)
    df_rxen = pd.DataFrame(df_rxen)
    df_rxen["Param"] = "RxEN_Value"

    df_qcaeye = process_eyedata(qca_eye)
    df_qcaeye = pd.DataFrame(df_qcaeye)
    df_qcaeye["Param"] = "QCA_eye"
    df = pd.concat(
        [
            df_qcs,
            df_qca,
            df_qcavref,
            df_wl,
            df_wlmr3,
            df_wlmr7,
            df_rxen,
            df_qcaeye
        ]
    ).reset_index(drop=True)
    hstnme = [inputhost]
    bios = [inputbios]
    df["Hostname"] = hstnme * len(df)
    df["BIOS"] = bios * len(df)
    df["Filename"] = inputbase
    df["run"] = run

    ordered_columns = [
        "Filename",
        "Hostname",
        "BIOS",
        "Param",
        "Socket",
        "IOD",           
        "channel",
        "subchannel(phy)",
        "rank",
        "dev",
        "value/delay",
        "vref",
        "run"
    ]

    df = df[ordered_columns]
    if os.path.exists(outputfile):
        df.to_csv(outputfile, mode="a", header=False, index=False)
    else:
        df.to_csv(outputfile, mode="w", header=True, index=False)    


    if analysis_csv:

        df_analysis = pd.concat(
            [
                df_qcs,
                df_qca,
                df_qcavref,
                df_wl,
                df_wlmr3,
                df_wlmr7,
                df_rxen
            ]
        ).reset_index(drop=True)
        ordered_columns_analysis = [
            "Param",
            "Socket",
            "IOD",           
            "channel",
            "subchannel(phy)",
            "rank",
            "dev",
            "value/delay"
        ]
        df_analysis = df_analysis[ordered_columns_analysis]

        if run == 0:
            df_analysis.to_csv(analysis_csv, mode="w", header=True, index=False)
        else:
            df_analysis = pd.read_csv(analysis_csv)
            trained_value_column = df["value/delay"]
            run_column_name = f"run{run}"
            df_analysis[run_column_name] = trained_value_column
            df_analysis.to_csv(analysis_csv, mode="w", header=True, index=False)

def log_to_csv(inputlog, jmp_output, analysis_output):
    run = 0
    hostname = ""
    bios = ""
    if len(inputlog) >1:
        for file in inputlog:
            base = os.path.splitext(os.path.basename(file))[0]
            bios, hostname = get_bios_hostname(base)
            try:
                print(f"start log debug: {analysis_output}")
                process_decodedlog(file, jmp_output, run, base, hostname, bios, analysis_output)
            except:
                print("LOG: Fail to process file: ",file) 
            run = run + 1
        #calculate_standard_deviation_and_range(analysis_output)
    else:
        base = os.path.splitext(os.path.basename(inputlog[0]))[0]
        bios, hostname = get_bios_hostname(base)
        process_decodedlog(inputlog[0], jmp_output, run, base, hostname, bios, "")
    print("csv file generated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Training value Processing")
    parser.add_argument("log", help="log file to process", default=None)
    args = parser.parse_args()
    run = 0
    hostname = ""
    bios = ""
    if os.path.isdir(args.log):
        log_files = get_files_from_directory(args.log)
        newdir, ext = os.path.splitext(os.path.abspath(log_files[0]))
        base = os.path.splitext(os.path.basename(log_files[0]))[0]
        if not os.path.exists(newdir):
            os.mkdir(newdir)
        out_csv = os.path.join(newdir, f"{base}__log_consolidated_jmp.csv")
        analysis_csv = os.path.join(newdir, f"{base}_log_analysis.csv")
        for file in log_files:
            base = os.path.splitext(os.path.basename(file))[0]
            bios, hostname = get_bios_hostname(base)
            process_decodedlog(file, out_csv, run, base, hostname, bios, analysis_csv)
            run = run + 1
        calculate_standard_deviation_and_range(analysis_csv)
    else:
        if os.path.exists(args.log):
            newdir, ext = os.path.splitext(os.path.abspath(args.log))
            base = os.path.splitext(os.path.basename(args.log))[0]
            if not os.path.exists(newdir):
                os.mkdir(newdir)
            out_csv = os.path.join(newdir, f"{base}_log_consolidated_jmp.csv")
            bios, hostname = get_bios_hostname(base)
            process_decodedlog(args.log, out_csv, run, base, hostname, bios, "")
        else:
            sys.exit(f"File {args.log} does not exist")
    print("csv file generated")


