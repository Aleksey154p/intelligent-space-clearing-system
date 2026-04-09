"""
cli.py — ввод и вывод, никакой логики
"""

import messages as msg
from solver import RouteResult


def show_welcome() -> None:
    print(msg.WELCOME)


def get_range_choice() -> str:
    """
    Показать меню и получить выбор пользователя
    Возвращает: "1", "2" или "0"
    """
    print(msg.MENU_SELECT_RANGE)
    return input(msg.MENU_PROMPT).strip()


def show_invalid_choice() -> None:
    print(msg.MENU_INVALID)


def show_row2_disabled() -> None:
    print(msg.MENU_ROW2_DISABLED)


def show_analyzing() -> None:
    print(msg.ANALYZING)


def show_result(result: RouteResult) -> None:
    """Показать результат solver"""
    print(msg.RESULT_HEADER)
    if not result.success:
        print(msg.NO_SOLUTION.format(error=result.error))
    else:
        print(msg.RESULT_SOURCE.format(source=result.source))
        print(msg.RESULT_TARGET.format(target=result.target))
        print(msg.RESULT_EO.format(eo_count=result.eo_count))
        print(msg.RESULT_SCORE.format(score=result.score))
        print(msg.RESULT_HINT)
    print(msg.RESULT_FOOTER)


def ask_continue() -> bool:
    """
    Спросить продолжать или выйти
    Возвращает True — продолжить, False — выйти
    """
    print(msg.CONTINUE)
    return input(msg.CONTINUE_PROMPT).strip() != "0"


def show_goodbye() -> None:
    print(msg.GOODBYE)
