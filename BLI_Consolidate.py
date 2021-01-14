#Date: 8/18/20
#Project: BLI_Consolidate.ipynb
#Purpose: To combine and organize all BLI assay data for hit picking - as well as export plate organization.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import re
import glob
import os

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
from IPython.core.display import display

directory = r'A:\Assay Development Team\Automation\BLI\JupyterNotebookAnalysis\Milestone_Independent' #Define Assay Load Files + Load

export_filename = 'Milestone' # Enter Project Name

# Classify different file types. Load | Assay | Export

assay_results=[]
load_count=[]
export_results=[]

# r=root, d=directories, f = files

for r,d, f in os.walk(directory):
    for file in f:
        if file.endswith(".csv"):
            if re.search('LoadCellCount',file):
                a=(os.path.join(r, file))
                load_count.append(a)
            elif re.search('export_results',file):
                a=(os.path.join(r, file))
                export_results.append(a)
            else:
                a=(os.path.join(r, file))
                assay_results.append(a)

#print('this is assay', assay_results, len(assay_results))
#print('\n')
#print('this is load', load_count, len(load_count))
#print('\n')
#print('this is export ', export_results, len(export_results))


#desired column headers
headers_load = ['Device_Id', 'Pen_Id', 'X_Pos', 'Y_Pos','Time_Stamp','Cell_Count_Verified','View']
headers_assay =['DeviceId', 'Pen_Id', 'IsPositiveVerified']
headers_export = ['DeviceId', 'PenId','WellPlateID','WellRow','WellColumn','NumCellsInPenBeforeUnpen',
                  'TimeStamp','ExportVolumeMicroLiters','IsUnpenSuccess','NestTempDegC','UnloadDurationSeconds','NestId']

complete_assay = pd.DataFrame()
total_load = pd.DataFrame()
export_plate = pd.DataFrame()

def label_function(a):               #Function to pull out label from filename of assay results
    file=(a.rsplit('\\')[-1])
    label=(file.rsplit('_')[3:5])
    return '_'.join(label)

# Complete Assay Results
for file in assay_results:
    AssayLabel=label_function(file)
    df = pd.read_csv(file, usecols=headers_assay)
    df['Label']=AssayLabel
    df = df.rename(columns={'DeviceId': 'Device_Id'})
    complete_assay=complete_assay.append(df)

# Complete Load Results
for file in load_count:
    df = pd.read_csv(file, usecols=headers_load)
    total_load=total_load.append(df)

# Complete Export Plate
for file in export_results:
    df=pd.read_csv(file,usecols=headers_export)
    df = df.rename(columns={'DeviceId': 'Device_Id', 'PenId': 'Pen_Id'})
    export_plate=export_plate.append(df)
    
complete_assay.reset_index(drop = True, inplace=True)
total_load.reset_index(drop = True, inplace=True)
complete_assay_pivot=complete_assay.pivot_table(index =['Device_Id','Pen_Id'], columns ='Label', values = 'IsPositiveVerified').reset_index()

# To merge Assay results with load cell count data
final = pd.merge(total_load, complete_assay_pivot,  how='left', left_on=['Device_Id','Pen_Id'], right_on =['Device_Id','Pen_Id']).sort_values(by=['Device_Id','Pen_Id'])
final_export = pd.merge(final,export_plate , how='outer',  left_on=['Device_Id','Pen_Id'], right_on =['Device_Id','Pen_Id']).sort_values(by=['Device_Id','Pen_Id'])

#Output into single file for Spotfire / Tableau Visualization
file_out = r'' + export_filename + '.csv'
file_export = r'' + export_filename + '_export.csv'
final.to_csv(file_out, index=False)
final_export.to_csv(file_export, index=False)

final
final_export
