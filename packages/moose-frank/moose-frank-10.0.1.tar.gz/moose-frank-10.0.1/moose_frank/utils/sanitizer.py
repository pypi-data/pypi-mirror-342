from typing import Iterable


def style_attribute_filter(allowed_styles: Iterable[str]):
    """
    A poor man's CSS filter for the nh3 sanitizing library.

    Example:

        The following example shows a style attribute being filtered. Note how `color` is
        filtered out, while `padding` is kept:

        >>> nh3.clean(
        ...     '<div style="color: red; padding: 10px">Hello</div>',
        ...     tags={"a", "div"},
        ...     attributes={
        ...         "a": {"href"},
        ...         "div": {"style"},
        ...     },
        ...     attribute_filter=style_attribute_filter({"border", "padding"}),
        ... )
        "<div style=\"padding:10px;\">Hello</div>"
    """

    def _filter(element, attribute, value):
        if attribute == "style":
            new_value = ""
            for line in value.split(";"):
                parts = line.split(":")
                if len(parts) != 2:
                    continue
                property, value = [x.strip() for x in parts]
                if property in allowed_styles:
                    new_value += f"{property}:{value};"
            return new_value
        return value

    return _filter
