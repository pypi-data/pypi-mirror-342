from collections.abc import Sized

from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
    SpinnerColumn,
    ProgressColumn,
)
from rich.text import Text
from rich.style import Style


def in_notebook() -> bool:
    """
    Detect if we're running inside a Jupyter or IPython (with kernel) environment.
    This is helpful for choosing the correct Console setup.
    """
    try:
        from IPython import get_ipython

        if "IPKernelApp" in get_ipython().config:
            return True
    except:
        pass
    return False


class UnitsColumn(ProgressColumn):
    """A custom column to display progress with units."""

    def __init__(self, unit="it"):
        super().__init__()
        self.unit = unit

    def render(self, task):
        """Show completed/total with units."""
        completed = int(task.completed)
        total = int(task.total) if task.total is not None else "?"
        return Text(
            f"{completed}/{total} {self.unit}", style=Style(color="cyan", bold=True)
        )


class RichTqdm:
    """
    A Rich-based progress bar wrapper that mimics tqdm usage, with extra features:


    Example usage:
    >>> for i in RichTqdm(range(100), desc="Processing", unit="files"):
    ...     # do something
    ...     pass
    """

    def __init__(
        self,
        iterable=None,
        desc="",
        unit="it",
        total=None,
        disable=False,
        console=None,
        transient=False,
    ):
        """
        :param iterable: The iterable to wrap (e.g. range(100)).
        :param desc: Description text to show in the progress bar.
        :param unit: Unit of measurement for items (e.g., "files", "patients").
        :param total: Total number of iterations (if None, tries len(iterable)).
        :param disable: If True, the progress bar is disabled (no display).
        :param console: A Rich Console instance (auto-detected if not provided).
        :param transient: Whether to leave the progress bar on screen after completion.
                          If True, it is removed once done (similar to tqdm's `leave=False`).
        """
        if total is None and isinstance(iterable, Sized):
            total = len(iterable)

        self.iterable = iterable
        self.desc = desc
        self.unit = unit
        self.total = total
        self.disable = disable

        if not self.disable:
            # Auto-detect console if none given
            if console is None:
                console = Console(force_jupyter=in_notebook())

            # Enhanced columns with better styling and unit display
            self.columns = [
                SpinnerColumn(style="green"),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(
                    bar_width=None,
                    complete_style="green",
                    finished_style="bright_green",
                ),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                UnitsColumn(unit=self.unit),
                TextColumn("•", style="bright_black"),
                TimeElapsedColumn(),
                TextColumn("•", style="bright_black"),
                TimeRemainingColumn(),
            ]

            # Create the Rich Progress
            self.progress = Progress(
                *self.columns,
                console=console,
                transient=transient,
                auto_refresh=True,
                refresh_per_second=10,
                expand=True,  # Make the progress bar use the full width
            )
        else:
            self.progress = None

        self.task_id = None

    def __iter__(self):
        if self.disable:
            # If disabled, just yield from the original iterable with no overhead
            yield from self.iterable
        else:
            # Use progress as a context manager
            with self.progress:
                self.task_id = self.progress.add_task(
                    f"[bold]{self.desc}[/bold]", total=self.total
                )

                for item in self.iterable:
                    self.progress.advance(self.task_id)
                    yield item

    def __len__(self):
        if self.total is not None:
            return self.total
        raise TypeError("object of type 'RichTqdm' has no len()")

    def __enter__(self):
        if self.disable:
            return self
        self._progress_context = self.progress.__enter__()
        self.task_id = self.progress.add_task(
            f"[bold]{self.desc}[/bold]", total=self.total
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.disable:
            return
        self.progress.update(self.task_id, completed=self.total)
        if self.task_id is not None:
            self.progress.remove_task(self.task_id)
            self.task_id = None
        self.progress.__exit__(exc_type, exc_val, exc_tb)

    def update(self, advance=1):
        """
        Manually update progress. Useful if you're not iterating directly
        or if the step size is dynamic.
        Example:
            p.update(advance=5)  # jump 5 steps
        """
        if self.disable or self.task_id is None:
            return
        self.progress.advance(self.task_id, advance=advance)

    def set_description(self, desc):
        """
        Set the description of the progress bar.
        Example:
            p.set_description("Processing item...")
        """
        if self.disable or self.task_id is None:
            return
        self.progress.update(self.task_id, description=desc)

    def write(self, *args, **kwargs):
        """
        Write a message to the console.
        Example:
            p.write("Processing item...")
        """
        if self.disable:
            return
        self.progress.console.print(*args, **kwargs)

    def close(self):
        """
        Close the progress bar and clean up.
        """
        if self.disable:
            return
        if self.task_id is not None:
            self.progress.remove_task(self.task_id)
            self.task_id = None
        self.progress.stop()
        self.progress = None
