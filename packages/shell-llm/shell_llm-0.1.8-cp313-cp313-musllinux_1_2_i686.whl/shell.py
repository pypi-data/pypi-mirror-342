#! /usr/bin/env python3
"""
Main shell wrapper module that provides an interactive shell with LLM capabilities.
Uses C core for improved performance.
Natural language queries start with '#'.
"""

import os
import sys
import asyncio
import shlex
import glob
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import HTML
from rich.console import Console
from rich.traceback import install
import json
import subprocess

from core import Shell
from llm import LLMClient
from completions import ShellCompleter
from formatters import ResponseFormatter
from error_handler import ErrorHandler
from models import COMMAND_SCHEMA, CommandResponse
from ui import ShellUI

# Install rich traceback handler
install()

class LLMShell:
    def __init__(self):
        self.console = Console(markup=True, highlight=True)
        self.history_file = os.path.expanduser("~/.llm_shell_history")
        
        # Pre-compute static parts of the prompt
        self.username = os.getenv("USER", "user")
        self.hostname = os.uname().nodename
        
        # Initialize components
        self.core_shell = Shell()
        self._llm_client = None
        self.formatter = ResponseFormatter(self.console)
        self.error_handler = ErrorHandler(self.console, self.llm_client)
        self.ui = ShellUI(self.console)

        self.session = PromptSession(
            history=FileHistory(self.history_file),
            auto_suggest=AutoSuggestFromHistory(),
            completer=ShellCompleter(core_shell=self.core_shell),
            enable_history_search=True,
        )
        
        # Clear the cache on startup
        if self.llm_client:
            self.llm_client.clear_cache()
    
    @property
    def llm_client(self):
        """Lazy initialization of LLM client."""
        if self._llm_client is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set")
            self._llm_client = LLMClient(api_key=api_key)
        return self._llm_client
    
    def get_prompt(self):
        """Generate the shell prompt."""
        cwd = self.core_shell.get_cwd()
        return HTML(f'<ansigreen>{self.username}@{self.hostname}</ansigreen>:<ansiblue>{cwd}</ansiblue>$ ')
    
    async def handle_natural_language_query(self, query: str, verbose: bool, very_verbose: bool):
        """Handle natural language query processing."""
        try:
            response = await self.llm_client.generate_command(query)
            
            # Handle string responses
            if isinstance(response, str):
                response = self._parse_string_response(response, query)
            
            # Ensure response is a dictionary
            if not isinstance(response, dict):
                response = {
                    'command': str(response),
                    'explanation': 'Could not get structured response',
                    'detailed_explanation': 'No detailed explanation available'
                }
            
            # Display command and explanations
            command = str(response.get('command', '')).strip() or f"echo 'Could not generate command for: {query}'"
            self.console.print(f"[bold bright_red]{command}[/bold bright_red]")
            
            if very_verbose and 'detailed_explanation' in response:
                self.formatter.format_detailed_explanation(response.get('detailed_explanation', ''))
            elif verbose and 'explanation' in response:
                self.formatter.format_brief_explanation(response.get('explanation', ''))
            
        except Exception as e:
            await self.error_handler.handle_error(e)
    
    def _parse_string_response(self, response: str, query: str) -> dict:
        """Parse string response into structured format."""
        if response.startswith('{'):
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        return {
            'command': str(response),
            'explanation': 'Could not parse response',
            'detailed_explanation': 'No detailed explanation available'
        }
    
    def _expand_globs(self, args):
        """Helper function to expand glob patterns in arguments."""
        if not args:
            return []

        expanded_args = [args[0]] # Keep the command itself
        for arg in args[1:]:
            # Simple check for glob characters
            if '*' in arg or '?' in arg or ('[' in arg and ']' in arg):
                matches = glob.glob(arg, recursive=False) # Consider recursive=True?
                if matches:
                    expanded_args.extend(matches)
                else:
                    # No match, pass the pattern literally
                    expanded_args.append(arg)
            else:
                # Not a glob pattern, pass as is
                expanded_args.append(arg)
        return expanded_args

    async def handle_command(self, query: str):
        """Process and execute a shell command."""
        if not query.strip():
            return
        
        result = None
        exit_code = 0
        error_msg = None
        command_description = "Command" # For error reporting

        try:
            query = query.strip()
            
            if query.startswith('#'):
                parts = query[1:].split()
                verbose = '-v' in parts
                very_verbose = '-vv' in parts
                clean_query = ' '.join([p for p in parts if p not in ['-v', '-vv']])
                await self.handle_natural_language_query(clean_query, verbose, very_verbose)
                return
            
            # --- Built-in Handling (before core execution) ---
            if query.startswith('cd ') or query == 'cd':
                 try:
                     args = shlex.split(query) # Use shlex even for cd for consistency
                     path = args[1] if len(args) > 1 else os.getenv("HOME", ".")
                     # Use core_shell.cd which updates internal CWD
                     exit_code = self.core_shell.cd(path)
                     if exit_code != 0:
                         # cd itself doesn't return error message, use strerror
                         # (Note: core_shell.cd should ideally set last_error in context)
                         error_msg = os.strerror(abs(exit_code)) # Assuming cd returns -errno
                 except Exception as e:
                     error_msg = f"cd error: {e}"
                     exit_code = 1 # Indicate error
                 # Skip core execution for cd
                 pass # Continue to error handling section

            # --- Alias Simulation (before parsing) ---
            # Add default color flags for common commands
            # NOTE: This is a basic simulation, real alias handling is complex.
            else:
                parts = query.split(None, 1) # Split command from args
                command_word = parts[0] if parts else ''
                original_args_str = parts[1] if len(parts) > 1 else ''
                
                commands_with_color = {'ls', 'grep', 'dir', 'vdir', 'diff'}
                
                if command_word in commands_with_color:
                    # Check if --color is already present
                    if '--color' not in query.split(): # Basic check
                        query = f"{command_word} --color=auto {original_args_str}".strip()
                        # print(f"Alias applied: {query}") # Debug

                # --- Core Execution (Now using potentially modified query) ---
                if '|' in query:
                    command_description = "Pipeline"
                    commands_str = [cmd.strip() for cmd in query.split('|')]
                    
                    # Apply alias simulation to each part of the pipeline
                    processed_cmds_str = []
                    for cmd_str in commands_str:
                        cmd_parts = cmd_str.split(None, 1)
                        cmd_word = cmd_parts[0] if cmd_parts else ''
                        cmd_args_str = cmd_parts[1] if len(cmd_parts) > 1 else ''
                        if cmd_word in commands_with_color and '--color' not in cmd_str.split():
                            processed_cmds_str.append(f"{cmd_word} --color=auto {cmd_args_str}".strip())
                        else:
                            processed_cmds_str.append(cmd_str)

                    # Parse each processed stage using shlex and expand globs
                    pipeline_args_parsed = [shlex.split(cmd) for cmd in processed_cmds_str]
                    # Expand globs for each command in the pipeline
                    pipeline_args_expanded = [self._expand_globs(parsed_cmd) for parsed_cmd in pipeline_args_parsed]

                    valid_pipeline_args = [args for args in pipeline_args_expanded if args]
                    if not valid_pipeline_args:
                         error_msg = "Invalid empty pipeline"
                         exit_code = 1
                    else:
                         result = self.core_shell.execute_pipeline(valid_pipeline_args)
                else:
                    # Handle Single Command
                    command_description = "Command"
                    # Parse the (potentially modified) query
                    args_parsed = shlex.split(query)
                    if not args_parsed:
                         return # Empty command
                    # Expand globs
                    args_expanded = self._expand_globs(args_parsed)

                    result = self.core_shell.execute(args_expanded)
            
            # Process result from core shell execution (if not handled by built-in)
            if result is not None:
                if isinstance(result, tuple):
                    exit_code, core_error_msg = result
                    # Prefer error message from core if available
                    error_msg = core_error_msg if core_error_msg else error_msg
                else:
                    exit_code = result

            # --- Error Handling --- 
            # Handle any error message or non-zero exit code from built-ins or core
            if (error_msg and error_msg.strip()) or exit_code != 0:
                error_text = error_msg.strip() if error_msg else f"{command_description} failed with exit code {exit_code}"
                # Call the async error handler
                await self.error_handler.handle_error(error_text)

        except ValueError as e:
            # Catch shlex parsing errors
            await self.error_handler.handle_error(f"Parsing error: {e}")
        except Exception as e:
            # Catch other unexpected errors during handling/execution
            await self.error_handler.handle_error(f"Execution error: {e}")

    async def run(self):
        """Run the interactive shell."""
        self.ui.show_welcome_banner()
        
        while True:
            try:
                command = await self.session.prompt_async(self.get_prompt)
                if command.strip() == "exit":
                    break
                await self.handle_command(command)
            except EOFError:
                break
            except KeyboardInterrupt:
                continue
            except Exception as e:
                await self.error_handler.handle_error(e)
        
        self.ui.show_goodbye()

def main():
    """Entry point for the shell."""
    shell = LLMShell()
    asyncio.run(shell.run())

if __name__ == "__main__":
    main() 