#!/usr/bin/env python3.5

import re
import sys, os

"""
path_to_scan variable
Get real path where this script is located and saves in path_to_scan var
"""
scriptfile = __file__
realpath = os.path.realpath(scriptfile)
path_to_scan = os.path.dirname(realpath)

def main():
    try:
        for path, dirs, subdirs in os.walk(path_to_scan):
            for name in dirs:
                if name == "practice-exercise" or name == "practive-exercise":
                    dirname = os.path.join(path, name)
                    dirpath = os.path.basename(dirname)
                    dirnewpath = "practice-exercises"
                    newdir = os.path.join(path, dirnewpath)
                    print("Original name: "+dirname)
                    dirname = os.rename(dirname, newdir)
                    print("Updated name: "+newdir+"\n")
        else:
            print("No folders found with spelling errors.")
                    

    except:
        print("Error: can not execute script.")
        

if __name__ == "__main__":


    main()
                    
