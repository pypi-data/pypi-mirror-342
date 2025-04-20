import { callPython, get_ws } from './voitta/pythonBridge_browser';
import { functions, get_opened_tabs } from "./integrations/jupyter_integrations"


/**
 * A class representing a chat message
 */
export class ResponseMessage {
  public readonly id: string;
  public readonly role: 'user' | 'assistant';
  public isNew: boolean;
  private messageElement: HTMLDivElement;
  private contentElement: HTMLDivElement;
  private content: string;

  /**
   * Create a new ResponseMessage
   * @param id Unique identifier for the message
   * @param role The role of the message sender ('user' or 'assistant')
   * @param initialContent Optional initial content for the message
   */
  constructor(id: string, role: 'user' | 'assistant', initialContent: string = '') {
    this.id = id;
    this.role = role;
    this.isNew = true;
    this.content = initialContent;

    // Create message element
    this.messageElement = document.createElement('div');
    this.messageElement.className = `escobar-message escobar-message-${role}`;
    this.messageElement.dataset.messageId = id;

    // Create content element
    this.contentElement = document.createElement('div');
    this.contentElement.className = 'escobar-message-content';
    this.contentElement.textContent = initialContent;

    this.messageElement.appendChild(this.contentElement);
  }

  /**
   * Set the content of the message
   * @param content The new content
   */
  public setContent(content: string): void {
    this.content = content;
    this.contentElement.textContent = content;

    // Get the parent chat container and scroll to bottom
    const chatContainer = this.messageElement.closest('.escobar-chat-container');
    if (chatContainer) {
      setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }, 0);
    }
  }

  /**
   * Get the content of the message
   */
  public getContent(): string {
    return this.content;
  }

  /**
   * Get the DOM element for the message
   */
  public getElement(): HTMLDivElement {
    return this.messageElement;
  }
}

/**
 * Interface for chat settings
 */
export interface IChatSettings {
  defaultGreeting: string;
  maxMessages: number;
  serverUrl: string;
  apiKey: string;
  username: string;
}

/**
 * A class to handle message operations and storage
 */
export class MessageHandler {
  private messages: ResponseMessage[] = [];
  private messageMap: Map<string, ResponseMessage> = new Map();
  private static messageCounter = 0;
  private apiKey: string;
  private username: string;
  private chatContainer: HTMLDivElement;
  private maxMessages: number;

  /**
   * Create a new MessageHandler
   * @param apiKey API key for authentication
   * @param username Username for the current user
   * @param chatContainer DOM element to display messages
   * @param maxMessages Maximum number of messages to keep
   */
  constructor(apiKey: string, username: string, chatContainer: HTMLDivElement, maxMessages: number = 100) {
    this.apiKey = apiKey;
    this.username = username;
    this.chatContainer = chatContainer;
    this.maxMessages = maxMessages;
  }

  /**
   * Update the settings for the message handler
   * @param apiKey New API key
   * @param username New username
   * @param maxMessages New maximum messages
   */
  public updateSettings(apiKey: string, username: string, maxMessages: number): void {
    this.apiKey = apiKey;
    this.username = username;
    this.maxMessages = maxMessages;
  }

  /**
   * Generate a unique message ID
   */
  public generateMessageId(prefix: string = ""): string {
    const timestamp = Date.now();
    const counter = MessageHandler.messageCounter++;
    const messageId = `${prefix}-msg-${timestamp}-${counter}`;
    return messageId;
  }

  /**
   * Find a message by ID
   * @param id The message ID to find
   */
  public findMessageById(id: string): ResponseMessage | undefined {
    return this.messageMap.get(id);
  }

  /**
   * Add a message to the chat
   * @param role The role of the message sender ('user' or 'assistant')
   * @param content The message content
   * @param id Optional message ID (generated if not provided)
   * @returns The created ResponseMessage
   */
  public addMessage(role: 'user' | 'assistant', content: string, id?: string): ResponseMessage {
    // Generate ID if not provided
    const messageId = id || this.generateMessageId();

    // Create a new ResponseMessage
    const message = new ResponseMessage(messageId, role, content);

    // Add to messages array
    this.messages.push(message);

    // Add to message map
    this.messageMap.set(messageId, message);

    // Add to DOM
    this.chatContainer.appendChild(message.getElement());

    // Scroll to bottom
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;

    // Limit the number of messages if needed
    this.limitMessages();

    return message;
  }

