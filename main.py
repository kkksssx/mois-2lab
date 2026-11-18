"""Точка входа (<<main>>): python main.py"""
import os
import sys

# чтобы запуск работал из любой папки
КОРЕНЬ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, КОРЕНЬ)

from app.injector import Инжектор  # noqa: E402


def main() -> None:
    окно = Инжектор(os.path.join(КОРЕНЬ, "data")).собрать()
    окно.запустить()


if __name__ == "__main__":
    main()
