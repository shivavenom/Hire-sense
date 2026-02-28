@echo off
echo Creating AI Interview Frontend Structure...

:: Create frontend root
mkdir frontend
cd frontend

:: Create subfolders
mkdir css
mkdir js
mkdir assets
mkdir assets\images
mkdir assets\icons

:: -----------------------
:: HTML Files
:: -----------------------

type nul > index.html
type nul > interview.html
type nul > report.html

:: -----------------------
:: CSS Files
:: -----------------------

cd css
type nul > styles.css
type nul > interview.css
type nul > report.css
cd ..

:: -----------------------
:: JavaScript Files
:: -----------------------

cd js
type nul > api.js
type nul > app.js
type nul > interview.js
type nul > report.js
type nul > utils.js
cd ..

:: -----------------------
:: Optional Config File
:: -----------------------

type nul > config.js

cd ..

echo Frontend structure created successfully!
pause
