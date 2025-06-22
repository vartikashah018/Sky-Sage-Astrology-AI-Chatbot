// script.js (final version with typing + sound + better structure)
const inputField = document.getElementById("user-input");
const chatLog = document.getElementById("chat-log");
const sendButton = document.getElementById("send-button");
const typing = document.getElementById("typing");
const ding = new Audio("/static/ding.mp3");

sendButton.addEventListener("click", sendMessage);
inputField.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    const message = inputField.value.trim();
    if (!message) return;

    addMessage("user", message);
    inputField.value = "";
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
        ding.play();
    } catch (error) {
        typing.classList.add("hidden");
        addMessage("bot", "⚠️ Couldn't reach the server.");
    }
}

function addMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.className = sender;
    messageDiv.innerHTML = sender === "bot" ?
        `<strong>Sky-Sage:</strong> ${text}` :
        text;
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
}
