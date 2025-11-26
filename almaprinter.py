#!/usr/bin/env python
# coding: utf-8

# Code pour imprimer les bordereaux générés par Alma (jobs)
# 
# Auteur : Pablo Iriarte, UNIGE - pablo.iriarte@unige.ch
# Date de cération : 14.05.2024
# Date de dernière modification : 18.07.2025
# 
# Alternatives et sources d'inspiration : 
# 
#  * https://github.com/ExLibrisGroup/alma-print-daemon
#  * https://github.com/natliblux/alma-print-nogui
#  * https://developers.exlibrisgroup.com/blog/print-daemon/
#  * https://github.com/Boldie/PartKeeprPrintingService
#  * https://github.com/university-of-york/fmsys-alma-printing-api

import os
import sys
import win32print
import requests
import json
import datetime
import pdfkit
import html2text
import time
import configparser

# version
soft_version = '18.07.2025'

# chargement de la config
configDefault = configparser.ConfigParser()
configDefault.read('config/config.ini')

configPrinter = configparser.ConfigParser()
configPrinter.read(['config/printer.ini'])

# [PRINTER]
if ('printer_id' in configPrinter['PRINTER']) and ('printer_alma' in configPrinter['PRINTER']):
    printer_id = configPrinter['PRINTER']['printer_id']
    printer_alma = configPrinter['PRINTER']['printer_alma']
else :
    print('ERREUR : il manque l\'imprimante Alma sur le fichier de configuration')
    sys.exit()

# [FILTRES]
mots_filtres = json.loads(configDefault['FILTRES']['mots_filtres'])
mots_from_unige = json.loads(configDefault['FILTRES']['mots_from_unige'])
mots_to_unige = json.loads(configDefault['FILTRES']['mots_to_unige'])
types_sans_filtre = json.loads(configDefault['FILTRES']['types_sans_filtre'])
                    
# [PARAMS]
apikey = configDefault['PARAMS']['apikey']
mytimeout = int(configDefault['PARAMS']['mytimeout'])
mypause = int(configDefault['PARAMS']['mypause'])
mystatus = configDefault['PARAMS']['mystatus']
mylimit = configDefault['PARAMS']['mylimit']
myfontmin = configDefault['PARAMS']['myfontmin']

headers = {'accept': 'application/json'}
printer_name = win32print.GetDefaultPrinter()

def log(txt):
    f = open('logs/almalog.txt', 'a')
    f.write(txt + '\n')
    f.close()
    
def logprint(txt):
    f = open('logs/printlog.txt', 'a')
    f.write(txt + '\n')
    f.close()

def printmyid(my_id) :
    my_file_pdf = str(my_id) + '.pdf'
    # imprimer le pdf
    print('Job ' + str(my_id) + ' : Impression lancée')
    log('Job ' + str(my_id) + ' : Impression lancée')
    mycmd = 'gswin64c.exe -dBATCH -dNOPAUSE -dNOSAFER -dNumCopies=1 -sDEVICE=mswinpr2 -sOutputFile="%printer%' + printer_name + '" "temp/pdf/' + my_file_pdf + '" >> logs/printlog.txt'
    os.system(mycmd)
    # déplacer le fichier dans le dossier "printed"
    os.replace('temp/pdf/' + my_file_pdf, 'printed/' + my_file_pdf)
    log('Job ' + str(my_id) + ' : Fichier déplacé sur printed/' + my_file_pdf)

def changestatus(my_id):
    # modifier le statut sur Alma
    try:
        r = requests.post('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/task-lists/printouts/' + my_id + '?op=mark_as_printed&apikey='+apikey, headers=headers, timeout=mytimeout)
    except:
        log('Job ' + my_id + ' : Modification du statut sur Alma Erreur -> TIMEOUT')
    else:
        # print('Status : ' + str(r.status_code))
        if (r.status_code == 200):
            log('Job ' + my_id + ' : Modification du statut sur Alma OK -> Printed')
        else:
            log('Job ' + my_id + ' : Modification du statut sur Alma Erreur -> Status code ' + str(r.status_code))


print('#######################################')
print('Outil d\'impression pour Alma')
print('Version : ' + soft_version)
print('Imprimante sur Alma : ' + printer_alma + ' (' + printer_id + ')')
print('Imprimante par défaut sur ce poste : ' + printer_name)

log('#######################################')
log('Lancement de l\'Outil d\'impression pour Alma')
log('Date et heure : ' + datetime.datetime.now().strftime('%d.%m.%Y %X'))
log('Imprimante : ' + printer_name)
log('#######################################')

