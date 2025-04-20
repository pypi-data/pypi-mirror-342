from ZCurvePy import __version__
f"""
    This is the util module for runnable scripts of ZCurvePy

    We are happy to see that the APIs provided here are also
    useful for your project, so you can just use it in your
    Python scripts.

    Authors:    Zetong Zhang, Feng Gao
    Version:    { __version__ }
    Copyright:  Copyright 2025 TUBIC
    License:    MIT License
    Date:       2025-02-26
"""
import os
import sys
from subprocess import run
from Bio.SeqIO import parse
from Bio.SeqRecord import SeqRecord

# where the downloaded files saved
CACHE_PATH = "ncbi_acc_download"

def download_acc(acc, command_name=__name__, form='fasta'):
    """
    Download genome files as genbank from NCBI database
    by accession using ncbi-acc-download

    Args:
        acc (str):          comma-splited accesions (or a
                            text files stores accessions)
        command_name (str): the name of command. If the
                            script is not called by console
                            commands, it is set as the name
                            of the module defaultly. 
        form (str):         the format of to-download files
    Returns:
        ready (list):       The save paths of the files 
                            downloaded and are ready to use.
    """
    to_download, ready = None, []

    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)
    
    if acc.endswith(".txt"):
        file = open(acc, 'r')
        to_download = file.readlines()
        file.close()
    else:
        to_download = acc.split(',')
    
    for item in to_download:
        item = item.strip()

        if len(item) == 0:
            continue
            
        temp_path = item + '.fa' if form == 'fasta' else '.gbk'
        save_path = os.path.join(CACHE_PATH, temp_path)

        if not os.path.exists(save_path):
            run(f"ncbi-acc-download -F {form} {item}")
            if os.path.exists(temp_path):
                os.replace(temp_path, save_path)
                print(f'ncbi-acc-download: [infor] downloaded {save_path}')
            
        if not os.path.exists(save_path):
            print(f"{command_name}: [error] ncbi-acc-download failed to download {item}. ")
            sys.exit(0)

        ready.append(save_path)
    return ready

def extract_CDS(genome):
    """
    Extract all the CDSs sequence from annotated genome files.
    Usually a GenBank file.

    Args:
        genome (str):   path to the genome file
    
    Returns:
        CDSs (list):    a list of CDS records
    """
    CDSs, records = [], parse(genome, "genbank")

    for record in records:
        for feature in record.features:
            if feature.type == "CDS":
                name = feature.qualifiers['locus_tag'][0]
                start = feature.location.start
                end = feature.location.end
                CDS_seq = record.seq[start:end]

                if feature.location.strand == -1:
                    CDS_seq = CDS_seq.reverse_complement()

                CDS_record = SeqRecord(CDS_seq, id=name)
                CDSs.append(CDS_record)
    
    return CDSs


def has_gui():
    """
    Check whether the current system has GUI

    Returns:
        bool: whether the current system has GUI
    """
    # Linux
    if sys.platform.startswith('linux'):
        if not os.environ.get('DISPLAY'):
            return False
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            root.update()
            root.destroy()
            return True
        except Exception:
            return False
    # Windows
    elif sys.platform == 'win32':
        try:
            import tkinter as tk
            tk.Tk().withdraw()
            return True
        except Exception:
            try:
                from ctypes import windll
                return windll.user32.GetSystemMetrics(0) != 0
            except Exception:
                return False
    # Unsupported OS
    else:
        return False