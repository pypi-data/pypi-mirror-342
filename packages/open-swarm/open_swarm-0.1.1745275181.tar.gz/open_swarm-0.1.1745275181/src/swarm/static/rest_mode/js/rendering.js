/**
 * rendering.js - Contains functions for rendering messages in the chat area,
 * and appending raw messages to the debug panel.
 */
const messageContainerId = "messageHistory";
const rawMessagesContainerId = "rawMessagesContent";

/**
 * Retrieves the current style theme.
 * @returns {string} - The current style theme ('pastel', 'tropical', 'corporate').
 */
function getCurrentStyleTheme() {
    const container = document.querySelector('.container');
    return container?.getAttribute('data-theme-color') || 'pastel';
}

/**
 * Renders a single message in the chat.
 */
export function renderMessage(role, message, sender = "", metadata = {}, isFirstUser = false) {
    const messageHistory = document.getElementById(messageContainerId);
    if (!messageHistory) return;

    const containerDiv = document.createElement("div");
    containerDiv.classList.add("message", role);
    if (isFirstUser) containerDiv.classList.add("first-user");

    // For our special "plus" icon on hover (to persist the message), we wrap the messageContent in a container
    // Then on hover, show a small plus icon in the top-right corner
    let messageContent = `<strong>${sender}:</strong> ${message.content}`;
    
    // If role === "assistant" and layout is "minimalist", remove boxes, etc.
    const containerElement = document.querySelector('.container');
    if (role === "assistant" && containerElement?.getAttribute('data-theme-layout') === 'minimalist-layout') {
        messageContent = message.content;
    }

    // Determine trash can icon based on current style
    const currentStyle = getCurrentStyleTheme();
    let trashCanIcon = '';
    if (currentStyle === 'corporate') {
        trashCanIcon = '✖️'; // X icon
    } else if (currentStyle === 'tropical') {
        trashCanIcon = '🗑️'; // Emoji trashcan
    } else { // pastel
        trashCanIcon = '🗑️'; // Smaller slim trash can could use a different emoji or a custom SVG
    }

    containerDiv.innerHTML = `
      <div class="message-text">
        ${messageContent}
      </div>
      <span class="persist-icon" title="Persist this message to the pinned area">➕</span>
      <span class="trash-can" title="Delete Chat">${trashCanIcon}</span>
    `;

    // Add event listener on the plus icon
    const plusIcon = containerDiv.querySelector('.persist-icon');
    plusIcon?.addEventListener('click', (event) => {
        event.stopPropagation();
        persistMessage(role, message, sender);
    });

    // Add event listener on the trash can
    const trashCan = containerDiv.querySelector('.trash-can');
    trashCan?.addEventListener('click', (event) => {
        event.stopPropagation();
        // Implement deletion logic if necessary
        showToast("��️ Delete feature is under development.", "info");
    });

    messageHistory.appendChild(containerDiv);
    messageHistory.scrollTop = messageHistory.scrollHeight;
}

/**
 * Persists a message in the "first user message" container,
 * along with any other pinned messages.
 */
function persistMessage(role, message, sender = "") {
    const firstUserMessageDiv = document.getElementById("firstUserMessage");
    if (!firstUserMessageDiv) return;

    // We'll allow multiple pinned messages by just appending
    const pinned = document.createElement("div");
    pinned.classList.add("pinned-message");
    pinned.innerHTML = `<small>${sender}:</small> ${message.content}`;

    firstUserMessageDiv.style.display = "block";
    firstUserMessageDiv.appendChild(pinned);
}

/**
 * Appends raw message data to the Raw Messages pane.
 * @param {string} role - The role of the sender.
 * @param {object} content - The message content.
 * @param {string} sender - The display name of the sender.
 * @param {object} metadata - The metadata associated with the message.
 */
export function appendRawMessage(role, content, sender, metadata) {
    const rawMessage = document.createElement("div");
    rawMessage.className = "raw-message";

    const rawData = {
        role: role,
        sender: sender || "Unknown",
        content: content.content || "No content provided.",
        metadata: metadata // Retain full metadata for backend processing
    };

    const pre = document.createElement("pre");
    pre.textContent = JSON.stringify(rawData, null, 2);
    rawMessage.appendChild(pre);

    rawMessagesContent.appendChild(rawMessage);
    rawMessagesContent.scrollTop = rawMessagesContent.scrollHeight;

    console.log("Appended Raw Message:", rawData);
}
