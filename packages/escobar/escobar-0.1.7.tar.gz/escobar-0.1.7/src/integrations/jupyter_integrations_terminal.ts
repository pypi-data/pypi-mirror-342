import { JupyterFrontEnd } from '@jupyterlab/application';
import { app, functions } from './jupyter_integrations'


function stripAnsi(text: any): string {
    return text.replace(
      // ANSI escape sequence pattern
      /\x1b\[[0-9;?]*[a-zA-Z]/g,
      ''
    );
  }


export async function findTerminalByName (
    app: JupyterFrontEnd,
    name: string
  ): Promise<ReturnType<typeof app.serviceManager.terminals.connectTo> | null> {
    const { terminals } = app.serviceManager;
  
    await terminals.ready; // always wait until ready
  
    const runningIterator = await terminals.running(); // Returns an IterableIterator<IModel>
    // Convert to array for easier manipulation
    const running = Array.from(runningIterator);
    
    // Log all available terminals for debugging
    console.log("All available terminals:", running.map(term => ({
      name: term.name
    })));
    console.log("Looking for terminal with name:", name);
    
    // First try exact match
    for (const term of running) {
      if (term.name === name) {
        console.log("Found exact terminal match:", term.name);
        return terminals.connectTo({ model: term });
      }
    }
    
    // If no exact match, try numeric match (in case name is just a number)
    if (/^\d+$/.test(name)) {
      for (const term of running) {
        // Check if the terminal name contains the number
        if (term.name.includes(name)) {
          console.log("Found numeric terminal match:", term.name, "for input:", name);
          return terminals.connectTo({ model: term });
        }
      }
    }
    
    // If still no match and we only have one terminal, use that one
    if (running.length === 1) {
      console.log("No match found but only one terminal exists, using:", running[0].name);
      return terminals.connectTo({ model: running[0] });
    }
    
    console.log("No terminal found with name:", name);
    return null;
  }



export function init_terminal() {
    functions["startTerminal"] = {
        "def": {
            "name": "startTerminal",
            "description": "Opens a command line terminal",
            "arguments": {}
        },
        "func": async (args: any): Promise<string> => {
            const terminals = app.serviceManager.terminals;
            const name="";

            const session = await terminals.startNew();

            await app.commands.execute('terminal:open', { name: session.name });

            return JSON.stringify({"staus":"ok", "terminal_name": session.name})

        }
    }

    functions["runCommandInTerminal"] = {
        "def": {
            "name": "runCommandInTerminal",
            "description": "Runs a command in a terminal, do not wait for output",
            "arguments": {
                "name": {
                    "type": "string",
                    "name":  "Name for the terminal to run the command in"
                },
                "command": {
                    "type": "string",
                    "name": "Command to run in the terminal"
                },
                "timeout": {
                    "type": "integer",
                    "name": "Timeout in milliseconds, default 10000"
                }
            }
        },
        "func": async (args: any): Promise<string> => {
            let name = args["name"] || "";
            const command = args["command"] || "";
            const timeout = args["timeout"] || 10000;

            console.log(`Attempting to run command in terminal: ${name}`);
            
            // If name is a JSON string (from getActiveTabInfo), parse it
            if (name.startsWith('{') && name.endsWith('}')) {
                try {
                    const parsed = JSON.parse(name);
                    if (parsed.name) {
                        name = parsed.name;
                        console.log(`Parsed terminal name from JSON: ${name}`);
                    }
                } catch (e) {
                    console.log(`Failed to parse terminal name as JSON: ${e.message}`);
                }
            }
            
            const { terminals } = app.serviceManager;
            
            // If no name provided, try to use the first available terminal
            if (!name) {
                const runningIterator = await terminals.running();
                const running = Array.from(runningIterator);
                if (running.length > 0) {
                    name = running[0].name;
                    console.log(`No terminal name provided, using first available: ${name}`);
                } else {
                    // No terminals available, create a new one
                    console.log("No terminals available, creating a new one");
                    const session = await terminals.startNew();
                    name = session.name;
                    await app.commands.execute('terminal:open', { name: name });
                    // Wait a bit for the terminal to initialize
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
            }
            
            const term = await findTerminalByName(app, name);
            if (term === null) {
                return JSON.stringify({
                    "status": "failure",
                    "message": `Terminal with name ${name} not found`
                });
            }
            
            // Make sure the terminal is open and visible
            await app.commands.execute('terminal:open', { name: name });
            
            // Send the command
            term.send({
                type: 'stdin',
                content: [command + ' ; echo __TERMINATOR__\n']
            });

            var stdout = "";
            var isTerminated = false;

            const commandPromise = new Promise<void>((resolve) => {
                const listener = (_, msg: any) => {
                    if (msg.type === 'stdout') {
                        if (Array.isArray(msg.content)) {
                            for (var i = 0; i < msg.content.length; i++) {
                                const content = stripAnsi(msg.content[i]);
                                stdout += content;
                                // Check if __TERMINATOR__ is in the output
                                if (content.includes('__TERMINATOR__')) {
                                    isTerminated = true;
                                    resolve();
                                }
                            }
                        } else {
                            console.log("> >", msg);
                        }
                    } else {
                        console.log("> >", msg);
                    }
                };
                
                // Connect the listener
                term.messageReceived.connect(listener);
            });

            const timeoutPromise = new Promise<void>(resolve => setTimeout(resolve, timeout));
            await Promise.race([commandPromise, timeoutPromise]);

            console.log(`Command completed: ${command}`);
            console.log(`Output: ${stdout}`);

            return JSON.stringify({
                "status": "success",
                "stop": isTerminated ? "natural" : "timeout",
                "result": stdout.replace('__TERMINATOR__', '').trim()
            });
        }
    }
}
