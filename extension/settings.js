document.addEventListener("DOMContentLoaded", () => {
    const modeEl = document.getElementById("detailMode");
    const msg = document.getElementById("msg");
    const btn = document.getElementById("saveBtn");

    chrome.storage.sync.get({ detailMode: "medio" }, (data) => {
        modeEl.value = data.detailMode;
    });

    btn.addEventListener("click", () => {
        chrome.storage.sync.set(
            { detailMode: modeEl.value },
            () => {
                msg.textContent = "Configurações salvas!";
                setTimeout(() => msg.textContent = "", 2000);
            }
        );
    });
});
