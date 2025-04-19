"""
History command for CAI REPL.
This module provides commands for displaying conversation history.
"""
from typing import Dict, List, Optional
from rich.console import Console  # pylint: disable=import-error
from rich.table import Table  # pylint: disable=import-error

from cai.repl.commands.base import Command, register_command

console = Console()


class HistoryCommand(Command):
    """Command for displaying conversation history."""

    def __init__(self):
        """Initialize the history command."""
        super().__init__(
            name="/history",
            description="Display the conversation history",
            aliases=["/h"]
        )

    def handle(self, args: Optional[List[str]] = None, 
               messages: Optional[List[Dict]] = None) -> bool:
        """Handle the history command.
        
        Args:
            args: Optional list of command arguments
            messages: Optional list of conversation messages
            
        Returns:
            True if the command was handled successfully, False otherwise
        """
        # If there are no arguments, show all history
        return self.handle_no_args(messages)

    def handle_no_args(self, messages: Optional[List[Dict]] = None) -> bool:
        """Handle the command when no arguments are provided.

        Args:
            messages: Optional list of conversation messages

        Returns:
            True if the command was handled successfully, False otherwise
        """
        # Access messages directly from repl.py's global scope
        try:
            if messages is None:
                from cai.repl.repl import messages as repl_messages  # pylint: disable=import-outside-toplevel  # noqa: E501
                messages = repl_messages
        except ImportError:
            console.print(
                "[red]Error: Could not access conversation history[/red]")
            return False
        except Exception as e:
            console.print(
                f"[red]Error accessing conversation history: {str(e)}[/red]")
            return False

        if not messages:
            console.print("[yellow]No conversation history available[/yellow]")
            return True

        # Create a table for the history
        table = Table(
            title="Conversation History",
            show_header=True,
            header_style="bold yellow"
        )
        table.add_column("#", style="dim")
        table.add_column("Role", style="cyan")
        table.add_column("Content", style="green")

        # Add messages to the table
        for idx, msg in enumerate(messages, 1):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            # Truncate long content for better display
            if len(content) > 100:
                content = content[:97] + "..."

            # Color the role based on type
            if role == "user":
                role_style = "cyan"
            elif role == "assistant":
                role_style = "yellow"
            else:
                role_style = "red"

            # Add a newline between each role for better readability
            if idx > 1:
                table.add_row("", "", "")

            table.add_row(
                str(idx),
                f"[{role_style}]{role}[/{role_style}]",
                content
            )

        console.print(table)
        return True


# Register the command
register_command(HistoryCommand())
