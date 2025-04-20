import typing

import tqdm
import tqdm.contrib

from .base import BaseLogger

T = typing.TypeVar("T")

class CLILogger(BaseLogger):
    def __init__(self):
        pass

    def print(self, data: T) -> None:
        print(data)

    def pbar(
        self,
        data: typing.Iterable[T],
        total: int = None,
        desc: typing.Optional[str] = None
    ) -> typing.Iterable[T]:
        return tqdm.tqdm(data, total = total, desc = desc)

    def zip(
        self,
        *iterables, 
        desc: typing.Optional[str] = None
    ):
        return tqdm.contrib.tzip(*iterables, desc = desc)

    def set_pbar_postfix(self, pbar: tqdm.tqdm, data: dict):
        pbar.set_postfix(data)
