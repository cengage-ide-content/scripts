import re
import sys, os
import xlrd

scriptfile = __file__
realpath = os.path.realpath(scriptfile)
path_to_scan = os.path.dirname(realpath)

# ------------------- CONFIGURE LINES -------------------- #

excel_filename = path_to_scan + '\filename.txt'
sheet_name = 'sheetname'


'''
def get_excel_column_values(excel_filename,sheet_name,column)
Reads scpreadsheet column number indicated in column variable and return
its values as a list.
'''
def get_excel_column_values(excel_filename,sheet_name,column):
    try:
        workbook = xlrd.open_workbook(excel_filename)
        sheet = workbook.sheet_by_name(sheet_name)
        x = []
        for value in sheet.col_values(column):
            if isinstance(value, str):
                x.append("!["+value+"]")
        x.pop(0)
        return x
    except:
        print("Error: can not read excel file column number "+column)


'''
def get_mdfiles()
Looks for .md files into folders and return a list with files founds.
'''
def get_mdfiles():
    mdfiles = []
    try:
        for path, subdirs, files in os.walk(path_to_scan):
            for name in files:
                fullpathtofile = os.path.join(path, name)
                if name.endswith('.md'):
                    mdfiles.append(fullpathtofile)
        return mdfiles        
    except:
        print("Error: can not execute script.")  


'''
def read_from_file(filename)
Reads and return content from a filename.
'''
def read_from_file(filename):
    try:
        f = open(filename,"r", encoding="utf-8")
        content = f.read()
        f.close()
        return content
    except:
        print("Error: can not open "+filename+" for reading file.")


'''
def wwrite_to_file(content,filename)
Creates and writes into a finlename content.
'''
def write_to_file(content,filename):
    try:
        f = open(filename,"w",encoding="utf-8")
        f.write(content)
        f.close()
    except:
        print("Error: can not open "+filename+" for writing file.")   

'''
def print_non_modified_mdfiles(mdfile,mdfilesmodified,labels,mdcontent,alt_texts)
Prints/return string with all filenames that includes labels different from the ones that
appears in spreadsheet ones and that could not be replaced because of this.
1.) labelsalt contains value of labels found into files
2.) Compares if each labelsalt is different from good labens in spreadsheet
3.) If so, adds filename to list of Non-modified filename string list to print out.
'''
def print_non_modified_mdfiles(mdfile,mdfilesmodified,labels,mdcontent,alt_texts):
    labelsalt = re.findall(r'!\[(.*)\]', mdcontent)
    newlabel=False
    j=0
    for x in labelsalt:
        labelsalt[j]="!["+x+"]"
        j+=1
    for x in labelsalt:
        if (x not in labels):
            if(x not in alt_texts):
                newlabel=True
    if newlabel:
        if mdfile not in mdfilesmodified:
            #print("Non-modified: "+mdfile)
            return "Non-modified: "+mdfile+"\n"
        else:
            return ''
    else:
        return ''


'''
def main()
Main function. Proccess:
1.) Creates list "labels" after reading it from spreadsheet column
2.) Creates list "alt_texts" after reading it from spreadsheet column
3.) Read content of each file inside "instructions" folders and replace each label that matches "labels" list with its correct alt_texts list value.
4.) Print list of modified files and list of non-modified files.
'''
def main():
    try:
        mdfilesmodified = []
        allnonmodified = ''
        labels = get_excel_column_values(excel_filename,sheet_name,2) # value 2 reads 2th column
        alt_texts = get_excel_column_values(excel_filename,sheet_name,4) # reads 4th column
        for mdfile in get_mdfiles():
            if "instructions" in mdfile:
                mdcontent = read_from_file(mdfile)
                mdcontent2 = ''
                i=0
                for label in labels:
                    #label = label.replace("–","-")
                    if label in mdcontent:                        
                        mdcontent2 = mdcontent.replace(label,alt_texts[i])
                        mdfilesmodified.append(mdfile)
                        print("Modified: "+mdfile)                        
                    i = i+1           
                if mdcontent2!='':
                    write_to_file(mdcontent2,mdfile)
                allnonmodified += print_non_modified_mdfiles(mdfile,mdfilesmodified,labels,mdcontent,alt_texts)
        print("\n"+allnonmodified)
        print("DONE. Read alt text from excel spreadsheet and written to .md files.")
    except:
        print("Error: can not execute script.")            


if __name__ == "__main__":


    main()


