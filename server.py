import base64
import io
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import (
    AutoProcessor,
    AutoModelForCausalLM,
    M2M100ForConditionalGeneration,
    M2M100Tokenizer
)

# ===============================
# 1) MODELO FLORENCE-2
# ===============================
FLORENCE_MODEL = "microsoft/Florence-2-large-ft"

print("🔄 Carregando Florence-2...")
processor = AutoProcessor.from_pretrained(FLORENCE_MODEL, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(FLORENCE_MODEL, trust_remote_code=True)
print("✅ Florence-2 carregado!")


# ===============================
# 2) TRADUTOR M2M100 (EN → PT)
# ===============================
print("🔄 Carregando tradutor...")
translator_name = "facebook/m2m100_418M"

translator_tokenizer = M2M100Tokenizer.from_pretrained(translator_name)
translator_model = M2M100ForConditionalGeneration.from_pretrained(translator_name)

translator_tokenizer.src_lang = "en"
translator_tokenizer.tgt_lang = "pt"
print("✅ Tradutor carregado!")


# ===============================
# FUNÇÕES AUXILIARES
# ===============================
def decode_image(b64):
    """Base64 → PIL.Image"""
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")


def florence_caption(img):
    """Gera legenda em inglês usando Florence (obrigatório inglês)."""

    # Florence exige texto **EXATAMENTE** = "<CAPTION>"
    inputs = processor(
        text="<CAPTION>",
        images=img,
        return_tensors="pt"
    )

    with torch.no_grad():
        output = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=256,
        )

    caption_en = processor.batch_decode(output, skip_special_tokens=True)[0]
    caption_en = caption_en.replace("<s>", "").replace("</s>", "").strip()

    return caption_en


def traduzir_para_pt(texto_en):
    """Traduz EN → PT-BR usando M2M100."""
    if not texto_en or texto_en.strip() == "":
        return ""

    encoded = translator_tokenizer(
        texto_en,
        return_tensors="pt"
    )

    generated_tokens = translator_model.generate(
        **encoded,
        forced_bos_token_id=translator_tokenizer.get_lang_id("pt")  # português
    )

    translated = translator_tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True
    )[0]

    return translated.strip()


# ===============================
# SERVIDOR FLASK
# ===============================
app = Flask(__name__)
CORS(app)

@app.post("/alt-text")
def alt_text():
    data = request.json
    if not data or "image" not in data:
        return jsonify({"error": "Envie { image: base64 }"}), 400

    try:
        img = decode_image(data["image"])
    except Exception as e:
        return jsonify({"error": f"Imagem inválida: {e}"}), 400

    # 1) Gera descrição em inglês
    raw_en = florence_caption(img)

    # 2) Traduz para português
    final_pt = traduzir_para_pt(raw_en)

    if final_pt.strip() == "":
        final_pt = "Não foi possível gerar a descrição."

    return jsonify({
        "description": final_pt,
        "raw_english": raw_en
    })


if __name__ == "__main__":
    print("🚀 Servidor iniciado em http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
