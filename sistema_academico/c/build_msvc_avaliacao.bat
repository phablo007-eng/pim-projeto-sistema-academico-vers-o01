@echo off
setlocal
REM Compila notas_avaliacao.c em notas_avaliacao.dll
REM Uso: abrir "x64 Native Tools Command Prompt for VS" e executar dentro desta pasta

if not exist notas_avaliacao.c (
  echo Arquivo notas_avaliacao.c nao encontrado nesta pasta.
  exit /b 1
)

cl /EHsc /LD notas_avaliacao.c /Fe:notas_avaliacao.dll
if %ERRORLEVEL% NEQ 0 (
  echo FALHA NA COMPILACAO
  exit /b 1
)

echo Sucesso! Gerado notas_avaliacao.dll
endlocal
