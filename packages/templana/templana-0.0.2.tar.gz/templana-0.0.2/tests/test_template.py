# -*- coding: utf-8 -*-
from templana import prompt


@prompt
def prompt_greeting(name: str, age: int):  # pyright: ignore[reportUnusedParameter]
    """Hello, I am {{ name }} and I am {{ age }} years old."""


def test_prompt_args():
    """Test prompt argument parsing."""
    rp = prompt_greeting('John', 40)
    assert rp == 'Hello, I am John and I am 40 years old.'
