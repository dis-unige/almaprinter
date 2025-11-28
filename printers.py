#!/usr/bin/env python
# coding: utf-8

# Code pour obtenir la liste des imprimantes et les ids qui sont utilisés dans le script d'impression
# 
# Auteur : Pablo Iriarte, UNIGE - pablo.iriarte@unige.ch
# Date de cération : 14.05.2024
# Date de dernière modification : 14.10.2024

import requests
import json
import pandas as pd

apikey = 'XXX'

# import de la liste (limitée à 100 imprimantes)
headers = {'accept': 'application/json'}
r = requests.get('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/conf/printers?library=ALL&printout_queue=ALL&name=ALL&code=ALL&limit=100&offset=0&apikey=' + apikey, headers=headers, timeout=mytimeout)

# print(r.text)
data = r.json()
if (len(data) > 0 and 'total_record_count' in data) :
	total_record_count = data['total_record_count']
	print ('total_record_count : ' + str(total_record_count))
			
# parser et ajouter les données au dataframe
df_printers = pd.DataFrame(columns=['id', 'code', 'name', 'email', 'library', 'printout_queue'])
if total_record_count > 0 :
    printers = data['printer']
    for printer in printers:
        printer_id = printer['id']
        if 'code' in printer :
            printer_code = printer['code']
        else :
            printer_code = ''
        if 'name' in printer :
            printer_name = printer['name']
        else :
            printer_name = ''
        if 'email' in printer :
            printer_email = printer['email']
        else :
            printer_email = ''
        if 'library' in printer :
            printer_library = printer['library']['desc']
        else :
            printer_library = ''
        if 'printout_queue' in printer :
            printer_printout_queue = printer['printout_queue']
        else :
            printer_printout_queue = ''
        df_printers = df_printers.append({'id' : printer_id,
                                    'code' : printer_code,
                                    'name' : printer_name,
                                    'email' : printer_email,
                                    'library' : printer_library,
                                    'printout_queue' : printer_printout_queue
                                    }, ignore_index=True)
									
df_printers.to_csv('export_printers.csv')
df_printers.to_excel('export_printers.xlsx')