from typing import Dict, Any, Optional
from typing_extensions import override
import re

from notionary.elements.text_inline_formatter import TextInlineFormatter
from notionary.elements.notion_block_element import NotionBlockElement


class CalloutElement(NotionBlockElement):
    """
    Handles conversion between Markdown callouts and Notion callout blocks.

    Markdown callout syntax:
    - !> [emoji] Text - Callout with custom emoji
    - !> {color} [emoji] Text - Callout with custom color and emoji
    - !> Text - Simple callout with default emoji and color

    Where:
    - {color} can be one of Notion's color options (e.g., "blue_background")
    - [emoji] is any emoji character
    - Text is the callout content with optional inline formatting
    """

    COLOR_PATTERN = r"(?:(?:{([a-z_]+)})?\s*)?"
    EMOJI_PATTERN = r"(?:\[([^\]]+)\])?\s*"
    TEXT_PATTERN = r"(.+)"

    # Combine the patterns
    PATTERN = re.compile(
        r"^!>\s+"  # Callout prefix
        + COLOR_PATTERN
        + EMOJI_PATTERN
        + TEXT_PATTERN
        + r"$"  # End of line
    )

    DEFAULT_EMOJI = "💡"
    DEFAULT_COLOR = "gray_background"

    VALID_COLORS = [
        "default",
        "gray",
        "brown",
        "orange",
        "yellow",
        "green",
        "blue",
        "purple",
        "pink",
        "red",
        "gray_background",
        "brown_background",
        "orange_background",
        "yellow_background",
        "green_background",
        "blue_background",
        "purple_background",
        "pink_background",
        "red_background",
    ]

    @override
    @staticmethod
    def match_markdown(text: str) -> bool:
        """Check if text is a markdown callout."""
        return text.strip().startswith("!>") and bool(
            CalloutElement.PATTERN.match(text)
        )

    @override
    @staticmethod
    def match_notion(block: Dict[str, Any]) -> bool:
        """Check if block is a Notion callout."""
        return block.get("type") == "callout"

    @override
    @staticmethod
    def markdown_to_notion(text: str) -> Optional[Dict[str, Any]]:
        """Convert markdown callout to Notion callout block."""
        callout_match = CalloutElement.PATTERN.match(text)
        if not callout_match:
            return None

        color = callout_match.group(1)
        emoji = callout_match.group(2)
        content = callout_match.group(3)

        if not emoji:
            emoji = CalloutElement.DEFAULT_EMOJI

        if not color or color not in CalloutElement.VALID_COLORS:
            color = CalloutElement.DEFAULT_COLOR

        return {
            "type": "callout",
            "callout": {
                "rich_text": TextInlineFormatter.parse_inline_formatting(content),
                "icon": {"type": "emoji", "emoji": emoji},
                "color": color,
            },
        }

    @override
    @staticmethod
    def notion_to_markdown(block: Dict[str, Any]) -> Optional[str]:
        """Convert Notion callout block to markdown callout."""
        if block.get("type") != "callout":
            return None

        callout_data = block.get("callout", {})
        rich_text = callout_data.get("rich_text", [])
        icon = callout_data.get("icon", {})
        color = callout_data.get("color", CalloutElement.DEFAULT_COLOR)

        text = TextInlineFormatter.extract_text_with_formatting(rich_text)
        if not text:
            return None

        emoji = ""
        if icon and icon.get("type") == "emoji":
            emoji = icon.get("emoji", "")

        color_str = ""
        if color and color != CalloutElement.DEFAULT_COLOR:
            color_str = f"{{{color}}} "

        emoji_str = ""
        if emoji:
            emoji_str = f"[{emoji}] "

        return f"!> {color_str}{emoji_str}{text}"

    @override
    @staticmethod
    def is_multiline() -> bool:
        return False

    @classmethod
    def get_llm_prompt_content(cls) -> dict:
        """
        Returns a dictionary with all information needed for LLM prompts about this element.
        Includes description, usage guidance, syntax options, and examples.
        """
        return {
            "description": "Creates a callout block to highlight important information with an icon and background color.",
            "when_to_use": "Use callouts when you want to draw attention to important information, tips, warnings, or notes that stand out from the main content.",
            "syntax": [
                "!> Text - Simple callout with default emoji (💡) and color (gray background)",
                "!> [emoji] Text - Callout with custom emoji",
                "!> {color} [emoji] Text - Callout with custom color and emoji",
            ],
            "color_options": [
                "default",
                "gray",
                "brown",
                "orange",
                "yellow",
                "green",
                "blue",
                "purple",
                "pink",
                "red",
                "gray_background",
                "brown_background",
                "orange_background",
                "yellow_background",
                "green_background",
                "blue_background",
                "purple_background",
                "pink_background",
                "red_background",
            ],
            "examples": [
                "!> This is a default callout with the light bulb emoji",
                "!> [🔔] This is a callout with a bell emoji",
                "!> {blue_background} [💧] This is a blue callout with a water drop emoji",
                "!> {yellow_background} [⚠️] Warning: This is an important note to pay attention to",
            ],
        }
