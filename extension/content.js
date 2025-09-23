async function processImages() {
    const images = document.querySelectorAll("img:not([alt]), img[alt='']");
    const urls = Array.from(images).map(img => img.src);

    if (urls.length === 0) {
        alert("Nenhuma imagem sem alt encontrada!");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/alt-text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ urls })
        });

        const data = await response.json();

        images.forEach(img => {
            const altText = data.results[img.src];
            if (altText && !altText.startsWith("Erro")) {
                img.alt = altText;
                console.log(`Alt adicionado para ${img.src}: ${altText}`);
                img.style.border = "2px solid green"; // visual feedback
            } else {
                console.log(`Erro ao gerar alt para ${img.src}: ${altText}`);
                img.style.border = "2px solid orange"; // sinaliza erro
            }
        });
    } catch (err) {
        console.error("Erro ao conectar com backend:", err);
    }
}

// Executa automaticamente quando a página é carregada
window.addEventListener("load", processImages);
