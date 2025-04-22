import WebSocket from 'ws';

// Interface for pending requests
interface PendingRequest {
  resolve: (value: any) => void;
  reject: (reason?: any) => void;
  timeout: any;
}

// Map to store pending requests by call_id
const pendingRequests: Map<string, PendingRequest> = new Map();

// Default timeout for requests in milliseconds
const DEFAULT_TIMEOUT = 1000 * 60; 

// Function registry type definitions
interface FunctionRegistryEntry {
  fn: Function;
  obj: object | null;
  isAsync: boolean;
  returns: boolean;
}

type FunctionRegistry = {
  [key: string]: FunctionRegistryEntry;
};

// Function registry to store registered functions
const registry: FunctionRegistry = {};

let ws: WebSocket | null = null;
let isConnected = false;
let connectionPromise: Promise<void> | null = null;

/**
 * Initializes the WebSocket connection to the Python server.
 * If a connection attempt is already in progress or the connection is active, it returns that promise.
 *
 * @param url - The WebSocket URL (default: "ws://localhost:8000/ws")
 * @returns A Promise that resolves when the connection is successfully established.
 */
export function initPythonBridge(url: string = "ws://127.0.0.1:8777/ws"): Promise<void> {
  // If already connected, return a resolved promise.
  if (ws && isConnected && ws.readyState === WebSocket.OPEN) {
    return Promise.resolve();
  }

  // If a connection attempt is in progress, return that promise.
  if (connectionPromise) {
    return connectionPromise;
  }

  connectionPromise = new Promise<void>((resolve, reject) => {
    ws = new WebSocket(url);

    ws.on('open', () => {
      isConnected = true;
      console.log("Connected to Python server");
      resolve();
      connectionPromise = null;
    });

    ws.on('error', (err: Error) => {
      console.error("Error connecting to Python server:", err);
      reject(err);
      connectionPromise = null;
    });

    ws.on('close', () => {
      isConnected = false;
      console.log("Python server connection closed");
    });

    ws.on('message', async (data: WebSocket.Data) => {
      const messageStr = typeof data === 'string' ? data : data.toString('utf-8');
      try {
        var jsonData:any = messageStr;
        if (typeof messageStr === 'string') {
          console.log("parsing:", typeof messageStr, messageStr);
          jsonData = JSON.parse(messageStr);
        }

        console.log(jsonData);

        let message_type = jsonData.message_type;
        
        if (message_type === "response") {
          // Check if this is a response to a pending request

          const call_id = jsonData.call_id;

          console.log(" ---- response ---- ", call_id);

          if (call_id && pendingRequests.has(call_id)) {
            console.log("-- call_id :: pendingRequests --");
            // Get the pending request
            const pendingRequest = pendingRequests.get(call_id)!;
            
            // Clear the timeout
            clearTimeout(pendingRequest.timeout);
            
            // Remove from pending requests
            pendingRequests.delete(call_id);
            
            // Extract the response data
            const responseData = jsonData.data || jsonData.response || jsonData;
            
            // Resolve the promise with the response data
            pendingRequest.resolve(responseData);
          } 
          // Also call the general response handler if registered
          else if (registry['handleResponse']) {
            console.log("-- handleResponse --");
            // Extract the response data
            const responseData = jsonData.data || jsonData.response || jsonData;
            // Call the registered response handler
            callRegisteredFunction(responseData);
          } else {
            console.warn("Received response with no matching request or handler");
          }
        } else if (message_type === "request") {
          let function_name = jsonData.function;
          let params = jsonData.params;
          
          // Check if the function exists in the registry
          if (!registry[function_name]) {
            console.error(`Function "${function_name}" not found in registry`);
            return;
          }
          
          let is_async = registry[function_name].isAsync;
          if (is_async) {
            let result = await callRegisteredFunctionAsync(jsonData);
          } else {
            let result = callRegisteredFunction(jsonData);
          } 
        }
      } catch (error) {
        console.error("Error parsing JSON message:", error);
      }
    });
  });

  return connectionPromise;
}

/**
 * Sends a message to the Python server and waits for a response.
 * If the connection is not yet established, it attempts to initialize it.
 *
 * @param message - The message to send (should be a JSON string or other string message).
 * @param timeoutMs - Optional timeout in milliseconds (default: 30000)
 * @returns A Promise that resolves with the response data when received.
 */
