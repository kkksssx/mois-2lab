"""Небольшие вспомогательные виджеты tkinter."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class ПрокручиваемаяОбласть(ttk.Frame):
    """Рамка с вертикальной прокруткой (нужна для списка карточек мероприятий)."""

    def __init__(self, master) -> None:
        super().__init__(master)
        self._холст = tk.Canvas(self, highlightthickness=0)
        полоса = ttk.Scrollbar(self, orient="vertical", command=self._холст.yview)
        self.внутри = ttk.Frame(self._холст)
        self._окно = self._холст.create_window((0, 0), window=self.внутри, anchor="nw")
        # при изменении размеров подгоняем область прокрутки и ширину содержимого
        self.внутри.bind("<Configure>",
                         lambda e: self._холст.configure(scrollregion=self._холст.bbox("all")))
        self._холст.bind("<Configure>",
                         lambda e: self._холст.itemconfigure(self._окно, width=e.width))
        self._холст.configure(yscrollcommand=полоса.set)
        self._холст.pack(side="left", fill="both", expand=True)
        полоса.pack(side="right", fill="y")
        # колесо мыши (Windows/macOS и Linux)
        self._холст.bind_all("<MouseWheel>", self._колесо, add="+")
        self._холст.bind_all("<Button-4>", self._колесо, add="+")
        self._холст.bind_all("<Button-5>", self._колесо, add="+")

    def _колесо(self, событие) -> None:
        try:
            if not self._холст.winfo_exists():
                return
            if getattr(событие, "num", 0) == 4 or getattr(событие, "delta", 0) > 0:
                self._холст.yview_scroll(-1, "units")
            else:
                self._холст.yview_scroll(1, "units")
        except tk.TclError:
            pass  # область уже закрыта, а обработчик остался — просто игнорируем
