@echo off
setlocal
rem ============================================================
rem  Padrao Clesio Artes Miniapps v1.0 - desinstalador
rem  Para outro app, troque so as duas linhas abaixo.
rem ============================================================
set "APP=ColaPrint"
set "PRINCIPAL=colaprint.pyw"
rem ============================================================

title %APP% - Desinstalar
cd /d "%~dp0"
cls
echo.
echo    %APP%  -  Desinstalar
echo    ------------------------------------------------
echo.
echo    Isto vai:
echo    - fechar o %APP%
echo    - tirar os atalhos
echo    - desligar o inicio automatico com o Windows
echo.
echo    O Python, as dependencias e os arquivos desta
echo    pasta continuam onde estao.
echo.
choice /c SN /n /m "   Continuar? [S/N] "
if errorlevel 2 (
  echo.
  echo    Nada foi alterado.
  echo.
  pause
  exit /b 0
)
echo.
python "%PRINCIPAL%" --desinstalar
if errorlevel 1 goto erro
echo    ------------------------------------------------
echo    Pronto! O %APP% foi desinstalado.
echo.
echo    Se quiser, agora pode apagar esta pasta.
echo.
pause
exit /b 0

:erro
echo.
echo    Algo nao saiu como esperado (detalhes acima).
echo    O registro tambem ficou no arquivo de erros do %APP%, nesta pasta.
echo.
pause
exit /b 1
