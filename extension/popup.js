let currentHints = {};
let currentMode = "";
let currentSessionId = null;

// ---------------- GENERATE GUIDANCE ----------------

document.getElementById("generate").addEventListener("click", async () => {
    currentMode = document.getElementById("mode").value;

    try {
        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        // Prevent restricted pages
        if (!tab.url.startsWith("http")) {
            document.getElementById("level1").innerText =
                "Cannot access content on this page.";
            return;
        }

        // Inject content script dynamically
        await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ["content.js"]
        });

        // Get page content
        const pageContent = await new Promise((resolve) => {
            chrome.tabs.sendMessage(
                tab.id,
                { action: "getContent" },
                (response) => {
                    resolve(response ? response.content : "");
                }
            );
        });

        // Send request to backend
        const response = await fetch("http://127.0.0.1:5000/generate_hint", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                mode: currentMode,
                page_content: pageContent
            })
        });

        currentHints = await response.json();
        currentSessionId = currentHints.session_id;

        // Show Level 1
        document.getElementById("level1").innerText =
            "Level 1: " + currentHints.level1;

        // Reset lower levels
        document.getElementById("level2").innerText = "";
        document.getElementById("level3").innerText = "";

        document.getElementById("unlock2").style.display = "block";
        document.getElementById("unlock3").style.display = "none";

    } catch (error) {
        document.getElementById("level1").innerText =
            "Error accessing backend.";
    }
});


// ---------------- UNLOCK LEVEL 2 ----------------

document.getElementById("unlock2").addEventListener("click", async () => {

    document.getElementById("level2").innerText =
        "Level 2: " + currentHints.level2;

    document.getElementById("unlock3").style.display = "block";

    if (currentSessionId) {
        await fetch("http://127.0.0.1:5000/track_usage", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                mode: currentMode,
                level_unlocked: 2,
                session_id: currentSessionId
            })
        });
    }
});


// ---------------- UNLOCK LEVEL 3 ----------------

document.getElementById("unlock3").addEventListener("click", async () => {

    document.getElementById("level3").innerText =
        "Level 3: " + currentHints.level3;

    if (currentSessionId) {
        await fetch("http://127.0.0.1:5000/track_usage", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                mode: currentMode,
                level_unlocked: 3,
                session_id: currentSessionId
            })
        });
    }
});
