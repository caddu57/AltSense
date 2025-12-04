from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from transformers import BlipProcessor, BlipForConditionalGeneration, AutoTokenizer, AutoModelForSeq2SeqLM
from PIL import Image
import torch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
#  BLIP-Large (caption em inglês)
# ===============================
MODEL = "Salesforce/blip-image-captioning-large"
print("🔄 Carregando BLIP-Large...")

processor = BlipProcessor.from_pretrained(MODEL)
model = BlipForConditionalGeneration.from_pretrained(
    MODEL,
    torch_dtype=torch.float32,
    use_safetensors=False
)
model.eval()

# ===================================
#  Tradutor leve (inglês → português)
# ===================================
print("🔄 Carregando tradutor EN→PT...")

tok = AutoTokenizer.from_pretrained("unicamp-dl/translation-en-pt-t5")
translator = AutoModelForSeq2SeqLM.from_pretrained("unicamp-dl/translation-en-pt-t5")

translator.eval()


# ===================================
#     Função principal de caption
# ===================================
def generate_caption_en(image):
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=70,
            num_beams=5
        )

    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption.strip()


def translate_to_pt(text):
    encoded = tok(text, return_tensors="pt")
    with torch.no_grad():
        out = translator.generate(
            **encoded,
            max_new_tokens=80,
            num_beams=5
        )
    return tok.decode(out[0], skip_special_tokens=True).strip()

def remove_repetition(text):
    """
    Remove repetições consecutivas de frases, como:
    'X. X.' → 'X.'
    """
    parts = [p.strip() for p in text.split(".") if p.strip()]
    cleaned = []
    for p in parts:
        if not cleaned or cleaned[-1].lower() != p.lower():
            cleaned.append(p)
    return ". ".join(cleaned) + "."



@app.post("/caption")
async def caption_endpoint(file: UploadFile = File(...)):
    img = Image.open(file.file).convert("RGB")

    caption_en = generate_caption_en(img)
    caption_pt = remove_repetition(translate_to_pt(caption_en))


    return {
        "caption": caption_pt,
        "caption_en": caption_en
    }