# démarrage du script tous les X secondes
starttime = time.monotonic()
while True:
    print('#######################################')
    print('Date et heure : ' + datetime.datetime.now().strftime('%d.%m.%Y %X'))
    print('PAUSE DE ' + str(mypause) + ' SECONDES...')
    log('#######################################')
    log('Date et heure : ' + datetime.datetime.now().strftime('%d.%m.%Y %X'))
    
    time.sleep(mypause - ((time.monotonic() - starttime) % mypause))
    # requête pour trouver les travaux en cours
    total_record_count = 0
    myurl = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/task-lists/printouts?status=' + mystatus + '&printer_id=' + printer_id + '&limit=' + mylimit + '&offset=0&apikey=' + apikey
    try:
        r = requests.get(myurl, headers=headers, timeout=mytimeout)
    except:
        print('API Alma Erreur -> TIMEOUT')
        log('Request : ' + myurl)
        log('API Alma Erreur -> TIMEOUT')
    else:
        # log(r + '\nStatus : ' + str(r.status_code))
        if (r.status_code == 200):
            # extraction des valeurs à partir du JSON
            # print ('réponse : ' + r.text)
            data = r.json()
            if (len(data) > 0 and 'total_record_count' in data) :
                total_record_count = data['total_record_count']
                print('API Alma OK : ' + str(total_record_count) + ' jobs à imprimer trouvés')
                log('API Alma OK : ' + str(total_record_count) + ' jobs à imprimer trouvés')
        else : 
            print('API Alma Erreur -> ' + str(r.status_code))
            log('Request : ' + myurl)
            log('Status : ' + str(r.status_code))

    if total_record_count > 0 :
        printouts = data['printout']
        for printout in printouts:
            # dossier par défaut
            myfolder_txt = 'temp/txt/'
            myfolder_html = 'temp/html/'
            myfolder_pdf = 'temp/pdf/'
            # par défaut le document n'est pas à filtrer
            printout_filtrer = 0
            # par défaut le document n'est pas intra-unige
            printout_from_unige = 0
            printout_to_unige = 0
            # extraction des données pour chaque printout
            printout_id = printout['id']
            log('Alma Job : ' + printout_id)
            if 'printout' in printout :
                printout_printout = printout['printout']
            else :
                printout_printout = ''
            if 'date' in printout :
                printout_date = printout['date']
            else :
                printout_date = ''
            if 'size' in printout :
                printout_size = printout['size']
            else :
                printout_size = ''
            if 'source' in printout :
                printout_source = printout['source']
            else :
                printout_source = ''
            if 'status' in printout :
                printout_status = printout['status']['value']
            else :
                printout_status = ''
            if 'letter' in printout :
                printout_letter = printout['letter']
                printout_letter_text = html2text.html2text(printout_letter)
                # remplacement pour simplifier le text
                printout_letter_text = printout_letter_text.replace('⇨', 'Vers: ')
                printout_letter_text = printout_letter_text.replace('Vers :', 'Vers: ')
                printout_letter_text = printout_letter_text.replace('Depuis :', 'Depuis: ')
                printout_letter_text = printout_letter_text.replace('De :', 'Depuis: ')
                printout_letter_text = printout_letter_text.replace('De:', 'Depuis: ')
                printout_letter_text = printout_letter_text.replace('Bibliotheque proprietaire :', 'Depuis: ')
                printout_letter_text = printout_letter_text.replace('Bibliotheque proprietaire:', 'Depuis: ')
                printout_letter_text = printout_letter_text.replace('**', '')
                printout_letter_text = printout_letter_text.replace(':  ', ': ')
                printout_letter_text = printout_letter_text.replace(':  ', ': ')
                printout_letter_text = printout_letter_text.replace(':  ', ': ')
                printout_letter_text = printout_letter_text.replace(':  ', ': ')
                printout_letter_text = printout_letter_text.replace(':  ', ': ')
                printout_letter_text = printout_letter_text.replace(':  ', ': ')
                printout_letter_text = printout_letter_text.replace(':  ', ': ')
                # filtrer en fonction du contenu
                for mot_filtre in mots_filtres:
                    if mot_filtre in printout_letter_text:
                        printout_filtrer = printout_filtrer + 1
                for mot_from_unige in mots_from_unige:
                    if mot_from_unige in printout_letter_text:
                        printout_from_unige = printout_from_unige + 1
                for mot_to_unige in mots_to_unige:
                    if mot_to_unige in printout_letter_text:
                        printout_to_unige = printout_to_unige + 1
                # filtrer si from unige AND to unige
                if ((printout_from_unige > 0) and (printout_to_unige > 0)):
                    printout_filtrer = printout_filtrer + 1
                # ne pas filtrer certains types
                if printout_printout in types_sans_filtre:
                    printout_filtrer = 0
                    log('Type ' + printout_printout + ' sur la liste de types sans filtre')
                # enregistrer dans le dossier "filtered" en fonction du filtrage
                if (printout_filtrer > 0):
                    myfolder_pdf = 'filtered/'
                    print('Job ' + str(printout_id) + ' : Filtré car origine et destination UNIGE')
                    log('Job ' + str(printout_id) + ' : Filtré car origine et destination UNIGE')
                # enregistrer la lettre comme fichier txt
                # with open(myfolder_txt + str(printout_id) + '.txt', 'w', encoding='utf-8') as f:
                #     f.write(printout_letter_text)
                #     f.close()
                # enregistrer la lettre comme fichier html
                # with open(myfolder_html + str(printout_id) + '.html', 'w', encoding='utf-8') as f:
                #     f.write(printout_letter)
                #     f.close()
                # modifier le HTML pour éviter certains problèmes
                printout_letter = printout_letter.replace('<img src="externalId.png" alt="externalId">', '')
                printout_letter = printout_letter.replace('alt="logo" style="height:20mm">', 'alt="logo" style="display:none">')
                # enregistrer la lettre comme fichier html modifié
                # with open(myfolder_html + str(printout_id) + '_new.html', 'w', encoding='utf-8') as f:
                #     f.write(printout_letter)
                #     f.close()
                # enregistrer la lettre comme fichier pdf
                myoptions = {'minimum-font-size': myfontmin,}
                pdfkit.from_string(printout_letter, myfolder_pdf + str(printout_id) + '.pdf', options = myoptions)
                
                # imprimer le fichier
                if (printout_filtrer == 0):
                    logprint('#######################################')
                    logprint('Date et heure : ' + datetime.datetime.now().strftime('%d.%m.%Y %X'))
                    logprint('Alma Job : ' + printout_id)
                    printmyid(printout_id)
                # modifier le statut sur alma
                changestatus(printout_id)
                # logprint('Status non changé : ' + printout_id)
            else :
                print('ERREUR - aucun fichier HTML trouvé')
                log('ERREUR - aucun fichier HTML trouvé')


