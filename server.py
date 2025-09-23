from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from io import BytesIO
from PIL import Image
import os

# Ajuste aqui para o caminho local do modelo BLIP
LOCAL_MODEL_PATH = "./blip-image-captioning-base"

from transformers import BlipProcessor, BlipForConditionalGeneration

app = Flask(__name__)
CORS(app)  # Libera todas as origens

# Inicializa modelo e processor
processor = BlipProcessor.from_pretrained(LOCAL_MODEL_PATH)
model = BlipForConditionalGeneration.from_pretrained(LOCAL_MODEL_PATH)

# Pasta temporária para fallback
os.makedirs("temp_images", exist_ok=True)

@app.route("/alt-text", methods=["POST"])
def alt_text():
    data = request.json
    urls = data.get("urls", [])
    results = {}

    for url in urls:
        try:
            # Download da imagem com User-Agent
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10, verify=False)  # verify=False para SSL problemático
            img_bytes = BytesIO(response.content)
            img = Image.open(img_bytes).convert("RGB")
        except Exception as e:
            # Fallback: salva localmente
            try:
                filename = os.path.join("temp_images", os.path.basename(url))
                with open(filename, "wb") as f:
                    f.write(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=False).content)
                img = Image.open(filename).convert("RGB")
            except Exception as e2:
                results[url] = f"Erro: {e2}"
                continue

        try:
            # Processa imagem com BLIP
            inputs = processor(images=img, return_tensors="pt")
            out = model.generate(**inputs)
            alt = processor.decode(out[0], skip_special_tokens=True)
            results[url] = alt
        except Exception as e:
            results[url] = f"Erro: {e}"

    return jsonify({"results": results})

if __name__ == "__main__":
    print("Servidor rodando em http://127.0.0.1:5000")
    app.run(debug=True)
