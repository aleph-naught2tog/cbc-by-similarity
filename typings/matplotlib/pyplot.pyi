from typing import NotRequired, TypedDict, Unpack

from numpy._typing import ArrayLike


class Figure:
    """A pyplot figure"""

def show() -> None:
    """Display all open figures."""

def xlabel(label: str) -> None:
    """Set the label for the y-axis."""

def ylabel(label: str) -> None:
    """Set the label for the y-axis."""

class __DefFigureKwargs(TypedDict):
    figsize: NotRequired[ArrayLike]

def figure(**kwargs: Unpack[__DefFigureKwargs]) -> Figure:
    """Create a new figure, or activate an existing figure.
    """
