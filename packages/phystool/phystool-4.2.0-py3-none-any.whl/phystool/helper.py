import subprocess
import datetime

from collections import deque
from logging import getLogger
from pathlib import Path
from typing import Iterable, Self
from unidecode import unidecode

logger = getLogger(__name__)


def terminal_yes_no(prompt: str) -> bool:
    """
    Ask for a confirmation in the terminal.

    :param prompt: text displayed before the '[y/n]:' question
    """
    while True:
        answer = input(prompt + " [y/n]: ").lower()
        if answer in ["yes", 'y']:
            return True
        elif answer in ['no', 'n']:
            return False


def silent_keyboard_interrupt(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print()  # to force a new line
            pass
    return inner


def greptex(query: str, path: Path, silent: bool) -> set[str]:
    """Find query in tex files stored in the single directory `path`.

    Format query to match a newline followed by spaces and returns a set of
    uuids of tex files containing query.

    :param query: string that should be matched
    :param path: directory where the search occurs
    :param silent: if True, logs a warning when no match was found
    :returns: a set of uuids corresponding to tex files that contains the query
    """
    if query:
        query = (
            query
            .replace('\\', '\\\\')
            .replace('$', '\\$')
            .replace('{', '\\{')
            .replace('}', '\\}')
        )
        command = [
            'rg',
            '--type', 'tex',
            '--color', 'never',
            '--multiline',
            '--smart-case',
            '--files-with-matches',
            '--max-depth', '1',
            r"\s+".join([tmp.strip() for tmp in query.split()]),
            str(path)
        ]

        try:
            match = subprocess.run(
                command,
                capture_output=True,
                text=True
            )
            return set(
                Path(m).stem
                for m in match.stdout.split('\n')
                if m
            )
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                if not silent:
                    logger.warning(
                        f"'{query}' not found in any texfile in {path}"
                    )
            else:
                logger.error(e)

    return set()


def lower_ascii(txt: str) -> str:
    return unidecode(txt).lower()


def bat(path: Path, title: str) -> None:
    """Display file in terminal with bat.

    The extension is detected from the filename extension

    :param path: file to display
    :param title: title displayed in the bat header
    """
    subprocess.run(
        [
            "bat",
            "--language", path.suffix[1:],
            "--file-name", title,
            path
        ]
    )


def as_valid_filename(txt: str) -> str:
    return "".join(
        [
            "-" if c in [" ", "'", "&", "/", "\\", ",", "[", "]"] else c
            for c in lower_ascii(txt)
        ]
    )


class ContextIterator[T]:
    """
    Wrapper around an iterable that allows peeking ahead to get next elements
    without consuming the iterator.
    """

    def __init__(self, iterable: Iterable[T], before: int, after: int):
        self._iterable = iter(iterable)
        self._cache_next: deque[T] = deque()
        self._cache_prev: deque[T] = deque()
        self._before = abs(before)
        self._after = abs(after)
        self._first_call = True
        self._current: T

    def __next__(self) -> T:
        if self._first_call:
            self._first_call = False
        else:
            self._cache_prev.append(self._current)
            if len(self._cache_prev) > self._before:
                self._cache_prev.popleft()

        if self._cache_next:
            self._current = self._cache_next.popleft()
        else:
            self._current = next(self._iterable)

        return self._current

    def __iter__(self) -> Self:
        return self

    def get(self) -> list[T]:
        try:
            while len(self._cache_next) < self._after:
                self._cache_next.append(next(self._iterable))
        except StopIteration:
            pass

        return (
            list(self._cache_prev)
            + [self._current]
            + list(self._cache_next)
        )


class Klass:
    def __init__(
        self,
        uuid: str,
        name: str,
        year: int,
        extra: str,
        evaluations: list[str]
    ):
        self.uuid = uuid
        self.name = name
        self.year = year
        self.extra = extra
        self.evaluations: list[str] = evaluations

    def __repr__(self) -> str:
        return f"Klass({self.name} [{self.year}/{self.extra}])"

    def __str__(self) -> str:
        return f"{self.name} [{self.year}/{self.extra}]"

    def is_current(self) -> bool:
        return self.year == 2024

    def to_dict(self) -> dict[str, str | list[str] | int]:
        return {
            'name': self.name,
            'year': self.year,
            'extra': self.extra,
            'evaluations': list(self.evaluations)
        }


class Evaluation:
    def __init__(
        self,
        uuid: str,
        klass_uuid: str,
        title: str = "",
        date: str = "2024-08-31",  # FIXME
        number: str = "",
        extra: list[str] = [],
        exercises: list[str] = []
    ):
        self.uuid: str = uuid
        self.klass_uuid: str = klass_uuid
        self.title: str = title
        self.date: datetime.date = datetime.datetime.fromisoformat(date).date()
        self.number: str = number
        self.extra: list[str] = extra
        self.exercises: list[str] = exercises

    def __lt__(self, other) -> bool:
        return self.date < other.date

    def __repr__(self) -> str:
        out = f"{self.date:%d %b %Y} [{self.number}] {self.title:<30} "
        if self.extra:
            out += ",".join(self.extra)
        return out

    def update(self, data: dict) -> tuple[set[str], set[str]]:
        self.title = data['title']
        self.date = datetime.datetime.fromisoformat(data['date']).date()
        self.number = data['number']
        self.extra = data['extra']
        old = set(self.exercises)
        new = set(data['exercises'])
        self.exercises = data['exercises']
        return (old - new), (new - old)

    def to_dict(self) -> dict[str, str | list[str]]:
        return {
            'klass_uuid': self.klass_uuid,
            'title': self.title,
            'date': self.date.isoformat(),
            'number': self.number,
            'extra': self.extra,
            'exercises': self.exercises
        }


def progress_bar(max_step: int, step: int, length: int, msg: str) -> None:
    """Display a progress bar in the terminal

    :param max_step: process' maximum number of steps
    :param step: current process' step
    :param length: number of characters of the progress bar
    :param msg: message displayed after the progress bar
    """
    if max_step:
        m = int(step*length/max_step)
        print(
            f"\r[{'='*m}{' '*(length-m)}]{100*step/max_step:7.2f}% {msg}",
            flush=True,
            end=""
        )
    else:
        print(f"\r[{'?'*length}]{' '*8} {msg}", flush=True, end="")
