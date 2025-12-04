console.log("[AltSense] background.js carregado (FINAL)");

const API = "http://localhost:8000/caption";

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action !== "caption") return;

    handleCaption(msg, sendResponse);
    return true; // manter canal aberto (obrigatório!)
});

async function handleCaption(msg, sendResponse) {
    try {
        const base64 = msg.image.split(",")[1];

        const blob = b64toBlob(base64);
        const form = new FormData();
        form.append("file", blob, "img.jpg");

        console.log("[AltSense] Enviando imagem...");

        const resp = await fetch(API, { method: "POST", body: form });
        console.log("[AltSense] Status:", resp.status);

        const data = await resp.json();

        console.log("[AltSense] Caption recebido do backend:", data.caption);

        sendResponse(data.caption);

    } catch (err) {
        console.error("[AltSense] Erro:", err);
        sendResponse(null);
    }
}

function b64toBlob(b64) {
    const bytes = atob(b64);
    const arr = new Uint8Array(bytes.length);
    for (let i = 0; i < bytes.length; i++) {
        arr[i] = bytes.charCodeAt(i);
    }
    return new Blob([arr], { type: "image/jpeg" });
}
