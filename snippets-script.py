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

"""
def write_to_file(content,pathtosave,filename)
1.) Check if directory "pathtosave" exists, and create it if not.
2.) If exists a previously snippet file for a lesson, append new code to old one.
3.) else, create a new snippet file for a lesson and save content.
"""
def write_to_file(content,pathtosave,filename):
    try:
        if not os.path.exists(pathtosave):
            os.makedirs(pathtosave)
        if os.path.isfile(pathtosave+filename):
            initialcontent = read_from_file(pathtosave+filename)
            if content not in initialcontent:
                f = open(pathtosave+filename, "a")
                f.write(content)
                f.close()
        else:
            f = open(pathtosave+filename,"w+")
            f.write(content)
            f.close()
    except:
        print("Error: can not open "+filename+" destination file.\n Check that folder name is exactly: 'lab-activities' or 'practice-exercises'.")           

"""
def read_from_file(filename)
Read and return content from a filename.
"""
def read_from_file(filename):
    try:
        f = open(filename,"r", encoding='utf-8')
        content = f.read()
        f.close()
        return content
    except:
        print("Error: can not open "+ filename +" original file.")

"""
def search_and_copy(content)
Copy and paste file path of content from file.
Read and return content from a filename.
"""
def search_and_copy(content, path):
    finalcode = ''
    goodpath = ''
    if "practice-exercises" in path:
        goodpath = path.split('practice-exercises')[1].replace("\instructions\\", '\\')
    elif "lab-activities" in path:
        goodpath = path.split('lab-activities')[1].replace("\instructions\\", '\\')
    elif "mla" in path:
        goodpath = path.split('mla')[1].replace("\instructions\\", '\\')
    elif "capstone" in path:
        goodpath = path.split('capstone')[1].replace("\instructions\\", '\\')
    if content != None:
        content = content.replace('```\n', 'codeblock102')
        content = content.replace('```', 'codeblock102')
        code = re.findall(r"codeblock102((.|\n)*?)codeblock102", content)
        for one in code:
            finalcode =   finalcode + str(one[0]) + "\n"
        finalcode = goodpath[1:] + "\n" + finalcode + "--------------------\n"
        
    return finalcode


"""
def pathtosave(pathtofile)
Create and return the exact path to save snippets files acording to original location of "instructions" folder.
Actual save paths options are: "lab-activities" or "practice-exercises"
"""
def pathtosave(pathtofile):
    value = ""
    if "lab-activities" in pathtofile:
        value = pathtofile.split('lab-activities')[0]+'lab-activities\snippets\\'
    elif "practice-exercises" in pathtofile:
        value = pathtofile.split('practice-exercises')[0]+'practice-exercises\snippets\\'
    elif "mla" in pathtofile:
        value = pathtofile.split('mla')[0]+'mla\snippets\\'
    elif "capstone" in pathtofile:
        value = pathtofile.split('capstone')[0]+'capstone\snippets\\'
    return value

"""
def filenametosave(pathtofile)
Read pathtofile name and, create a friendly name for file saving. That name will be "title of module_snippets.txt".
"""
def filenametosave(pathtofile):
    filename = ""
    if "lesson-" in pathtofile:
        filename = pathtofile.split('lesson-')[1]
        filename = filename.split('\\')[0]+'_snippets.txt'
    elif "mla" in pathtofile:
        filename = pathtofile.split('module-')[1]
        filename = filename.split('\\')[0]+'_snippets.txt'
    elif "capstone" in pathtofile:
        filename = 'capstone_snippets.txt'
    return filename

"""
def main()
Main function. Proccess:
1.) Loop to scan all folders, subfolders, files
2.) Check if exists a "instructions" folder. If so:
3.) Read content of each file inside "instructions" folder and extract code locate between ``` patterns.
4.) Create or append to a unique snippet file per lesson extracted code.
"""
def main():
    try:
        for path, subdirs, files in os.walk(path_to_scan):
            for name in files:
                fullpathtofile = os.path.join(path, name)
                line_to_search = "```"
                if "instructions" in fullpathtofile and "md" in fullpathtofile:
                    content = read_from_file(fullpathtofile)
                    if line_to_search in content:
                        extractedcode = search_and_copy(content, fullpathtofile)
                        if extractedcode != None:                    
                            filenamesaving = filenametosave(fullpathtofile)
                            if filenamesaving:
                                pathsaving = pathtosave(fullpathtofile)
                                print("Read: " + fullpathtofile)
                                write_to_file(extractedcode, pathsaving, filenamesaving)
                                print("Created: " + pathsaving + filenamesaving + "\n")
    
    except Exception as e:
        print("Error: can not execute script: ")
        print(e)
    


if __name__ == "__main__":
    main()
    
