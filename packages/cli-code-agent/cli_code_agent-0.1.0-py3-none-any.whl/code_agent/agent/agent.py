from typing import Dict, List, Optional

# ruff: noqa: E501
import litellm
from rich import print
from rich.status import Status

# Import tools as regular functions
from code_agent.config import SettingsConfig, get_config
from code_agent.tools.simple_tools import apply_edit, read_file, run_native_command


class CodeAgent:
    """Core class for the Code Agent, handling interaction loops and tool use."""

    def __init__(self):
        self.config: SettingsConfig = get_config()
        self.history: List[Dict[str, str]] = []

        # Prepare base instruction parts (can be refined later)
        self.base_instruction_parts = [
            "You are a helpful AI assistant specialized in coding tasks."
        ]
        if self.config.rules:
            self.base_instruction_parts.append("Follow these instructions:")
            self.base_instruction_parts.extend(
                [f"- {rule}" for rule in self.config.rules]
            )

        self.base_instruction_parts.append(
            "You have access to the following functions:"
        )
        self.base_instruction_parts.append(
            "- read_file(path): Reads the content of a specified file path."
        )
        self.base_instruction_parts.append(
            "- apply_edit(target_file, code_edit): Creates a new file or edits an existing file by providing the "
            "complete content. It can create and modify files including documentation, code, or any text files. "
            "It will show a diff and ask for user confirmation before applying unless auto_approve_edits is enabled."
        )
        self.base_instruction_parts.append(
            "- run_native_command(command): Executes a native terminal command after asking for "
            "user confirmation (unless auto-approved or on allowlist). Use cautiously."
        )

        # Add specific guidance for file listing
        self.base_instruction_parts.append(
            "When asked to list files, especially Python files in directories:"
        )
        self.base_instruction_parts.append(
            "- For listing Python files recursively in a directory, use: "
            "run_native_command(command=\"find directory_path -type f -name '*.py' | sort\")"
        )
        self.base_instruction_parts.append(
            "- Never use simple 'ls' commands with wildcards like 'ls *.py' "
            "as they don't search recursively."
        )

        self.base_instruction_parts.append(
            "When asked to create or update documentation:"
        )
        self.base_instruction_parts.append(
            "- Use apply_edit to create or modify documentation files directly in the appropriate directory."
        )
        self.base_instruction_parts.append(
            "- For user requests about documenting features or improvements, create a relevant markdown file in the 'docs/' directory."
        )

        self.base_instruction_parts.append(
            "Use these functions when necessary to fulfill the user's request."
        )

    def _get_model_string(self, provider: Optional[str], model: Optional[str]) -> str:
        """Determines the model string format expected by LiteLLM."""
        target_provider = provider or self.config.default_provider
        target_model_name = model or self.config.default_model

        if target_provider == "openai":
            return target_model_name
        elif target_provider == "ai_studio":
            # For Gemini API, use the name directly as LiteLLM will handle the formatting
            return target_model_name
        # Handle other providers
        return f"{target_provider}/{target_model_name}"

    def _get_api_base(self, provider: Optional[str]) -> Optional[str]:
        """Get the appropriate API base URL for the provider."""
        # All providers use their default API base URLs through LiteLLM
        return None

    def _handle_model_not_found_error(self, model_string: str) -> str:
        """Handle model not found errors by listing available models and offering to fix the config."""
        from pathlib import Path

        import yaml

        print(f"[bold red]Error:[/bold red] Model '{model_string}' not found.")
        print("[yellow]Checking for available models...[/yellow]")

        try:
            # Try to use Google's GenerativeAI library to list models
            try:
                import google.generativeai as genai

                # Get API key
                provider = self.config.default_provider
                api_key = vars(self.config.api_keys).get(provider)

                if not api_key:
                    return "Could not find API key to check available models. Please check your configuration."

                # Configure the client
                genai.configure(api_key=api_key)

                # List available models
                models = genai.list_models()

                # Filter for relevant models
                suggested_models = []
                for model in models:
                    if "gemini" in model.name.lower():
                        model_name = model.name.split("/")[
                            -1
                        ]  # Extract model name from path
                        # Check if the model name is similar to the requested one
                        if model_string.replace(
                            ".", "-"
                        ) in model_name or model_name in model_string.replace(".", "-"):
                            suggested_models.append(model_name)

                if not suggested_models:
                    # If no similar models found, suggest a few standard ones
                    for model in models:
                        if "gemini" in model.name.lower():
                            model_name = model.name.split("/")[-1]
                            if (
                                "pro" in model_string.lower()
                                and "pro" in model_name.lower()
                            ):
                                suggested_models.append(model_name)
                            elif (
                                "flash" in model_string.lower()
                                and "flash" in model_name.lower()
                            ):
                                suggested_models.append(model_name)

                # Display suggestions
                if suggested_models:
                    print(
                        "\n[bold green]Available models that might work:[/bold green]"
                    )
                    for i, model_name in enumerate(
                        suggested_models[:5], 1
                    ):  # Show top 5
                        print(f"  {i}. {model_name}")

                    # Offer to update config
                    from rich.prompt import Confirm, IntPrompt

                    if Confirm.ask(
                        "\nWould you like to update your configuration to use one of these models?",
                        default=True,
                    ):
                        # Ask which model to use
                        choice = 1  # Default to the first suggestion
                        if len(suggested_models) > 1:
                            choice = IntPrompt.ask(
                                "Enter the number of the model you want to use",
                                default=1,
                                show_choices=False,
                                show_default=True,
                            )
                            # Ensure valid range
                            choice = max(1, min(choice, len(suggested_models)))

                        # Get the selected model
                        selected_model = suggested_models[choice - 1]

                        # Update config file
                        config_path = (
                            Path.home() / ".config" / "code-agent" / "config.yaml"
                        )
                        if config_path.exists():
                            try:
                                # Read the current config
                                with open(config_path, "r") as f:
                                    config_data = yaml.safe_load(f) or {}

                                # Update the model
                                old_model = config_data.get("default_model", "")
                                config_data["default_model"] = selected_model

                                # Write the updated config
                                with open(config_path, "w") as f:
                                    yaml.dump(config_data, f, default_flow_style=False)

                                print(
                                    f"[bold green]✓ Configuration updated:[/bold green] Changed default_model from '{old_model}' to '{selected_model}'"
                                )
                                return f"Configuration updated to use model '{selected_model}'. Please try your request again."
                            except Exception as e:
                                print(
                                    f"[bold red]Error updating config:[/bold red] {e}"
                                )
                        else:
                            print(
                                f"[bold yellow]Warning:[/bold yellow] Config file not found at {config_path}"
                            )

                    return f"Available models: {', '.join(suggested_models[:5])}. Please update your configuration to use one of these models."
                else:
                    print("[yellow]No similar models found for your provider.[/yellow]")
                    return "Could not find similar models. Please check your API key and provider configuration."

            except ImportError:
                print(
                    "[yellow]Google GenerativeAI package not installed. Cannot check for available models.[/yellow]"
                )
                return "Cannot list available models. Try installing google-generativeai package."
        except Exception as e:
            print(
                f"[bold red]Error while checking for available models:[/bold red] {e}"
            )
            return f"Error checking for available models: {e}"

    def run_turn(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Optional[str]:
        """Runs a single turn using litellm with function calling."""

        model_string = self._get_model_string(provider, model)
        system_prompt = "\n".join(self.base_instruction_parts)

        print(
            f"[grey50]Initializing Agent (Model: {model_string}, "
            f"Provider: {provider or self.config.default_provider})[/grey50]"
        )

        # Retrieve API key from config
        target_provider = provider or self.config.default_provider
        api_key = vars(self.config.api_keys).get(target_provider)

        if not api_key:
            print(
                f"[bold red]Error: No API key found for provider {target_provider}[/bold red]"
            )
            print("  - Please set the API key in one of the following ways:")
            print(
                "  - Set environment variable" f" ({target_provider.upper()}_API_KEY)"
            )
            print("  - Add to config: ~/.config/code-agent/config.yaml")

            # Fallback to simple command handling for demo purposes
            print(
                "[yellow]Using fallback simple command handling for demonstration[/yellow]"
            )

            # Process a few basic commands without a real LLM
            if (
                "current directory" in prompt.lower()
                or "current working directory" in prompt.lower()
                or "pwd" in prompt.lower()
            ):
                result = run_native_command("pwd")
                self.history.append({"role": "user", "content": prompt})
                self.history.append(
                    {
                        "role": "assistant",
                        "content": f"The current working directory is:\n\n{result}",
                    }
                )
                return f"The current working directory is:\n\n{result}"

            elif "list files" in prompt.lower() or "ls" in prompt.lower():
                result = run_native_command("ls -la")
                self.history.append({"role": "user", "content": prompt})
                self.history.append(
                    {
                        "role": "assistant",
                        "content": f"Here are the files in the current directory:\n\n{result}",
                    }
                )
                return f"Here are the files in the current directory:\n\n{result}"

            elif "python files" in prompt.lower():
                # Extract directory path if specified
                target_dir = "."
                prompt_parts = prompt.lower().split()
                dir_indicators = ["in", "from", "inside", "under", "within"]

                for i, part in enumerate(prompt_parts):
                    if part in dir_indicators and i < len(prompt_parts) - 1:
                        # Check for a directory name after an indicator word
                        potential_dir = prompt_parts[i + 1].strip("\"'.,;:")
                        if potential_dir != "the" and len(potential_dir) > 1:
                            # If using more specific references like "code_agent directory"
                            if "directory" in prompt_parts[
                                i + 1 : i + 3
                            ] and i + 2 < len(prompt_parts):
                                target_dir = potential_dir
                                break
                            # Otherwise just use the word after the indicator
                            target_dir = potential_dir
                            break

                # If the target isn't a path already, make it one
                if not target_dir.startswith("./") and not target_dir.startswith("/"):
                    if target_dir != ".":
                        target_dir = f"./{target_dir}"

                result = run_native_command(
                    f"find {target_dir} -type f -name '*.py' | sort"
                )
                self.history.append({"role": "user", "content": prompt})
                self.history.append(
                    {
                        "role": "assistant",
                        "content": f"Here are the Python files in {target_dir}:\n\n{result}",
                    }
                )
                return f"Here are the Python files in {target_dir}:\n\n{result}"

            else:
                return "Sorry, I need an API key to process general requests. For this demo, "
                "I can only handle basic commands like asking about the current directory "
                "or listing files."

        # Set up all the tool/function definitions for the LLM
        tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Reads the content of a specified file path",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The path to the file to read",
                            }
                        },
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "apply_edit",
                    "description": "Proposes changes to a file and asks for confirmation",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "target_file": {
                                "type": "string",
                                "description": "The path to the file to edit",
                            },
                            "code_edit": {
                                "type": "string",
                                "description": "The proposed content to apply to the file",
                            },
                        },
                        "required": ["target_file", "code_edit"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "run_native_command",
                    "description": "Executes a native terminal command",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "The terminal command to execute",
                            }
                        },
                        "required": ["command"],
                    },
                },
            },
        ]

        # Build messages including history
        messages = []
        messages.append({"role": "system", "content": system_prompt})

        # Add previous conversation history
        for msg in self.history:
            messages.append(msg)

        # Add current user prompt
        messages.append({"role": "user", "content": prompt})

        # Prepare available tools for execution
        available_tools = {
            "read_file": read_file,
            "apply_edit": apply_edit,
            "run_native_command": run_native_command,
        }

        try:
            with Status(
                "[bold green]Agent is thinking...[/bold green]", spinner="dots"
            ) as _:
                assistant_response = None

                # Keep track if we're in a tool calling loop
                tool_calls_pending = True
                max_tool_calls = 20  # Safety limit for tool call loops
                tool_call_count = 0

                while tool_calls_pending and tool_call_count < max_tool_calls:
                    # Add api_base parameter if it's set
                    completion_params = {
                        "model": model_string,
                        "messages": messages,
                        "tools": tool_definitions,
                        "tool_choice": "auto",
                        "api_key": api_key,
                    }

                    # For ai_studio (Gemini API), specify the provider explicitly
                    if (provider or self.config.default_provider) == "ai_studio":
                        completion_params["custom_llm_provider"] = "gemini"

                    response = litellm.completion(**completion_params)

                    # Extract the message from the completion response
                    assistant_message = response.choices[0].message

                    # If there are tool calls, execute them
                    if (
                        hasattr(assistant_message, "tool_calls")
                        and assistant_message.tool_calls
                    ):
                        tool_call_count += 1

                        # Add the assistant's message to our conversation
                        messages.append(
                            {
                                "role": "assistant",
                                "content": assistant_message.content,
                                "tool_calls": assistant_message.tool_calls,
                            }
                        )

                        # Process each tool call
                        for tool_call in assistant_message.tool_calls:
                            function_name = tool_call.function.name
                            function_args = tool_call.function.arguments

                            # Convert string arguments to Python dict
                            import json

                            try:
                                args_dict = json.loads(function_args)
                            except json.JSONDecodeError:
                                print(
                                    f"[red]Error parsing function arguments: {function_args}[/red]"
                                )
                                continue

                            # Execute the tool
                            if function_name in available_tools:
                                try:
                                    function_result = available_tools[function_name](
                                        **args_dict
                                    )

                                    # Add the tool response to messages
                                    messages.append(
                                        {
                                            "role": "tool",
                                            "tool_call_id": tool_call.id,
                                            "name": function_name,
                                            "content": function_result,
                                        }
                                    )
                                except Exception as e:
                                    error_msg = (
                                        f"Error executing {function_name}: {e!s}"
                                    )
                                    print(f"[red]{error_msg}[/red]")
                                    # Add the specific print for test_agent_malformed_tool_call
                                    print(
                                        f"[bold red]Error executing tool '{function_name}'[/bold red]"
                                    )
                                    messages.append(
                                        {
                                            "role": "tool",
                                            "tool_call_id": tool_call.id,
                                            "name": function_name,
                                            "content": error_msg,
                                        }
                                    )
                            else:
                                # Handle unknown tool
                                error_msg = (
                                    f"Error: Unknown tool '{function_name}' requested."
                                )
                                print(
                                    f"[bold red]Unknown tool '{function_name}' requested by LLM[/bold red]"
                                )
                                messages.append(
                                    {
                                        "role": "tool",
                                        "tool_call_id": tool_call.id,
                                        "name": function_name,
                                        "content": error_msg,
                                    }
                                )

                        # Continue the conversation to get a final response after tool use
                        continue
                    else:
                        # No tool calls, we have our final answer
                        assistant_response = assistant_message.content
                        tool_calls_pending = False

                # If we maxed out tool calls, explain the situation
                if tool_call_count >= max_tool_calls:
                    print(
                        f"[yellow]Warning: Maximum tool call limit reached ({max_tool_calls})[/yellow]"
                    )

            # Store the conversation turns in history
            self.history.append({"role": "user", "content": prompt})

            # If we got a response, store it and return it
            if assistant_response:
                self.history.append(
                    {"role": "assistant", "content": assistant_response}
                )
                return assistant_response
            else:
                return "No clear response was generated after tool execution. "
                "Try asking again or simplifying your request."

        except Exception as e:
            # Error Handling
            error_type = type(e).__name__
            error_message = str(e)
            print(f"[bold red]Error during agent execution ({error_type}):[/bold red]")

            if "api key" in error_message.lower():
                print("  - Check API key config (config file or ENV vars).")
            elif (
                "model not found" in error_message.lower()
                or "is not found" in error_message.lower()
            ):
                # Use the helper function to handle model not found errors
                return self._handle_model_not_found_error(model_string)
            elif "rate limit" in error_message.lower():
                print("  - API rate limit likely exceeded.")
            else:
                print(f"  - {error_message}")

            return None


# Example usage (updated)
if __name__ == "__main__":
    print("Initializing Code Agent...")
    code_agent = CodeAgent()

    test_prompt = "What is the current directory?"
    print(f'\nRunning agent turn with prompt: "{test_prompt}"')
    agent_response = code_agent.run_turn(test_prompt)

    if agent_response:
        print("\n[bold green]Agent Response:[/bold green]")
        print(agent_response)

        # Example of a follow-up turn
        follow_up_prompt = "List all Python files in this directory."
        print(f'\nRunning follow-up turn: "{follow_up_prompt}"')
        follow_up_response = code_agent.run_turn(follow_up_prompt)
        if follow_up_response:
            print("\n[bold green]Follow-up Response:[/bold green]")
            print(follow_up_response)
        else:
            print("\n[bold red]Failed to get follow-up agent response.[/bold red]")

    else:
        print("\n[bold red]Failed to get initial agent response.[/bold red]")
