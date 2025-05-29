from typing import Any, NotRequired, TypedDict, Unpack

from numpy._typing import ArrayLike
from numpy.typing import NDArray


class Figure:
    """A pyplot figure"""
    def suptitle(self, title: str) -> None: ...

class Axes:
    def set_title(self, title: str) -> None:
        """Set the title"""

def show() -> None:
    """Display all open figures."""

def xlabel(label: str) -> None:
    """Set the label for the y-axis."""

def ylabel(label: str) -> None:
    """Set the label for the y-axis."""

class __DefFigureKwargs(TypedDict):
    figsize: NotRequired[ArrayLike]

def figure(**kwargs: Unpack[__DefFigureKwargs]) -> Figure:
    """Create a new figure, or activate an existing figure."""

def plot(xData: ArrayLike, yData: ArrayLike) -> None:
    """ Plot y versus x as lines and/or markers."""

def title(t: str) -> None: ...

def bar(xData: ArrayLike, yData: ArrayLike, width: float | ArrayLike = 0.8) -> None:
    """Make a bar plot."""

def subplots(
    numberOfRows: int = 1,
    numberOfColumns: int =1,
    **fig_kw: Unpack[__DefFigureKwargs]
) -> tuple[Figure, Axes | NDArray[Any]]:
    """Create a figure and a set of subplots.

    Args:
        numberOfRows (int, optional): How many plots down. Defaults to 1.
        numberOfColumns (int, optional): How many plots across. Defaults to 1.

    Returns:
        tuple[Figure, Axes]: _description_
    """
