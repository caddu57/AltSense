document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("scanPage");
    const statusEl = document.getElementById("status");

    btn.addEventListener("click", () => {
        statusEl.textContent = "Carregando configurações...";

        chrome.storage.sync.get(
            { detailMode: "medio" },
            (data) => {
                const modo = data.detailMode;

                statusEl.textContent = "Iniciando análise...";

                chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                    if (!tabs || !tabs[0]) {
                        statusEl.textContent = "Nenhuma aba ativa.";
                        return;
                    }

                    chrome.tabs.sendMessage(
                        tabs[0].id,
                        { action: "processar", modo: modo },
                        () => {
                            statusEl.textContent = "Processamento iniciado!";
                        }
                    );
                });
            }
        );
    });
});
