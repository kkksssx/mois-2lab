"""Экраны приложения — по одному классу на каждый макет окна из лабораторной №1.

[отклонение Д3] В базовой диаграмме классов есть только два класса интерфейса
(ИнтерфейсОрганизатора и ИнтерфейсУчастника), а макетов окон шесть. Сами окна здесь —
это «глупые» рамки tkinter: они рисуют поля и кнопки и вызывают переданные функции.
Решения принимают классы ИнтерфейсОрганизатора / ИнтерфейсУчастника.
"""
from __future__ import annotations

import datetime
import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List, Optional

from .widgets import ПрокручиваемаяОбласть

ШРИФТ_ЗАГОЛОВКА = ("Arial", 16, "bold")
ШРИФТ_ЖИРНЫЙ = ("Arial", 11, "bold")
ШРИФТ_ОБЫЧНЫЙ = ("Arial", 10)


def форматДаты(секунды: int) -> str:
    return datetime.datetime.fromtimestamp(секунды).strftime("%d.%m.%Y %H:%M")


# ======================================================================
class ЭкранВхода(ttk.Frame):
    """Макет «Экран входа»."""

    def __init__(self, master, при_входе: Callable[[str, str], None],
                 при_регистрации: Callable[[], None]) -> None:
        super().__init__(master, padding=20)
        self._при_входе = при_входе
        ttk.Label(self, text="Экран входа", font=ШРИФТ_ЗАГОЛОВКА).pack(pady=(60, 20))
        форма = ttk.Frame(self)
        форма.pack()
        ttk.Label(форма, text="Логин:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self._логин = ttk.Entry(форма, width=32)
        self._логин.grid(row=0, column=1, pady=5)
        ttk.Label(форма, text="Пароль:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self._пароль = ttk.Entry(форма, width=32, show="*")
        self._пароль.grid(row=1, column=1, pady=5)
        ttk.Button(self, text="Войти", command=self._нажатьВойти).pack(pady=12)
        ссылка = tk.Label(self, text="Зарегистрироваться", fg="blue", cursor="hand2",
                          font=("Arial", 10, "underline"))
        ссылка.pack()
        ссылка.bind("<Button-1>", lambda событие: при_регистрации())
        self._пароль.bind("<Return>", lambda событие: self._нажатьВойти())
        self._логин.focus_set()

    def _нажатьВойти(self) -> None:
        self._при_входе(self._логин.get(), self._пароль.get())


# ======================================================================
class ЭкранРегистрации(ttk.Frame):
    """Макет «Экран регистрации»."""

    def __init__(self, master, при_регистрации: Callable[[str, str, str, str], None],
                 при_возврате: Callable[[], None]) -> None:
        super().__init__(master, padding=20)
        self._при_регистрации = при_регистрации
        ttk.Label(self, text="Экран регистрации", font=ШРИФТ_ЗАГОЛОВКА).pack(pady=(40, 20))
        форма = ttk.Frame(self)
        форма.pack()
        self._поля: Dict[str, ttk.Entry] = {}
        for номер, (подпись, ключ, скрыть) in enumerate([
                ("Имя:", "имя", False), ("Email:", "email", False),
                ("Пароль:", "пароль", True), ("Повтор:", "повтор", True)]):
            ttk.Label(форма, text=подпись).grid(row=номер, column=0, sticky="e", padx=5, pady=5)
            поле = ttk.Entry(форма, width=32, show="*" if скрыть else "")
            поле.grid(row=номер, column=1, pady=5)
            self._поля[ключ] = поле
        ttk.Button(self, text="Зарегистрироваться", command=self._нажать).pack(pady=12)
        # переход «Уже есть аккаунт» из диаграммы состояний интерфейса
        ссылка = tk.Label(self, text="Уже есть аккаунт", fg="blue", cursor="hand2",
                          font=("Arial", 10, "underline"))
        ссылка.pack()
        ссылка.bind("<Button-1>", lambda событие: при_возврате())

    def _нажать(self) -> None:
        п = self._поля
        self._при_регистрации(п["имя"].get(), п["email"].get(), п["пароль"].get(), п["повтор"].get())


# ======================================================================
class ГлавнаяСтраница(ttk.Frame):
    """Макет «Главная страница (Мои мероприятия)».

    карточки — список словарей: ид, тема, датаВремя, роль, статус, естьЗапись.
    Если колбэк создания/статистики равен None, соответствующая кнопка не показывается.
    """

    ФИЛЬТРЫ = ["Все", "Я организатор", "Я участник", "Идут сейчас", "Завершённые"]

    def __init__(self, master, карточки: List[dict],
                 при_создании: Optional[Callable[[], None]],
                 при_подключении: Callable[[str], None],
                 при_статистике: Optional[Callable[[str], None]],
                 при_записи: Callable[[str], None],
                 при_выходе: Callable[[], None]) -> None:
        super().__init__(master, padding=10)
        self._карточки = карточки
        self._при_подключении = при_подключении
        self._при_статистике = при_статистике
        self._при_записи = при_записи

        верх = ttk.Frame(self)
        верх.pack(fill="x")
        ttk.Label(верх, text="Главная страница (Мои мероприятия)",
                  font=ШРИФТ_ЗАГОЛОВКА).pack(side="left")
        ttk.Button(верх, text="Выйти из системы", command=при_выходе).pack(side="right")

        панель = ttk.Frame(self)
        панель.pack(fill="x", pady=8)
        if при_создании is not None:
            ttk.Button(панель, text="+ Создать мероприятие", command=при_создании).pack(side="left", padx=(0, 12))
        ttk.Label(панель, text="Поиск:").pack(side="left")
        self._поиск = tk.StringVar()
        self._поиск.trace_add("write", lambda *args: self._перерисовать())
        ttk.Entry(панель, textvariable=self._поиск, width=24).pack(side="left", padx=(4, 12))
        ttk.Label(панель, text="Фильтр:").pack(side="left")
        self._фильтр = ttk.Combobox(панель, values=self.ФИЛЬТРЫ, state="readonly", width=16)
        self._фильтр.set("Все")
        self._фильтр.pack(side="left", padx=4)
        self._фильтр.bind("<<ComboboxSelected>>", lambda событие: self._перерисовать())

        self._область = ПрокручиваемаяОбласть(self)
        self._область.pack(fill="both", expand=True)
        self._перерисовать()

    def _подходит(self, к: dict) -> bool:
        текст = self._поиск.get().strip().lower()
        if текст and текст not in к["тема"].lower():
            return False
        фильтр = self._фильтр.get()
        if фильтр == "Я организатор":
            return к["роль"] == "Организатор"
        if фильтр == "Я участник":
            return к["роль"] == "Участник"
        if фильтр == "Идут сейчас":
            return к["статус"] == "Идёт"
        if фильтр == "Завершённые":
            return к["статус"] == "Завершено"
        return True

    def _перерисовать(self) -> None:
        for виджет in self._область.внутри.winfo_children():
            виджет.destroy()
        показано = [к for к in self._карточки if self._подходит(к)]
        if not показано:
            ttk.Label(self._область.внутри, text="Мероприятий не найдено",
                      font=ШРИФТ_ОБЫЧНЫЙ).pack(pady=30)
        for к in показано:
            self._нарисоватьКарточку(к)

    def _нарисоватьКарточку(self, к: dict) -> None:
        рамка = tk.Frame(self._область.внутри, bd=1, relief="solid", padx=10, pady=8)
        рамка.pack(fill="x", padx=4, pady=5)
        ttk.Label(рамка, text="Карточка: " + к["тема"], font=ШРИФТ_ЖИРНЫЙ).pack(anchor="w")
        ttk.Label(рамка, text="Дата: %s | Роль: %s | Статус: %s" %
                  (форматДаты(к["датаВремя"]), к["роль"], к["статус"])).pack(anchor="w")
        кнопки = ttk.Frame(рамка)
        кнопки.pack(anchor="w", pady=(6, 0))
        if к["статус"] != "Завершено":
            подпись = "Открыть конференцию" if (к["роль"] == "Организатор" and к["статус"] == "Создано") \
                else "Подключиться"
            ttk.Button(кнопки, text=подпись,
                       command=lambda ид=к["ид"]: self._при_подключении(ид)).pack(side="left", padx=(0, 6))
        if к["роль"] == "Организатор" and self._при_статистике is not None:
            ttk.Button(кнопки, text="Статистика",
                       command=lambda ид=к["ид"]: self._при_статистике(ид)).pack(side="left", padx=(0, 6))
        if к["естьЗапись"]:
            ttk.Button(кнопки, text="Запись",
                       command=lambda ид=к["ид"]: self._при_записи(ид)).pack(side="left")


# ======================================================================
class ЭкранСозданияМероприятия(ttk.Frame):
    """Макет «Создание мероприятия»."""

    def __init__(self, master, при_сохранении: Callable[[], None],
                 при_копировании: Callable[[], None], при_отмене: Callable[[], None]) -> None:
        super().__init__(master, padding=20)
        ttk.Label(self, text="Создание мероприятия", font=ШРИФТ_ЗАГОЛОВКА).pack(pady=(20, 15))
        форма = ttk.Frame(self)
        форма.pack()
        ttk.Label(форма, text="Тема:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self._тема = ttk.Entry(форма, width=40)
        self._тема.grid(row=0, column=1, columnspan=3, sticky="w", pady=5)

        завтра = datetime.datetime.now() + datetime.timedelta(days=1)
        ttk.Label(форма, text="Дата:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self._дата = ttk.Entry(форма, width=14)
        self._дата.insert(0, завтра.strftime("%d.%m.%Y"))
        self._дата.grid(row=1, column=1, sticky="w", pady=5)
        ttk.Label(форма, text="Время:").grid(row=1, column=2, sticky="e", padx=5)
        self._время = ttk.Entry(форма, width=8)
        self._время.insert(0, "10:00")
        self._время.grid(row=1, column=3, sticky="w")
        ttk.Label(форма, text="(дд.мм.гггг)").grid(row=2, column=1, sticky="w")

        ttk.Label(форма, text="Доступ:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        ttk.Button(форма, text="Копировать ссылку", command=при_копировании).grid(
            row=3, column=1, columnspan=2, sticky="w", pady=5)

        self._запись = tk.BooleanVar(value=True)
        self._зал = tk.BooleanVar(value=True)
        ttk.Checkbutton(форма, text="Включить запись", variable=self._запись).grid(
            row=4, column=1, columnspan=3, sticky="w", pady=2)
        ttk.Checkbutton(форма, text="Зал ожидания", variable=self._зал).grid(
            row=5, column=1, columnspan=3, sticky="w", pady=2)

        кнопки = ttk.Frame(self)
        кнопки.pack(pady=18)
        ttk.Button(кнопки, text="Сохранить и пригласить", command=при_сохранении).pack(side="left", padx=6)
        ttk.Button(кнопки, text="Отмена", command=при_отмене).pack(side="left", padx=6)

    def получитьДанные(self) -> dict:
        return {"тема": self._тема.get(), "дата": self._дата.get().strip(),
                "время": self._время.get().strip(), "запись": bool(self._запись.get()),
                "залОжидания": bool(self._зал.get())}


# ======================================================================
class ЭкранКонференции(ttk.Frame):
    """Макет «Экран конференции (Комната)»: видеосетка, чат, нижняя панель."""

    ПЕРИОД_ОПРОСА_МС = 2000  # раз в 2 секунды обновляем участников и чат

    def __init__(self, master, тема: str, этоОрганизатор: bool, колбэки: Dict[str, Optional[Callable]]) -> None:
        super().__init__(master, padding=10)
        self._к = колбэки
        self._микрофонВкл = False
        self._экранВкл = False
        self._подписьСетки = None   # чтобы не перерисовывать сетку без изменений
        self._подписьЧата = None

        ttk.Label(self, text="Экран конференции (Комната)", font=ШРИФТ_ЗАГОЛОВКА).pack(anchor="w")
        self._заголовок = ttk.Label(self, text=тема, font=ШРИФТ_ЖИРНЫЙ)
        self._заголовок.pack(anchor="w", pady=(0, 6))

        # --- видеосетка участников ---
        self._сетка = tk.Frame(self, bg="#e6e6e6", height=230)
        self._сетка.pack(fill="x")
        self._сетка.pack_propagate(False)

        # --- чат ---
        ttk.Label(self, text="Чат:").pack(anchor="w", pady=(8, 0))
        чат = ttk.Frame(self)
        чат.pack(fill="both", expand=True)
        self._чат = tk.Text(чат, height=7, state="disabled", wrap="word")
        прокрутка = ttk.Scrollbar(чат, command=self._чат.yview)
        self._чат.configure(yscrollcommand=прокрутка.set)
        self._чат.pack(side="left", fill="both", expand=True)
        прокрутка.pack(side="right", fill="y")
        ввод = ttk.Frame(self)
        ввод.pack(fill="x", pady=4)
        self._сообщение = ttk.Entry(ввод)
        self._сообщение.pack(side="left", fill="x", expand=True)
        self._сообщение.bind("<Return>", lambda событие: self._отправить())
        self._кнопкаОтправить = ttk.Button(ввод, text="Отправить", command=self._отправить)
        self._кнопкаОтправить.pack(side="left", padx=(6, 0))

        # --- нижняя панель: [Микрофон] [Экран] [Участники] [Завершить] ---
        панель = ttk.Frame(self)
        панель.pack(fill="x", pady=(6, 0))
        self._кнопкаМикрофон = ttk.Button(панель, text="Микрофон: выкл", command=self._микрофон)
        self._кнопкаМикрофон.pack(side="left", padx=3)
        self._кнопкаЭкран = ttk.Button(панель, text="Экран: выкл", command=self._экран)
        self._кнопкаЭкран.pack(side="left", padx=3)
        if этоОрганизатор and колбэки.get("участники"):
            ttk.Button(панель, text="Участники", command=колбэки["участники"]).pack(side="left", padx=3)
        if этоОрганизатор and колбэки.get("завершить"):
            tk.Button(панель, text="Завершить", fg="red", font=ШРИФТ_ЖИРНЫЙ,
                      command=колбэки["завершить"]).pack(side="left", padx=3)
        ttk.Button(панель, text="Выйти из системы", command=колбэки["выйти"]).pack(side="right", padx=3)
        ttk.Button(панель, text="Покинуть встречу", command=колбэки["покинуть"]).pack(side="right", padx=3)
        if not этоОрганизатор:
            self._кнопкаЭкран.state(["disabled"])  # демонстрацию экрана включает организатор

        self._идОпроса = self.after(self.ПЕРИОД_ОПРОСА_МС, self._опрос)
        self.bind("<Destroy>", self._приУничтожении)

    # ---------- обновление данных ----------
    def показатьСостояние(self, участники: List[dict], сообщения: List[dict],
                          я: Optional[dict], демонстрация: bool) -> None:
        """участники: имя, статус, микрофон, организатор. сообщения: ид, время, автор, текст."""
        ожидание = я is not None and я["статус"] == "Зал ожидания"
        подписьСетки = (tuple((у["имя"], у["статус"], у["микрофон"]) for у in участники),
                        ожидание, демонстрация)
        if подписьСетки != self._подписьСетки:
            self._подписьСетки = подписьСетки
            self._нарисоватьСетку(участники, ожидание, демонстрация)
        подписьЧата = tuple(с["ид"] for с in сообщения)
        if подписьЧата != self._подписьЧата:
            self._подписьЧата = подписьЧата
            self._чат.configure(state="normal")
            self._чат.delete("1.0", "end")
            for с in сообщения:
                время = datetime.datetime.fromtimestamp(с["время"]).strftime("%H:%M")
                self._чат.insert("end", "[%s] %s: %s\n" % (время, с["автор"], с["текст"]))
            self._чат.configure(state="disabled")
            self._чат.see("end")
        # кнопки зависят от состояния текущего пользователя
        self._микрофонВкл = bool(я and я["микрофон"])
        self._кнопкаМикрофон.configure(text="Микрофон: вкл" if self._микрофонВкл else "Микрофон: выкл")
        self._экранВкл = демонстрация
        self._кнопкаЭкран.configure(text="Экран: вкл" if демонстрация else "Экран: выкл")
        состояние = ["disabled"] if ожидание else ["!disabled"]
        self._кнопкаМикрофон.state(состояние)
        self._кнопкаОтправить.state(состояние)

    def _нарисоватьСетку(self, участники: List[dict], ожидание: bool, демонстрация: bool) -> None:
        for виджет in self._сетка.winfo_children():
            виджет.destroy()
        if ожидание:
            tk.Label(self._сетка, bg="#e6e6e6", font=ШРИФТ_ЖИРНЫЙ,
                     text="Вы в зале ожидания.\nДождитесь, пока организатор вас впустит.").pack(expand=True)
            return
        if демонстрация:
            tk.Label(self._сетка, bg="#bfd9ff", text="[ Идёт демонстрация экрана организатора ]",
                     font=ШРИФТ_ЖИРНЫЙ).pack(fill="x", padx=6, pady=(6, 2))
        в_комнате = [у for у in участники if у["статус"] == "Подключён"]
        плитки = tk.Frame(self._сетка, bg="#e6e6e6")
        плитки.pack(fill="both", expand=True)
        for номер, у in enumerate(в_комнате):
            текст = у["имя"] + ("\n(организатор)" if у["организатор"] else "\n") + \
                    "\nмикрофон: " + ("вкл" if у["микрофон"] else "выкл")
            tk.Label(плитки, text=текст, bg="#2b2b2b", fg="white", width=22, height=4).grid(
                row=номер // 3, column=номер % 3, padx=5, pady=5)
        if not в_комнате:
            tk.Label(плитки, bg="#e6e6e6", text="[ Видео-сетка участников ]").pack(expand=True)

    # ---------- кнопки ----------
    def _отправить(self) -> None:
        текст = self._сообщение.get()
        if текст.strip():
            self._сообщение.delete(0, "end")
            self._к["сообщение"](текст)

    def _микрофон(self) -> None:
        self._к["микрофон"](not self._микрофонВкл)

    def _экран(self) -> None:
        self._к["экран"](not self._экранВкл)

    # ---------- периодический опрос ----------
    def _опрос(self) -> None:
        try:
            if not self.winfo_exists():
                return
            self._к["опрос"]()  # интерфейс сам решит, что обновить (или уйти с экрана)
            if self.winfo_exists():
                self._идОпроса = self.after(self.ПЕРИОД_ОПРОСА_МС, self._опрос)
        except tk.TclError:
            pass  # экран закрыли во время опроса

    def _приУничтожении(self, событие) -> None:
        if событие.widget is self:
            try:
                self.after_cancel(self._идОпроса)
            except (tk.TclError, AttributeError):
                pass


# ======================================================================
class ОкноМодерации(tk.Toplevel):
    """Окно со списком участников: пустить из зала ожидания, дать/забрать микрофон.
    Открывается кнопкой «Участники» (метод ИнтерфейсОрганизатора.модерироватьВстречу)."""

    def __init__(self, master, при_допуске: Callable[[str], None],
                 при_микрофоне: Callable[[str, bool], None]) -> None:
        super().__init__(master)
        self.title("Участники встречи")
        self.geometry("460x360")
        self._при_допуске = при_допуске
        self._при_микрофоне = при_микрофоне
        self._подпись = None
        self._тело = ttk.Frame(self, padding=10)
        self._тело.pack(fill="both", expand=True)

    def обновить(self, участники: List[dict]) -> None:
        подпись = tuple((у["идЗаписи"], у["статус"], у["микрофон"]) for у in участники)
        if подпись == self._подпись:
            return
        self._подпись = подпись
        for виджет in self._тело.winfo_children():
            виджет.destroy()
        if not участники:
            ttk.Label(self._тело, text="Пока никого нет").pack()
        for у in участники:
            строка = ttk.Frame(self._тело)
            строка.pack(fill="x", pady=3)
            ttk.Label(строка, text="%s — %s" % (у["имя"], у["статус"]), width=34).pack(side="left")
            if у["организатор"]:
                continue
            if у["статус"] == "Зал ожидания":
                ttk.Button(строка, text="Пустить",
                           command=lambda ид=у["идЗаписи"]: self._при_допуске(ид)).pack(side="left")
            elif у["статус"] == "Подключён":
                подпись_кнопки = "Забрать микрофон" if у["микрофон"] else "Дать микрофон"
                ttk.Button(строка, text=подпись_кнопки,
                           command=lambda ид=у["идЗаписи"], в=not у["микрофон"]: self._при_микрофоне(ид, в)
                           ).pack(side="left")


# ======================================================================
class ЭкранСтатистики(ttk.Frame):
    """Макет «Экран статистики»."""

    def __init__(self, master, тема: str, посещаемость: int, всего: int, активность: int,
                 при_скачивании: Callable[[], None], при_возврате: Callable[[], None]) -> None:
        super().__init__(master, padding=20)
        ttk.Label(self, text="Экран статистики", font=ШРИФТ_ЗАГОЛОВКА).pack(pady=(30, 5))
        ttk.Label(self, text=тема, font=ШРИФТ_ЖИРНЫЙ).pack(pady=(0, 15))
        ttk.Label(self, text="Посещаемость: %d%%" % посещаемость, font=ШРИФТ_ОБЫЧНЫЙ).pack(pady=3)
        ttk.Label(self, text="Всего участников: %d" % всего, font=ШРИФТ_ОБЫЧНЫЙ).pack(pady=3)
        ttk.Label(self, text="Сообщений в чате: %d" % активность, font=ШРИФТ_ОБЫЧНЫЙ).pack(pady=3)
        кнопки = ttk.Frame(self)
        кнопки.pack(pady=20)
        ttk.Button(кнопки, text="Скачать отчет", command=при_скачивании).pack(side="left", padx=6)
        ttk.Button(кнопки, text="Назад", command=при_возврате).pack(side="left", padx=6)
