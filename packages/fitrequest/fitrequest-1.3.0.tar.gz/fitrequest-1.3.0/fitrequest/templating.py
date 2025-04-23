import jinja2


class KeepPlaceholderUndefined(jinja2.Undefined):
    """
    Custom Jinja2 Undefined class that preserves undefined variables
    in the rendered output using placeholder syntax.

    Instead of replacing undefined variables with an empty string or raising
    an error, this class returns the variable name wrapped in delimiters,
    matching the environment's variable start and end strings.

    This is useful for:
      - Debugging template output with missing variables.
      - Partial rendering where some variables are intentionally left unresolved.
      - Avoiding unintended rendering of docstring templates when rehydrating
        configurations (e.g., `fit_config`) into new class instances.

    The most common use case is when the docstring template is something like
    ``"Request endpoint: {endpoint}"`` and ``endpoint="/item/{item}"``.

    The final docstring in the `fit_config` variable will be:
    ``"Request endpoint: /item/{item}"``

    But if rendered with standard Jinja2, ``{item}`` would be treated as an undefined
    variable and replaced with an empty string, resulting in:
    ``"Request endpoint: /item/"``

    This breaks deserialization integrity when calling:
    ``FitConfig.from_dict(**client.fit_config)``

    Using ``KeepPlaceholderUndefined`` preserves ``{item}``, ensuring:
    ``assert FitConfig.from_dict(**client.fit_config).fit_config == client.fit_config``
    """

    def __str__(self) -> str:
        # single-brace style, to match your custom delimiters
        return f'{{{self._undefined_name}}}'


#: Custom Jinja2 environment tailored for safe and partial rendering of docstring templates.
jinja_env: jinja2.Environment = jinja2.Environment(
    variable_start_string='{',
    variable_end_string='}',
    autoescape=True,  # ruff S701
    undefined=KeepPlaceholderUndefined,
)
