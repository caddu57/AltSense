document.getElementById("checkImages").addEventListener("click", async () => {
    // Executa script na aba atual
    chrome.scripting.executeScript({
        target: { tabId: (await chrome.tabs.query({ active: true, currentWindow: true }))[0].id },
        func: () => {
            const event = new Event("load"); // dispara processImages do content.js
            window.dispatchEvent(event);
        }
    });
});
