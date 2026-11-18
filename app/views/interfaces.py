"""IПредставление — интерфейс из пакета «Представление»."""
from __future__ import annotations

from abc import ABC, abstractmethod


class IПредставление(ABC):  # на диаграмме <<interface>>
    @abstractmethod
    def отобразить(self, данные: object) -> None:
        """Показать на экране переданные данные."""

    @abstractmethod
    def обновить(self, данные: object) -> None:
        """Обновить уже показанный экран."""