export async function callPython(message: string, timeoutMs: number = DEFAULT_TIMEOUT): Promise<any> {
  // If not connected, attempt to initialize the bridge.
  if (!ws || !isConnected || ws.readyState !== WebSocket.OPEN) {
    try {
      await initPythonBridge();
    } catch (err) {
      console.error("Failed to connect while calling Python:", err);
      throw new Error(`Failed to connect to Python server: ${err}`);
    }
  }

  
  // Generate a unique call ID
  const call_id = crypto.randomUUID();

  // In Node.js environment, we'll use a different approach
  // For now, we'll just use the default value
  // In the future, we could use environment variables or a configuration file
  let machineId = "jupyter lab";
  
  // We could add a function to set the username externally
  // This would be called from the main application
  
  // Create the payload
  const payload = JSON.stringify({
    "machineId": machineId,
    "sessionId": "jupyter lab",
    "call_id": call_id,
    "message_type": "request",
    "message": message
  });

  // Return a promise that resolves when the response is received
  return new Promise((resolve, reject) => {
    // If the connection is now open, send the message.
    if (ws && isConnected && ws.readyState === WebSocket.OPEN) {
      // Set up a timeout to reject the promise if no response is received
      const timeout = setTimeout(() => {
        // Remove from pending requests
        pendingRequests.delete( call_id );
        reject(new Error(`Request timed out after ${timeoutMs}ms`));
      }, timeoutMs);

      // Store the promise callbacks and timeout in the pending requests map

      console.log("===== setting call_id =====");
      console.log(call_id);

      pendingRequests.set(call_id, {
        resolve,
        reject,
        timeout
      });

      // Send the message
      ws.send(payload);
      console.log(`Sent message with call_id: ${call_id}`);
    } else {
      reject(new Error("Cannot send message. WebSocket is not connected after attempting to reconnect."));
    }
  });
}

/**
 * Registers a function in the registry to be called later.
 * 
 * @param name - The name to register the function under
 * @param isAsync - Whether the function is asynchronous
 * @param fn - The function to register
 */
export function registerFunction(name: string, isAsync: boolean, 
  fn: Function, obj: object | null = null, returns:boolean = false): void {

  if (registry[name]) {
    console.warn(`Function "${name}" already exists in the registry. Overwriting`);
  }
  
  registry[name] = {
    fn,
    obj,
    isAsync,
    returns
  };
}


export function bridgeReturn(call_id:string, value:any) {
  console.log(`bridgeReturn: ${call_id} ${value}`);
  const payload = {
    call_id: call_id,
    value: value,
    message_type: "response"
  }
  if (ws !== null) {
    ws.send(JSON.stringify(payload));
  } else {
    console.error("WebSocket is null. Cannot send message.");
  }
}


/**
 * Calls a registered function by name with the provided arguments.
 * 
 * @param name - The name of the registered function to call
 * @param args - The arguments to pass to the function
 * @returns The result of the function call, or a Promise if the function is async
 * @throws Error if the function is not found in the registry
 */

export async function callRegisteredFunctionAsync(jsonData: any): Promise<any> {
  console.log("callRegisteredFunctionAsync", typeof jsonData);
  console.log(jsonData);

  const call_id = jsonData["call_id"] || "";
  const function_name = jsonData["function"] || "";
  var params = jsonData["params"] || {};
  const partial = params["partial"] || false;

  var param = params["param"] || {};
  if (partial) {
    param = params["text"] || "";
  }

  console.log(function_name);

  const entry = registry[function_name];
  

  console.log("callRegisteredFunctionAsync args parsed");

  if (!entry) {
    throw new Error(`Function "${function_name}" not found in registry`);
  }
  
  try {
    console.log("callRegisteredFunctionAsync calling func");
    const result = await entry.fn.call(entry.obj, params);
    console.log("callRegisteredFunctionAsync returning result");
    if (entry.returns) {
      bridgeReturn (call_id, result);
    }
    //return await entry.fn.call(entry.obj, param);
  } catch (error) {
    console.error(`Error calling function "${function_name}":`, error);
    throw error;
  }
}


export function callRegisteredFunction(jsonData: any): any {
  const call_id = jsonData["call_id"] || "";
  const function_name = jsonData["function"] || "";
  var params = jsonData["params"] || {};
  const partial = params["partial"] || false;

  var param = params["param"] || {};
  if (partial) {
    param = params["text"] || "";
  }


  const entry = registry[function_name];
  
  
  if (!entry) {
    throw new Error(`Function "${function_name}" not found in registry`);
  }
  try {
    let result = entry.fn.call(entry.obj, params);
    if (entry.returns) {
      bridgeReturn (call_id, result);
    }
  } catch (error) {
    console.error(`Error calling function "${function_name}":`, error);
    throw error;
  }
}

/**
 * Gets the registry of functions.
 * 
 * @returns The function registry with an added call method for each function
 */
export function getFunctionRegistry(): FunctionRegistry & { 
  [key: string]: FunctionRegistryEntry & { 
    call: (name: string, args: any) => any 
  } 
} {
  // Create a proxy to add a 'call' method to each registry entry
  return new Proxy(registry, {
    get(target, prop) {
      if (typeof prop === 'string' && prop in target) {
        // Add a call method to the registry entry
        const entry = target[prop];
        return {
          ...entry,
          call: (name: string, args: any) => {
            try {
              return entry.fn.call(null, args);
            } catch (error) {
              console.error(`Error calling function "${name}":`, error);
              throw error;
            }
          }
        };
      }
      return Reflect.get(target, prop);
    }
  }) as any;
}
