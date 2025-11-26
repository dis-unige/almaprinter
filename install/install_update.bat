rem derniŠre mise … jour : 22.05.2024
echo off
cls
:start
echo.
echo Installation et mise … jour du script d'impression pour Alma
echo --------------------------------------------------------------
echo Ce programme va copier ou remplacer le script sur votre disque dur
echo par la nouvelle version disponible sur I:\GT_transversaux\almaprinter
echo.
echo Veuillez choisir l'imprimante Alma correspondant … votre guichet :
echo 1. Uni Arve - BELS
echo 2. Uni Arve - ISE
echo 3. Uni Arve - Mathematiques
echo 4. Uni Arve - Observatoire
echo 5. Uni Bastions - Jura
echo 6. Uni Bastions - Battelle
echo 7. Uni Bastions - Philosophes
echo 8. Uni CMU
echo 9. Uni Mail
echo 0. DBU
echo --------------------------------------------------------------
set choice=
set /p choice=Appuyez sur un chiffre : 
if '%choice%'=='1' goto bels
if '%choice%'=='2' goto ise
if '%choice%'=='3' goto maths
if '%choice%'=='4' goto obs
if '%choice%'=='5' goto jura
if '%choice%'=='6' goto battelle
if '%choice%'=='7' goto philosophes
if '%choice%'=='8' goto cmu
if '%choice%'=='9' goto mail
if '%choice%'=='0' goto dbu
echo "%choice%" N'est pas un choix valable
echo.
goto start
:bels
set dist_ini=I:\GT_transversaux\almaprinter\install\configs\bels.ini
goto end
:ise
set dist_ini=I:\GT_transversaux\almaprinter\install\configs\ise.ini
goto end
:maths
set dist_ini=I:\GT_transversaux\almaprinter\install\configs\maths.ini
goto end
:obs
set dist_ini=I:\GT_transversaux\almaprinter\install\configs\obs.ini
goto end
:jura
set dist_ini=I:\GT_transversaux\almaprinter\install\configs\jura.ini
goto end
:battelle
set dist_ini=I:\GT_transversaux\almaprinter\install\configs\battelle.ini
goto end
:philosophes
set dist_ini=I:\GT_transversaux\almaprinter\install\configs\philosophes.ini
goto end
:cmu
set dist_ini=I:\GT_transversaux\almaprinter\install\configs\cmu.ini
goto end
:mail
set dist_ini=I:\GT_transversaux\almaprinter\install\configs\mail.ini
goto end
:dbu
set dist_ini=I:\GT_transversaux\almaprinter\install\configs\dbu.ini
goto end
:end
rem def des dossiers
set dist_dir=I:\GT_transversaux\almaprinter
set local_dir=C:\Temp\almaprinter
set local_ini=C:\Temp\almaprinter\config\printer.ini
rem Copie des dossiers
robocopy  %dist_dir% %local_dir% /MIR
rem Copie des fichiers ini
xcopy  %dist_ini% %local_ini% /y
echo --------------------------------------------------------------
echo Fin de l'installation ou mise … jour 
echo.
echo En cas de problŠme merci d'ouvrir un ticket sur helpDIS
echo.
echo Appuyez sur une touche pour terminer
echo --------------------------------------------------------------
pause>nul
exit


