ipconfig | find "IPv4">myip.txt
FOR /F "delims=: tokens=2" %%a IN (myip.txt) do set var=%%a
CALL C:\Django\myvenv\Scripts\activate.bat
python C:\Django\myvenv\Kvest\manage.py runserver %var%:8000
pause


