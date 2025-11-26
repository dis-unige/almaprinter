# Almaprinter

A Python Printer Daemon developed by the University of Geneva Library and dedicated to printing letters and slips from Alma Printout Queues

* Author: Pablo Iriarte, UNIGE Library - pablo.iriarte@unige.ch
* Creation date: 14.05.2024
* Last modifications on: 18.07.2025

## Alternatives and inspiration sources 

* https://github.com/ExLibrisGroup/alma-print-daemon
* https://github.com/natliblux/alma-print-nogui
* https://developers.exlibrisgroup.com/blog/print-daemon/
* https://github.com/Boldie/PartKeeprPrintingService
* https://github.com/university-of-york/fmsys-alma-printing-api


## Installation

Windows installer files are available on the folder "install\soft"

1. Insatll Python 3 
2. Install Ghostscript and add to PATH "C:\Program Files\gs\gs10.03.1\bin"
3. Install html2pdf and add to PATH "C:\Program Files\wkhtmltopdf\bin"
4. Add the python  libraries with pip: py -m pip install [library name]
    - pywin32
    - requests
    - pdfkit
    - html2text

