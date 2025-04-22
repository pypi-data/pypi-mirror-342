import { DocEvents } from "yjs/dist/src/internals";
import { JupyterFrontEnd } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { SettingsPage } from "./setting_page";

/**
 * Create an icon button with tooltip
 * @param className CSS class for the button
 * @param style CSS style string for the button
 * @param svgContent Inline SVG content
 * @param tooltip Tooltip text for mouseover
 * @returns The created button element
 */
export function createIconButton(className: string, style: string, svgContent: string, tooltip: string): HTMLButtonElement {
  const button = document.createElement('button');
  button.className = `escobar-icon-button ${className}`;
  button.title = tooltip; // This adds the native tooltip on hover
  button.style.cssText = style; // Apply the custom style
  
  // Create a span to hold the SVG content
  const iconSpan = document.createElement('span');
  iconSpan.className = 'escobar-icon-container';
  iconSpan.innerHTML = svgContent;
  
  button.appendChild(iconSpan);
  return button;
}

/**
 * Create the top buttons for the chat interface
 * @param app JupyterFrontEnd instance
 * @param settingsRegistry Settings registry
 * @param getSettings Function to get the current settings
 * @param onNewChat Callback for new chat button
 * @param onReconnect Callback for reconnect button
 * @param onSettingsUpdate Callback for when settings are updated
 * @returns The button container element
 */
export function createTopButtons(
  app: JupyterFrontEnd, 
  settingsRegistry: ISettingRegistry | null,
  getSettings: () => any,
  onNewChat: () => Promise<void>,
  onReconnect: () => Promise<void>,
  onSettingsUpdate: (newSettings: any) => void
): HTMLDivElement {
  // Create button container for top buttons
  const buttonContainer = document.createElement('div');
  buttonContainer.className = 'escobar-button-container';
  
  // Style for all buttons to make them more bold without backgrounds
  const buttonStyle = `
    font-weight: bold;
    margin: 0 5px;
    padding: 5px;
    background: transparent;
    border: none;
  `;
  
  // Create new chat button with inline SVG
  const newChatButton = createIconButton(
    'escobar-new-chat-button',
    buttonStyle,
    `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="escobar-icon-svg">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="12" y1="8" x2="12" y2="16"></line>
      <line x1="8" y1="12" x2="16" y2="12"></line>
    </svg>`,
    'New Chat'
  );
  newChatButton.addEventListener('click', async () => {
    await onNewChat();
    console.log('New chat button clicked');
  });
  buttonContainer.appendChild(newChatButton);

  // Create reconnect button with inline SVG
  const reconnectButton = createIconButton(
    'escobar-reconnect-button',
    buttonStyle,
    `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="escobar-icon-svg">
      <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"></path>
    </svg>`,
    'Reconnect'
  );
  reconnectButton.addEventListener('click', async () => {
    console.log('Reconnect button clicked');
    
    try {
      // Call the reconnect function
      await onReconnect();
      console.log("Reconnected and initialized successfully");
      
      // Blink the reconnect icon 3 times to indicate success
      const iconContainer = reconnectButton.querySelector('.escobar-icon-container') as HTMLElement;
      if (iconContainer) {
        // Store original opacity
        const originalOpacity = iconContainer.style.opacity || '1';
        
        // Blink 3 times (fade out and in)
        for (let i = 0; i < 3; i++) {
          // Fade out
          iconContainer.style.opacity = '0.2';
          await new Promise(resolve => setTimeout(resolve, 150));
          
          // Fade in
          iconContainer.style.opacity = '1';
          await new Promise(resolve => setTimeout(resolve, 150));
        }
      }
    } catch (e) {
      console.error('Error reconnecting to server:', e);
      // Error handling is done in the callback
    }
  });
  buttonContainer.appendChild(reconnectButton);

  // Create stop button with inline SVG
  const stopButton = createIconButton(
    'escobar-stop-button',
    buttonStyle,
    `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="escobar-icon-svg">
      <rect x="6" y="6" width="12" height="12" rx="2" ry="2"></rect>
    </svg>`,
    'Stop'
  );
  stopButton.addEventListener('click', () => {
    console.log('Stop button clicked');
    // The actual stop logic is handled in the chat widget
  });
  buttonContainer.appendChild(stopButton);
  
  // Create settings button with inline SVG
  const settingsButton = createIconButton(
    'escobar-settings-button',
    buttonStyle,
    `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="escobar-icon-svg">
      <circle cx="12" cy="12" r="3"></circle>
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
    </svg>`,
    'Settings'
  );
  settingsButton.addEventListener('click', () => {
    // Create and show settings page
    if (settingsRegistry) {
      // Always use the most up-to-date settings
      const settingsPage = new SettingsPage(
        settingsRegistry, 
        getSettings(), // Get the current settings
        (newSettings) => {
          // Update settings when saved
          onSettingsUpdate(newSettings);
          console.log('Settings updated:', newSettings);
        }
      );
      settingsPage.show();
    } else {
      console.error('Settings registry not available');
    }
  });
  buttonContainer.appendChild(settingsButton);
  
  return buttonContainer;
}

