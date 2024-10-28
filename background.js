

// Listen for HTTP requests
chrome.webNavigation.onCompleted.addListener(
    (details) => {
        const url = new URL(details.url);
        const domain = url.hostname;

        console.log(`Tracked domain visited: ${domain}`);
        // You could also save this to storage if you want to track statistics
        chrome.storage.local.get({ visitedDomains: [] }, (data) => {
            const visitedDomains = data.visitedDomains;
            visitedDomains.push(domain);
            chrome.storage.local.set({ visitedDomains });
        });
    },
    { url: [{ schemes: ["http", "https"] }] }
);
