# 📘 AltSense — Geração Automática de ALT Text com IA

Aumente a acessibilidade da web com um clique.

## 🧩 Sobre o Projeto

AltSense é uma ferramenta composta por:

🔌 Extensão Chrome — identifica imagens sem ALT text em qualquer página e gera descrições automaticamente.

🧠 Backend FastAPI + BLIP-Large — usa modelos de Visão+Linguagem para gerar descrições de alta qualidade.

🌎 Tradução/Refinamento PT-BR — todo output é limpo, objetivo e em português natural.

O objetivo é melhorar a acessibilidade digital, permitindo que usuários e administradores de site adicionem ALT texts com apenas um clique.

## 🚀 Funcionalidades
- Extensão Chrome

- Detecta automaticamente imagens sem alt-text
- Envia imagens para o backend

- Substitui/insere ALT text sem recarregar a página

- Interface simples com um único botão: Gerar ALT texts

- Backend

- Recebe imagens (file upload)

- Gera descrição com BLIP-Large

- Refina a descrição (opcional)

- Retorna resposta em JSON

## 🧱 Arquitetura
```bash
┌──────────────────────────┐
│     Extensão Chrome       │
│  content.js / popup.js    │
└──────────────┬───────────┘
               │ fetch
               ▼
┌──────────────────────────┐
│      FastAPI Backend      │
│  /caption (POST upload)   │
└──────────────┬───────────┘
               │ model.generate
               ▼
┌──────────────────────────┐
│     BLIP-Large (CPU)      │
│  + refinamento PT-BR      │
└──────────────────────────┘
```
## 🛠️ Instalação — Backend

1) Clonar o repositório
```bash
git clone https://github.com/caddu57/AltSense.git
cd AltSense
```
2) Build do Docker
```bash 
docker build -t altsense-blip .
```

3) Executar
```bash
docker run --rm -p 8000:8000 altsense-blip
```

Backend disponível em:
```bash
http://localhost:8000/docs
```


## 🧩 Instalação — Extensão Chrome
1. Abra o Google Chrome (ou Microsoft Edge).
2. Vá para:
```bash
chrome://extensions/
```
3. Ative o Modo desenvolvedor (canto superior direito).

4. Clique em "Carregar sem compactação".

5. Selecione a pasta extension/ do projeto.

6. Pronto ✅ — a extensão está ativa.

## 🧠 Modelo Utilizado

- BLIP-Large (Salesforce/blip-image-captioning-large)

- Execução em CPU

- Refinamento em PT-BR automático