export function createEscobarSplitButton(options: string[] = []): HTMLDivElement {
    //onst container = document.getElementById(containerId);
  
    const splitButton: HTMLDivElement = document.createElement('div');
    splitButton.className = 'escobar-split-button';
  
    const mainButton: HTMLButtonElement = document.createElement('button');
    mainButton.className = 'escobar-main-button';
    mainButton.textContent = options[0] || 'Select';
    //mainButton.onclick = () => alert(`Clicked: ${mainButton.textContent}`);
  
    const toggleButton: HTMLButtonElement = document.createElement('button');
    toggleButton.className = 'escobar-dropdown-toggle';
    
    // Create SVG icon for dropdown toggle
    const svgIcon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svgIcon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svgIcon.setAttribute('width', '16');
    svgIcon.setAttribute('height', '16');
    svgIcon.setAttribute('viewBox', '0 0 24 24');
    svgIcon.setAttribute('fill', 'none');
    svgIcon.setAttribute('stroke', 'currentColor');
    svgIcon.setAttribute('stroke-width', '2');
    svgIcon.setAttribute('stroke-linecap', 'round');
    svgIcon.setAttribute('stroke-linejoin', 'round');
    svgIcon.classList.add('escobar-icon-svg');
    
    // Create path for chevron-down icon
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M6 9l6 6 6-6');
    
    svgIcon.appendChild(path);
    toggleButton.appendChild(svgIcon);
  
    const dropdownMenu: HTMLUListElement = document.createElement('ul');
    dropdownMenu.className = 'escobar-dropdown-menu';
  
    options.forEach((option: string): void => {
      const li: HTMLLIElement = document.createElement('li');
      const btn: HTMLButtonElement = document.createElement('button');
      btn.textContent = option;
      btn.onclick = (e: MouseEvent): void => {
        e.stopPropagation(); // Prevent the document click handler from firing
        mainButton.textContent = option;
        dropdownMenu.style.display = 'none';
      };
      li.appendChild(btn);
      dropdownMenu.appendChild(li);
    });
  
    
    // Add click handler to document to close dropdown when clicking outside
    const closeDropdown = (e: MouseEvent): void => {
      if (dropdownMenu.style.display === 'block' && 
          !dropdownMenu.contains(e.target as Node) && 
          e.target !== toggleButton) {
        dropdownMenu.style.display = 'none';
      }
    };
    
    document.addEventListener('click', closeDropdown);
    
    toggleButton.onclick = (e: MouseEvent): void => {
      e.stopPropagation();
      
      // Simply toggle display
      if (dropdownMenu.style.display === 'block') {
        dropdownMenu.style.display = 'none';
      } else {
        // Remove from current parent if it exists
        if (dropdownMenu.parentNode) {
          dropdownMenu.parentNode.removeChild(dropdownMenu);
        }
        
        // Ensure the dropdown is appended to the body to avoid stacking context issues
        document.body.appendChild(dropdownMenu);
        
        // Get the button's position relative to the viewport
        const buttonRect = toggleButton.getBoundingClientRect();
        
        // Position it above the button
        dropdownMenu.style.position = 'fixed';
        dropdownMenu.style.bottom = `${window.innerHeight - buttonRect.top + 5}px`;
        dropdownMenu.style.right = `${window.innerWidth - buttonRect.right}px`;
        
        dropdownMenu.style.display = 'block';
      }
    };
    
    splitButton.appendChild(mainButton);
    splitButton.appendChild(toggleButton);
    splitButton.appendChild(dropdownMenu);
    
    splitButton["mainButton"] = mainButton;
    return splitButton;
  }
