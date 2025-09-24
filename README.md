# AltSense

AltSense é uma extensão de navegador que detecta automaticamente imagens sem **alt text** em páginas da web e gera descrições automáticas usando inteligência artificial.
## Funcionalidades

- Detecta imagens sem alt text.
- Gera descrições automáticas usando um modelo de visão computacional.
- Fácil instalação como extensão de navegador.
- Integração com backend hospedado (Flask).

## Instalação e uso

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/AltSense.git
cd AltSense
```
2. Crie um ambiente virtual (opcional, mas recomendado):
```bash 
2. python -m venv venv
# Linux/Mac
source venv/bin/activate  
# Windows
venv\Scripts\activate
```

3.Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o servidor:
```bash
python server.py
```

O servidor ficará disponível em:
👉 http://127.0.0.1:5000

## 🌐 Extensão do Navegador
1. Abra o Google Chrome (ou Microsoft Edge).
2. Vá para:
```bash
chrome://extensions/
```
3. Ative o Modo desenvolvedor (canto superior direito).

4. Clique em "Carregar sem compactação".

5. Selecione a pasta extension/ do projeto.

6. Pronto ✅ — a extensão está ativa.

## ▶️ Uso
- Acesse qualquer página da web.

- A extensão detectará imagens sem alt text automaticamente.

- Cada imagem encontrada será enviada ao backend Flask.

- O backend gera uma descrição com BLIP e retorna para a página.

- O alt text é adicionado diretamente no código da imagem.

## 🧪 Teste Manual da API
Se quiser testar a API do backend sem a extensão, use PowerShell:
```bash
$body = @{ urls = @("https://i.imgur.com/dhJpv38.jpg") } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5000/alt-text" -Method POST -Body $body -ContentType "application/json"
```
Resposta esperada:
```bash
{
  "results": {
    "https://i.imgur.com/dhJpv38.jpg": "Descrição gerada pelo modelo"
  }
}
```