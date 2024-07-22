import re
from django.core.exceptions import ValidationError


def validate_colors(value):
    # Regex patterns for different color formats
    hex_pattern = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
    rgb_pattern = re.compile(r"^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$")
    color_names = [
        "red",
        "blue",
        "green",
        "yellow",
        "black",
        "white",
        "gray",
        "orange",
        "purple",
        "pink",
    ]  # Add more if needed

    for color in value:
        color = color.strip()
        if not (
            hex_pattern.match(color) or rgb_pattern.match(color) or color in color_names
        ):
            raise ValidationError(f"{color} is not a valid color")
