document.addEventListener("DOMContentLoaded", () => {
    chrome.storage.local.get("visitedDomains", (data) => {
        const domainList = data.visitedDomains || [];
        const domainListDiv = document.getElementById("domainList");
        domainListDiv.innerHTML = domainList
            .map(domain => `<p>${domain}</p>`)
            .join("");
    });
});
