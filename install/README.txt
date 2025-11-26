# Code pour imprimer les bordereaux générés par Alma (jobs)

Auteur : Pablo Iriarte, UNIGE - pablo.iriarte@unige.ch

Installation :

    1. Installer Python 3 (lancer le fichier python-3.12.3-amd64.exe dans le dossier "almaprinter\install\soft")
    2. Installer Ghostscript (lancer le fichier gs10031w64.exe dans le dossier "almaprinter\install\soft") et modifier les variables d'environmment pour ajouter ce dossier au PATH : C:\Program Files\gs\gs10.03.1\bin
    3. Installer html2pdf (lancer le fichier wkhtmltox-0.12.6-1.msvc2015-win64.exe dans le dossier dans le dossier "almaprinter\install\soft") et modifier les variables d'environmment pour ajouter ce dossier au PATH : C:\Program Files\wkhtmltopdf\bin
    4. Dans une console ajouter les librairies python avec pip : py -m pip install [nom de la librairie]
        - pywin32
        - requests
        - pdfkit
        - html2text
    5. Copier les fichiers et dossiers en lançant le script qui se trouve sur I:\GT_transversaux\almaprinter\install\install_update.bat
    6. Copier les raccourcis "almaprinter", "almaprinter-fichiers-filtrés" et "almaprinter-fichiers-imprimés" sur le bureau à partir du dossier "shortcuts"
    7. Ajouter le raccourci au démarrage windows : copier ce même fichier sur C:\Users\[votre compte]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup


Mise à jour : 

    - Lancer le bat qui se trouve sur ce dossier ou sur I:\GT_transversaux\almaprinter\install\install_update.bat