::python-3.6.8-amd64.exe
::mkdir C:\Django
::xcopy /s Kvest C:\Django\Kvest\
::xcopy startserver.bat C:\Django\
::%HOMEPATH%\AppData\Local\Programs\Python\Python36\Scripts\pip.exe install -r requirements.txt
xcopy startserver.bat %HOMEPATH%\Desktop
pause



