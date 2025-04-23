document.addEventListener("DOMContentLoaded", function(){
    const chatBox = document.getElementById("chat-box");
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const resetBtn = document.getElementById("reset-btn");
    const plot3dBox = document.getElementById("plot3d-box");
    const plot2dBox = document.getElementById("plot2d-box");
    const thetaInput = document.getElementById("theta-input");
    const thetaBtn = document.getElementById("theta-btn");
    const saveBtn = document.getElementById("save-btn");

    // Function to render messages in the chatbox with animations
    function renderMessage(sender, text, isTyping = false) {
        let messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender); // Adds "user" or "bot" class

        let messageWrapper = document.createElement("div");
        messageWrapper.classList.add("message-wrapper");
        messageWrapper.appendChild(messageDiv);
        
        chatBox.appendChild(messageWrapper);
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll

        if (isTyping) {
            typeText(messageDiv, text);
        } else {
            messageDiv.innerText = text;
        }
    }

    // Typing effect function
    function typeText(element, text, speed = 15) {
        let index = 0;
        function type() {
            if (index < text.length) {
                element.innerHTML += text.charAt(index);
                index++;
                setTimeout(type, speed);
            }
        }
        type();
    }

    // Show a welcome message with typing animation
    function showWelcomeMessage() {
        renderMessage("bot", "👋 Hello! Welcome to MMM-Fair Chat. \n At the moment, I can help you train either\n - 'MMM_Fair' (the AdaBoost style), or\n - 'MMM_Fair_GBT' (the Gradient Boosting style).\n\n Please type 'MMM_Fair' or 'MMM_Fair_GBT' to begin. \n Or type 'default' to run the GBT version on Adult data with default parameters.🙂 ", true);
    }

    function loadSessionOnLoad() {
        fetch("/get_session_state")
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML = "";
            plot3dBox.innerHTML = "";
            plot2dBox.innerHTML = "";

            if (data.chat_history && data.chat_history.length > 0) {
                data.chat_history.forEach(msg => {
                    renderMessage(msg.sender, msg.text, false);
                });
            } else {
                showWelcomeMessage();
            }

            if (data.plot_all_url) {
                plot3dBox.innerHTML = `<iframe src="${data.plot_all_url}" width="100%" height="400px" frameborder="0"></iframe>`;
            }

            if (data.plot_fair_url) {
                lastPlotFairURL = data.plot_fair_url;
                plot2dBox.innerHTML = `<iframe src="${lastPlotFairURL}" width="100%" height="400px" frameborder="0"></iframe>`;
            }
        })
        .catch(error => {
            console.error("Error loading session state:", error);
            showWelcomeMessage();
        });
    }

    // Reset chat history on page load
    function resetChatOnLoad() {
        fetch("/reset_chat")
        .then(() => {
            chatBox.innerHTML = "";
            plot3dBox.innerHTML = "";
            plot2dBox.innerHTML = "";
            showWelcomeMessage();
        })
        .catch(error => console.error("Error resetting chat:", error));
    }

    // Send message function
    function sendMessage(customMessage = null){
        let userMessage = customMessage || chatInput.value.trim();
        if (!userMessage) return;
        chatInput.value = "";

        renderMessage("user", userMessage);

        fetch("/ask_chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: userMessage})
        })
        .then(response => response.json())
        .then(data => {
            if (data.require_api_key) {
               const providerName = data.provider || "the selected LLM";
               const apiKey = prompt(`🔐 To use AI explanation features, please enter your LLM (${providerName}) API key:`);
               if (!apiKey) {
                    alert("No API key entered. LLM features will remain disabled.");
                    return;
                }
               if (apiKey) {
                    fetch("/provide_api_key", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({api_key: apiKey, model:providerName})
                    })
                    .then(response => response.json())
                    .then(res => {
                        if (res.success) {
                            alert(res.message || "API key saved successfully. Now you can ask for explanations!");
                            // Retry previous message after setting API key
                            sendMessage(userMessage);  // re-run the same message
                        } else {
                            alert("Failed to save API key: " + res.error);
                        }
                    })
                    .catch(err => {
                        alert("Error sending API key.");
                        console.error(err);
                    });
                    return;  // Don't render chat until re-tried
                } else {
                    alert("API key was not provided. LLM features remain disabled.");
               }
            }
            data.chat_history.forEach(chat => {
                renderMessage(chat.sender, chat.text, true);
            });

            // **Load Plot HTML Files Dynamically**
            if (data.plot_all_url) {
                console.log("DEBUG: Loading Plot3D from", data.plot_all_url);
                plot3dBox.innerHTML = `<iframe src="${data.plot_all_url}" width="100%" height="400px" frameborder="0"></iframe>`;
            }
            if (data.plot_fair_url) {
                console.log("DEBUG: Loading Plot2D from", data.plot_fair_url);
                plot2dBox.innerHTML = `<iframe src="${data.plot_fair_url}" width="100%" height="400px" frameborder="0"></iframe>`;
            }

            // Auto-scroll to new messages
            chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
        })
       
        .catch(error => console.error("Error:", error));
    }

    // Send message on button click
    sendBtn.addEventListener("click", sendMessage);

    // Send message on Enter key
    chatInput.addEventListener("keydown", function(e){
        if (e.key === "Enter") sendMessage();
    });

    // Reset Chat on button click
    resetBtn.addEventListener("click", function(){
        fetch("/reset_chat")
        .then(() => {
            chatBox.innerHTML = "";
            plot3dBox.innerHTML = "";
            plot2dBox.innerHTML = "";
            showWelcomeMessage();
        })
        .catch(error => console.error("Error resetting chat:", error));
    });

    // Handle Theta Selection and Model Update
    thetaBtn.addEventListener("click", function(){
        let thetaValue = thetaInput.value.trim();
        if (!thetaValue) {
            alert("Please enter a valid Theta index!");
            return;
        }

        fetch("/update_model", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({theta: thetaValue})
        })
        .then(response => response.json())
        .then(data => {
        if (data.success) {
            alert(`Model updated successfully with Theta ${thetaValue}`);

        // ✅ Dynamically update the fairness report (plot2d)
        if (data.plot_fair_url) {
            console.log("DEBUG: Updating plot2dBox with new report");
            plot2dBox.innerHTML = `<iframe src="${data.plot_fair_url}?t=${Date.now()}" width="100%" height="400px" frameborder="0"></iframe>`;
        }
    } else {
        alert(`Error updating model: ${data.error}`);
    }
    })
        .catch(error => console.error("Error updating model:", error));
    });

    // Handle Save Model Button
    saveBtn.addEventListener("click", function(){
        let savePath = document.getElementById("save-path").value.trim();
        
        if (!savePath) {
            alert("Please enter a valid directory path to save the model!");
            return;
        }
    
        fetch("/save_model", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({save_path: savePath})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Model saved successfully in: ${savePath}`);
            } else {
                alert(`Error saving model: ${data.error}`);
            }
        })
        .catch(error => console.error("Error saving model:", error));
    });

    // Reset chat every time the page loads
    //resetChatOnLoad();
    loadSessionOnLoad();
});