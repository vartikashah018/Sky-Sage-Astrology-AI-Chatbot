async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();
    if (!message) return;

    addMessage("user", message);
    inputField.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        addMessage("bot", data.reply);
    } catch (error) {
        addMessage("bot", "⚠️ Error reaching the server.");
    }
}

function addMessage(sender, text) {
    const chatLog = document.getElementById("chat-log");
    const messageDiv = document.createElement("div");
    messageDiv.className = sender;
    messageDiv.innerText = text;
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
}
document.getElementById("send-button").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();
    if (!message) return;

    addMessage("user", message);
    inputField.value = "";

    const typing = document.getElementById("typing");
    typing.classList.remove("hidden");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        typing.classList.add("hidden");
        addMessage("bot", data.reply);
    } catch (error) {
        typing.classList.add("hidden");
        addMessage("bot", "⚠️ Couldn't reach the server.");
    }
}

function addMessage(sender, text) {
    const chatLog = document.getElementById("chat-log");
    const messageDiv = document.createElement("div");
    messageDiv.className = sender;
    messageDiv.innerHTML = sender === "bot" ?
        `<strong>Sky-Sage:</strong> ${text}` :
        text;
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
}
