function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;

    let chatBox = document.getElementById("chatBox");

    // Append User Message
    let userMessage = document.createElement("div");
    userMessage.className = "message user-message";
    userMessage.innerHTML = `<div class="message-content">${userInput}</div>`;
    chatBox.appendChild(userMessage);

    document.getElementById("userInput").value = "";

    // Typing Animation
    let typingDiv = document.createElement("div");
    typingDiv.className = "message bot-message";
    typingDiv.innerHTML = `<div class="message-content typing"><span></span><span></span><span></span></div>`;
    chatBox.appendChild(typingDiv);

    setTimeout(() => {
        chatBox.removeChild(typingDiv);

        // Append Bot Response
        let botMessage = document.createElement("div");
        botMessage.className = "message bot-message";
        botMessage.innerHTML = `<div class="message-content">${getBotResponse(userInput)}</div>`;
        chatBox.appendChild(botMessage);

        chatBox.scrollTop = chatBox.scrollHeight;
    }, 1500);
}

// Sample AI Responses
function getBotResponse(input) {
    let responses = {
        "hi": "Hello! How can I assist you today?",
        "how are you": "I'm just a bot, but I'm doing great! 😊",
        "what is your name": "I am an AI assistant, here to help you!",
        "default": "I’m not sure about that. Could you rephrase?"
    };

    return responses[input.toLowerCase()] || responses["default"];
}
