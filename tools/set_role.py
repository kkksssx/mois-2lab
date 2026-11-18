"""Меняет роль пользователя (в макете регистрации поля «роль» нет).

Пример:  python tools/set_role.py user@mail.ru Организатор
"""
import os
import sys

КОРЕНЬ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, КОРЕНЬ)

from app.controllers import КонтроллерПользователей  # noqa: E402
from app.model import Репозиторий  # noqa: E402


def main() -> None:
    if len(sys.argv) != 3:
        print("Использование: python tools/set_role.py <email> <Организатор|Участник>")
        return
    email, роль = sys.argv[1].lower(), sys.argv[2]
    репо = Репозиторий(os.path.join(КОРЕНЬ, "data", "storage.pkl"))
    for пользователь in репо.пользователи.values():
        if пользователь.email.lower() == email:
            КонтроллерПользователей(репо).управлениеПравами(пользователь.идПользователя, роль)
            print("Готово: %s теперь %s" % (пользователь.имя, роль))
            return
    print("Пользователь с таким email не найден")


if __name__ == "__main__":
    main()
