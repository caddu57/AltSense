console.log("[AltSense] content.js carregado");

chrome.runtime.onMessage.addListener(async (msg) => {
    if (msg.action !== "scan_images") return;

    console.log("[AltSense] Iniciando scan...");

    const imgs = [...document.querySelectorAll("img")];
    const withoutAlt = imgs.filter(i => !i.alt || i.alt.trim() === "");

    console.log("[AltSense] Imagens sem ALT:", withoutAlt);

    for (const img of withoutAlt) {
        const b64 = await toBase64(img.src);
        if (!b64) {
            console.log("[AltSense] Falha ao converter imagem.");
            continue;
        }

        chrome.runtime.sendMessage(
            { action: "caption", image: b64 },
            (caption) => {
                console.log("[AltSense] Caption recebido:", caption);

                if (caption) {
                    img.alt = caption;
                    img.setAttribute("data-altsense", "ok");
                } else {
                    console.warn("[AltSense] Sem caption.");
                }
            }
        );
    }
});

function toBase64(url) {
    return fetch(url)
        .then(r => r.blob())
        .then(blob => new Promise(resolve => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(blob);
        }))
        .catch(() => null);
}