  /**
   * Limit the number of messages based on settings
   */
  public limitMessages(): void {
    if (this.messages.length > this.maxMessages) {
      // Remove excess messages
      const excessCount = this.messages.length - this.maxMessages;
      const removedMessages = this.messages.splice(0, excessCount);

      // Remove from DOM and message map
      for (const message of removedMessages) {
        this.chatContainer.removeChild(message.getElement());
        this.messageMap.delete(message.id);
      }
    }
  }

  /**
   * Clear all messages from the chat area
   */
  public async clearMessages(): Promise<void> {
    // Create a copy of the messages array to safely iterate through
    const messagesToRemove = [...this.messages];

    // Clear the original arrays first
    this.messages = [];

    // Now safely remove each message from the DOM and the map
    for (const message of messagesToRemove) {
      try {
        if (this.chatContainer.contains(message.getElement())) {
          this.chatContainer.removeChild(message.getElement());
        }
        this.messageMap.delete(message.id);
      } catch (error) {
        console.error('Error removing message:', error);
      }
    }

    // Clear the message map as a final safety measure
    this.messageMap.clear();
  }

  /**
   * Load messages from the server
   */
  public async loadMessages(): Promise<void> {
    const call_id = this.generateMessageId();
    const payload = JSON.stringify({
      method: "loadMessages",
      message: { machineId: this.username, "sessionId": "jupyter lab" },
      api_key: this.apiKey,
      call_id: call_id
    });

    const response = await callPython(payload);
    console.log("------ loadMessages -----");
    console.log(response.value);

    for (var i = 0; i < response.value.length; i++) {
      const message = response.value[i];
      switch (message.role) {
        case "user":
          this.addMessage('user', message.content);
          break;
        case "assistant":
          if ((message.content != undefined) && (message.content != "")) {
            this.addMessage('assistant', message.content);
          }
          break;
        default:
          console.log(`unknown message type: ${message.role}`);
      }
    }
  }

  /**
   * Create a new chat session
   */
  public async createNewChat(): Promise<void> {
    const call_id = this.generateMessageId();
    const payload = JSON.stringify({
      method: "createNewChat",
      message: { machineId: this.username, "sessionId": "jupyter lab" },
      api_key: this.apiKey,
      call_id: call_id
    });

    await callPython(payload);
  }

  /**
   * Send a message to the server
   * @param content Message content
   * @param mode Message mode (Talk, Plan, Act)
   * @returns The response message
   */
  public async sendMessage(content: string, mode: string): Promise<ResponseMessage> {
    // Generate unique IDs for this message
    const userMessageId = this.generateMessageId();
    const messageId = this.generateMessageId();

    const opened_tabs = await get_opened_tabs();
    const current_notebook = await functions["listCells"].func()

    // Add user message
    this.addMessage('user', content, userMessageId);

    // Create a placeholder response message with the same ID
    const responseMessage = this.addMessage('assistant', 'Waiting for response...', messageId);

    const ws = get_ws();

    // Send message to WebSocket server if connected
    if (ws && ws.readyState === WebSocket.OPEN) {
      try {
        const payload = JSON.stringify({
          method: "userMessage",
          message: content,
          opened_tabs: opened_tabs,
          current_notebook: current_notebook,
          mode: mode,
          api_key: this.apiKey,
          username: this.username,
          call_id: messageId
        });

        const response = await callPython(payload);
        this.handlePythonResponse(response, responseMessage);

      } catch (error) {
        responseMessage.setContent('Error sending message to server');
      }
    } else {
      // Fallback to echo response if not connected
      setTimeout(() => {
        responseMessage.setContent(`Echo: ${content} (WebSocket not connected)`);
      }, 500);
    }

    return responseMessage;
  }

  /**
   * Handle response from Python server
   * @param response Response data
   * @param responseMsg Response message to update
   */
  public handlePythonResponse(response: any, responseMsg?: ResponseMessage): void {
    try {
      let responseText: string;

      console.log("handlePythonResponse:", response);

      var value = response.value;

      if (typeof value === 'string') {
        responseText = value;
      } else if (value && typeof value === 'object') {
        responseText = JSON.stringify(value);
      } else {
        responseText = 'Received empty response from server';
      }

      // Update the response message with the content
      if (responseMsg) {
        responseMsg.setContent(responseText);
      }
    } catch (error) {
      console.error('Error handling Python response:', error);
      if (responseMsg) {
        responseMsg.setContent('Error: Failed to process server response');
      }
    }
  }

  /**
   * Get all messages
   */
  public getMessages(): ResponseMessage[] {
    return [...this.messages];
  }
}
