# Almaprinter

A Python Printer Daemon developed by the University of Geneva Library and dedicated to printing letters and slips from Alma Printout Queues

* Author: Pablo Iriarte, UNIGE Library - pablo.iriarte@unige.ch
* Creation date: 14.05.2024
* Last modifications on: 18.07.2025

## Install

Windows installers are available on the folder "install\soft"

1. Install Python 3 
2. Install Ghostscript and add to PATH "C:\Program Files\gs\gs10.03.1\bin"
3. Install html2pdf and add to PATH "C:\Program Files\wkhtmltopdf\bin"
4. Add the python libraries with pip: py -m pip install [library name]
    - requests
    - pywin32
    - pdfkit
    - html2text

## Flowchart
![](almaprinter.png)

## Alternatives and inspiration sources 

* **HoldSlipPrinter**: https://developers.exlibrisgroup.com/blog/print-daemon/ 
* **Ex Libris Alma Print Daemon**: https://developers.exlibrisgroup.com/blog/how-to-set-up-and-use-the-alma-print-daemon/ 
* **alma-print-nogui**: https://github.com/natliblux/alma-print-nogui 
* **Alma Printing With Powershell**: https://github.com/university-of-york/fmsys-alma-printing-api
* **PartKeeprPrintingService**: https://github.com/Boldie/PartKeeprPrintingService
