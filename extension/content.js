// Extract basic visible text from page
function getPageContent() {
    let text = document.body.innerText;
    return text.substring(0, 2000); // limit size for now
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getContent") {
        sendResponse({ content: getPageContent() });
    }
});
