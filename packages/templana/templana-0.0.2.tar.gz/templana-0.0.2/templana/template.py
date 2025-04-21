# -*- coding: utf-8 -*-
from __future__ import annotations as _annotations
import inspect
import re
import jinja2
from dataclasses import dataclass
from typing import Callable, Generic
from typing_extensions import ParamSpec


TemplateParams = ParamSpec('TemplateParams', default=...)


# TODO This will change once you add filesystem loaders
# instead of global you will have a custom loader and initialize this
# inside appropriate methids.
env = jinja2.Environment(
    loader=None,
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
    undefined=jinja2.StrictUndefined,
)


@dataclass
class Template(Generic[TemplateParams]):
    """
    Represents a prompt template.

    We return a `Template` class instead of a simple function so the
    template can be accessed by callers.
    """
    template: jinja2.Template
    signature: inspect.Signature | None

    def __call__(self, *args: TemplateParams.args, **kwargs: TemplateParams.kwargs) -> str:
        """Render and return the template.

        Returns:
            The rendered template as a Python ``str``.
        """
        if self.signature is not None:
            bound_arguments = self.signature.bind(*args, **kwargs)
            bound_arguments.apply_defaults()
            return self.template.render(**bound_arguments.arguments)
        else:
            return self.template.render(**kwargs)

    @classmethod
    def from_string(cls, content: str):
        """Create a `Template instance from a string containing a Jinja2 template.`

        Args:
            content: The string to construct a template from
        Returns:
            A `Template` instance with the provided content as the template
        """
        return cls(env.from_string(content), None)


def prompt(fn: Callable[TemplateParams, None]) -> Template[TemplateParams]:
    """Decorate a function and turn it's docstring into a template."""
    signature = inspect.signature(fn)

    # The docstring contains the template that will be rendered to be used
    # as a prompt to the language model.
    docstring = fn.__doc__

    if docstring is None:
        raise TypeError("Could not find a template in the function's docstring.")

    # Dedent, and remove extra linebreak
    cleaned_template = inspect.cleandoc(docstring)

    # Add linebreak if there were any extra linebreaks that
    # `cleandoc` would have removed
    ends_with_linebreak = docstring.replace(" ", "").endswith("\n\n")
    if ends_with_linebreak:
        cleaned_template += "\n"

    # Remove extra whitespaces, except those that immediately follow a newline symbol.
    # This is necessary to avoid introducing whitespaces after backslash `\` characters
    # used to continue to the next line without linebreak.
    cleaned_template = re.sub(r"(?![\r\n])(\b\s+)", " ", cleaned_template)
    return Template(env.from_string(cleaned_template), signature)
