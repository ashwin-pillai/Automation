# Title: EnVision_Consolidate.py
# Author: Ashwin Pillai
# Purpose: To modify instrument data files from various formats. Creating output files with only relevant data necessary.
#          Also able to join data files into a single columnized file which allows for import into other data repositories.

import pandas as pd
import numpy as np
import os 
import glob
import csv
import tkinter as tk
from tkinter import filedialog
import re

# Determine FileLocation Directory using directory lookup

def List_Files_Select(dirname):
    dirname = filedialog.askdirectory(initialdir='/',title='Please select Folder with Files to Condense')
    dirname=dirname+'/'
    files=[]
    for r,d,f in os.walk(dirname):      # r=root, d=directories, f=files
        for file in f:
            if '.txt' in file:                      # or '.csv' if CSV is needed also
                files.append(os.path.join(r,file))
                print(r,file)
    return(files)

# Range of columns/rows -- can be changed for 96 well plate or 1536 well plate - 384 well plate is the standard
def Determine_PlateType(plate_size): # Input 96 or 384 or 1536 for well name output ( i.e. A1 A2 A3 A4 )
    import string
    plate_size=str(plate_size)
    plate_columns = {'96':list(string.ascii_uppercase[:8]), '384':list(string.ascii_uppercase[:16]),'1536':['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF']}
    plate_number={'96':list(range(1,13)), '384':list(range(1,25)),'1536':list(range(1,37))}
    
    table=[]
    
    for let in plate_columns[plate_size]:
        for num in plate_number[plate_size]:
            table.append(let + str(num))            
    return(table)

def Determine_Slice_Dataframe(reply):

    if reply == 'Odd':
        return(slice(0,None,2))         # Odd rows/columns start at index 0
    elif reply =='Even':
        return(slice(1,None,2))         # Even rows/columns start at index 1
    else:
        a,b=reply.split('-')
        return(slice(int(a)-1,int(b)))  # Splits desired range into a slice to be used in Manipulation Function

    manipulation_dict={'Odd':0, 'Even':1}


def Modification_PlateData(df,run,row=None,col=None):
    
    if run =='Yes':
        return (df)                     # If no modification is required simply return same dataframe
    
    a = Determine_Slice_Dataframe(row)
    b = Determine_Slice_Dataframe(col)
    
    df = df.iloc[a,b]                   # Modify dataframe to user input
    return(df)

def FileName(input_filename):
    
    path, filename = os.path.split(input_filename)              # Path and Filename separated as variables
    path_processed = os.path.join(path, 'Processed_Files')      # Create Subfolder Name for Processed Files
    output = os.path.join(path_processed, filename)             # Output Filename & Location
    filename_shortened=(filename.split(sep="_"))[0]             # Barcode Identifier Only without Date information
    barcode=(filename.split(sep="."))[0]                        # Barcode Identifier

    return(path,filename,path_processed,output,filename_shortened,barcode)


# Parse EnVision Data File - single file input.

def ParseFile(input):
    
        data = [line.strip() for line in open(input) if re.findall('^[A-Z]\s([d]+)*[^-]+' , line)]   #Search through file and always find data block

        df = pd.DataFrame(data)
        df=df[0].str.split('\t', expand=True)   # Split Alphanumeric string with tab into separate columns
        df=df.iloc[:,1:]                        # This is the base format that is required before manipulation - only data block - Removes Letter from first column

        return(df)


#Consolidate Files from FileLocation - Turning original file formatted data into cleaned useful version of data.
    
def Consolidate_PlateData():
    
    Master_Files = List_Files_Select('')
            
    run = input('Do you want all data exported? - Reply Yes or No: ').capitalize()
    row = input('Enter Rows you want | Reply - Odd, Even, or a Range i.e. 1-10: ').capitalize()
    col = input('Enter Columns you want | Reply - Odd, Even, or a Range i.e. 1-10: ').capitalize()


    for file in Master_Files:
       
        (path,filename,path_processed,output,filename_shortened,barcode) = FileName(file)   # Name variables from FileName Function

        if not os.path.exists(path_processed):                                              # Create Subdirectory if doesn't already exist
            os.makedirs(path_processed)
        
        
        df = ParseFile(file)                                                                # Parse EnVision Data file and output as DataFrame
        final=Modification_PlateData(df,run,row,col)
        
        final.to_csv(output, mode='w', index =False, sep='\t', header = None)
        a = pd.read_csv(output, delimiter='\t', header =None)
        
    return(path_processed)
        


def Columnize_Data():
    
    
    CleanedFiles = Consolidate_PlateData()

    
    ColumnizeList = List_Files_Select(CleanedFiles)
    
    
    final_output = pd.DataFrame()
    
    for file in ColumnizeList:
        
        (path,filename,path_processed,output,filename_shortened,barcode) = FileName(file)   # Name variables from FileName Function
        
        df = pd.read_csv(file, header=None, delimiter = '\t')
        ds = df.values.tolist()
        ds=sum(ds,[])

        a = (list(zip([barcode]*384, Determine_PlateType(384), ds)))
        df = pd.DataFrame(a)
        final_output = final_output.append(df)


    final_output.to_csv(path+'//' +'Export.csv', index = False, header = ['Plate Information', 'Well', 'Count'])
    print('Data exported to this location : ', path+'//' +'Export.csv')
        
    
#Consolidate_PlateData()
Columnize_Data()


