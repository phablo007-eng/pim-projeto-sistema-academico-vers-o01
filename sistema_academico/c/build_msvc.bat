@echo off
setlocal
REM Script simples para compilar a DLL notas_basico.dll
REM Uso: abra "x64 Native Tools Command Prompt for VS" e execute este arquivo dentro da pasta c.

if not exist notas_basico.c (
  echo Arquivo notas_basico.c nao encontrado nesta pasta.
  exit /b 1
)

cl /EHsc /LD notas_basico.c /Fe:notas_basico.dll
if %ERRORLEVEL% NEQ 0 (
  echo FALHA NA COMPILACAO
  exit /b 1
)

echo Sucesso! Gerado notas_basico.dll
endlocal
