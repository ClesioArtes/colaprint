@echo off
setlocal
rem ============================================================
rem  Padrao Clesio Artes Miniapps v1.0 - instalador
rem  Para outro app, troque so as tres linhas abaixo.
rem ============================================================
set "APP=ColaPrint"
set "PRINCIPAL=colaprint.pyw"
set "LOG=colaprint_instalacao.txt"
rem ============================================================

title %APP% - Instalar
cd /d "%~dp0"
set "VERSAO=?"
if exist VERSION set /p VERSAO=<VERSION
cls
echo.
echo    %APP% %VERSAO%  -  um utilitario Clesio Artes
echo    ------------------------------------------------
echo.
echo %date% %time% - %APP% %VERSAO% > "%LOG%"

echo    [1/4] Conferindo os arquivos...
for %%F in ("%PRINCIPAL%" "requirements.txt" "VERSION") do (
  if not exist "%%~F" (
    echo          Falta o arquivo %%~F nesta pasta.
    echo Falta o arquivo %%~F >> "%LOG%"
    goto erro
  )
)
echo          ok

echo    [2/4] Conferindo o Python...
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >> "%LOG%" 2>&1
if errorlevel 1 goto sem_python
echo          ok

echo    [3/4] Instalando o que o %APP% precisa...
python -m pip install --disable-pip-version-check -r requirements.txt >> "%LOG%" 2>&1
if errorlevel 1 (
  echo          Nao deu certo. Ultimas linhas do registro:
  echo.
  powershell -NoProfile -Command "Get-Content -Path '%LOG%' -Tail 8 | ForEach-Object { '          ' + $_ }"
  goto erro
)
echo          ok

echo    [4/4] Criando os atalhos...
python "%PRINCIPAL%" --instalar >> "%LOG%" 2>&1
if errorlevel 1 (
  echo          Nao deu certo. Ultimas linhas do registro:
  echo.
  powershell -NoProfile -Command "Get-Content -Path '%LOG%' -Tail 8 | ForEach-Object { '          ' + $_ }"
  goto erro
)
echo          ok
echo.

start "" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\%APP%.lnk"
echo Instalacao concluida >> "%LOG%"
echo    ------------------------------------------------
echo    Pronto! %APP% %VERSAO% instalado e ligado.
echo.
echo    - Icone perto do relogio
echo    - Atalho na area de trabalho e no menu Iniciar
echo    - Como usar: abra o LEIA-ME.html
echo.
pause
exit /b 0

:sem_python
echo.
echo    Falta o Python neste computador (versao 3.9 ou mais nova).
echo.
echo    1. Baixe em  https://www.python.org/downloads/
echo    2. Na instalacao, marque "Add python.exe to PATH"
echo    3. Depois, rode este instalador de novo
echo.
pause
exit /b 1

:erro
echo.
echo    ------------------------------------------------
echo    A instalacao parou. O registro completo ficou em:
echo    %LOG%  (nesta pasta)
echo.
pause
exit /b 1
