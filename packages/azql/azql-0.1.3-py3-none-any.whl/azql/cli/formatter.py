import textwrap
from argparse import HelpFormatter


class CustomHelpFormatter(HelpFormatter):
    """Custom formatter for argparse help messages."""

    def __init__(
        self,
        prog,
        indent_increment=2,
        max_help_position=30,
        width=None,
    ):
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_action_invocation(self, action):
        """Customize how arguments are displayed in help."""
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            return action.metavar or default

        parts = []
        if action.nargs == 0:
            parts.extend(action.option_strings)
        else:
            # Format as requested: "-i, --input_file input_file"
            if len(action.option_strings) > 1:
                # Use lowercase metavar in the display
                parts.append(f"{', '.join(action.option_strings)}")
            else:
                parts.append(f"{action.option_strings[0]}")

        return ", ".join(parts)

    def _format_usage(self, usage, actions, groups, prefix):
        """Format the usage string differently."""
        return super()._format_usage(
            usage,
            actions,
            groups,
            prefix,
        )

    def _split_lines(self, text, width):
        """Improve text wrapping for help descriptions."""
        return textwrap.wrap(text, width)
