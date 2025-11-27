@echo off
echo ===========================================
echo     AltSense - Script de Instalacao
echo ===========================================
echo.

REM --- Verifica se o venv existe ---
if not exist "venv" (
    echo [INFO] Criando ambiente virtual...
    "C:\Program Files\Python310\python.exe" -m venv venv
)

echo [INFO] Ativando venv...
call venv\Scripts\activate

echo.
echo ===========================================
echo  Instalando PyTorch CPU (Windows)
echo ===========================================
pip install torch==2.2.2+cpu torchvision==0.17.2+cpu torchaudio==2.2.2+cpu --index-url https://download.pytorch.org/whl/cpu

echo.
echo ===========================================
echo  Instalando dependencias principais
echo ===========================================
pip install flask flask-cors pillow transformers sentencepiece sacremoses

echo.
echo ===========================================
echo  Instalacao finalizada!
echo  Para rodar o servidor, execute:
echo      venv\Scripts\activate
echo      python server.py
echo ===========================================
pause
