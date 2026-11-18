"""Файл, которым обменялись участники мероприятия (класс данных)."""
from __future__ import annotations


class Файл:
    def __init__(self, идФайла: str, имяФайла: str, размер: int, тип: str) -> None:
        self.идФайла: str = идФайла
        self.имяФайла: str = имяФайла
        self.размер: int = размер  # Long в диаграмме, в питоне просто int (байты)
        self.тип: str = тип
