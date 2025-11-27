console.log("[AltSense] Content script ativo.");

async function gerarAltParaImagem(base64, modo) {
    try {
        const response = await fetch("http://127.0.0.1:5000/alt-text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: base64, mode: modo })
        });

        if (!response.ok) {
            console.error("[AltSense] Backend retornou erro:", response.status);
            return null;
        }

        const json = await response.json();
        console.log("[AltSense] Resposta do backend:", json);
        return json.description || null;

    } catch (err) {
        console.error("[AltSense] Erro ao conectar ao backend:", err);
        return null;
    }
}


// Converte imagem para base64, mas ignora imagens tainted
function converterParaBase64(img) {
    return new Promise((resolve, reject) => {
        try {
            const canvas = document.createElement("canvas");
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;

            const ctx = canvas.getContext("2d");

            ctx.drawImage(img, 0, 0);

            const dataUrl = canvas.toDataURL("image/jpeg");
            resolve(dataUrl.split(",")[1]);

        } catch (e) {
            console.warn("[AltSense] Canvas tainted, ignorando imagem.");
            reject(e);
        }
    });
}

async function processarPagina(modo) {
    console.log("[AltSense] Iniciando processamento... modo:", modo);

    const imagens = Array.from(document.querySelectorAll("img"));
    console.log(`[AltSense] Encontradas ${imagens.length} imagens.`);

    for (const img of imagens) {
        try {
            const base64 = await converterParaBase64(img)
                .catch(() => null);

            if (!base64) {
                console.log("[AltSense] Imagem ignorada (tainted).");
                continue;
            }

            const descricao = await gerarAltParaImagem(base64, modo);

            if (descricao) {
                img.alt = descricao;
                console.log("[AltSense] ALT aplicado:", descricao);
            } else {
                console.log("[AltSense] Nenhuma descrição retornada.");
            }

        } catch (err) {
            console.error("[AltSense] Erro ao processar imagem:", err);
        }
    }

    console.log("[AltSense] Processamento FINALIZADO.");
}


// Listener principal
chrome.runtime.onMessage.addListener((msg) => {
    if (msg.action === "processar") {
        console.log("[AltSense] Mensagem recebida do popup:", msg);
        processarPagina(msg.modo || "medio");
    }
});
