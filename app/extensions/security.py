"""Направление 3. Безопасность и мобильное приложение (голубые классы на диаграмме)."""
from __future__ import annotations

from typing import List

from ..views.interfaces import IПредставление

_НЕ_РЕАЛИЗОВАНО = "Направление развития: в базовой версии не реализовано"


class КодПодтверждения:
    def __init__(self, код: str, времяЖизни: int, использован: bool = False) -> None:
        self.код = код
        self.времяЖизни = времяЖизни
        self.использован = использован


class ДвухфакторнаяАутентификация:
    def __init__(self, идМетода: str, типМетода: str, секретныйКлюч: str, активен: bool = False) -> None:
        self.идМетода = идМетода
        self.типМетода = типМетода
        self._секретныйКлюч = секретныйКлюч
        self.активен = активен
        self.коды: List[КодПодтверждения] = []   # «генерирует», 0..*


class СессияПользователя:
    def __init__(self, идСессии: str, токен: str, устройство: str, времяСоздания: int) -> None:
        self.идСессии = идСессии
        self.токен = токен
        self.устройство = устройство
        self.времяСоздания = времяСоздания


class ЛокальныйКэш:
    def __init__(self, идКэша: str, размер: int, датаОбновления: int, зашифрованныеДанные: str) -> None:
        self.идКэша = идКэша
        self.размер = размер
        self.датаОбновления = датаОбновления
        self._зашифрованныеДанные = зашифрованныеДанные


class МобильноеПриложение:
    def __init__(self, идПриложения: str, версия: str, платформа: str, кэш: ЛокальныйКэш,
                 офлайнРежим: bool = False) -> None:
        self.идПриложения = идПриложения
        self.версия = версия
        self.платформа = платформа
        self.офлайнРежим = офлайнРежим
        self.кэш = кэш   # «использует», 1


class КонтроллерБезопасности:
    def включить2FA(self, идПользователя: str) -> None:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def проверитьКод(self, идПользователя: str, код: str) -> bool:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def создатьСессию(self, идПользователя: str) -> СессияПользователя:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def завершитьСессию(self, идСессии: str) -> None:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def _сгенерироватьТокен(self) -> str:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)


class КонтроллерМобильногоПриложения:
    def синхронизироватьДанные(self) -> None:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def загрузитьВКэш(self, данные: object) -> None:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def получитьИзКэша(self, ид: str) -> object:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def работатьОфлайн(self) -> None:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)


class IПредставлениеБезопасности(IПредставление):  # <<interface>>
    def отобразитьНастройки2FA(self, настройки: ДвухфакторнаяАутентификация) -> None:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def запроситьКодПодтверждения(self) -> str:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def показатьАктивныеСессии(self, сессии: List[СессияПользователя]) -> None:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)


class IМобильноеПредставление(IПредставление):  # <<interface>>
    def отобразитьОфлайнРежим(self, доступен: bool) -> None:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def показатьСтатусСинхронизации(self, статус: str) -> None:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)

    def отобразитьКэшированныеДанные(self, данные: object) -> None:
        raise NotImplementedError(_НЕ_РЕАЛИЗОВАНО)
