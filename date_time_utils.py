"""Модуль для работы с датой и временем."""

from datetime import datetime, date, timedelta
from typing import Optional


class DateTimeHandler:
    """Класс для работы с датой и временем."""

    @staticmethod
    def get_current_date() -> date:
        """
        Возвращает текущую дату.

        Returns:
            Объект date с текущей датой.
        """
        return date.today()

    @staticmethod
    def get_current_datetime() -> datetime:
        """
        Возвращает текущую дату и время.

        Returns:
            Объект datetime с текущей датой и временем.
        """
        return datetime.now()

    @staticmethod
    def format_date(d: date, fmt: str = "%d.%m.%Y") -> str:
        """
        Форматирует дату в строку.

        Args:
            d: Дата для форматирования.
            fmt: Формат даты (по умолчанию "%d.%m.%Y").

        Returns:
            Отформатированная строка с датой.
        """
        return d.strftime(fmt)

    @staticmethod
    def parse_date(date_str: str, fmt: str = "%d.%m.%Y") -> Optional[date]:
        """
        Парсит строку в дату.

        Args:
            date_str: Строка с датой.
            fmt: Формат даты (по умолчанию "%d.%m.%Y").

        Returns:
            Объект date или None, если парсинг не удался.
        """
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            return None

    @staticmethod
    def add_days(d: date, days: int) -> date:
        """
        Добавляет дни к дате.

        Args:
            d: Исходная дата.
            days: Количество дней для добавления.

        Returns:
            Новая дата.
        """
        return d + timedelta(days=days)

    @staticmethod
    def get_period_start(period_month: int, period_year: int) -> date:
        """
        Возвращает начало периода (месяца).

        Args:
            period_month: Номер месяца (1-12).
            period_year: Год.

        Returns:
            Дата начала периода.
        """
        return date(period_year, period_month, 1)

    @staticmethod
    def get_period_end(period_month: int, period_year: int) -> date:
        """
        Возвращает конец периода (месяца).

        Args:
            period_month: Номер месяца (1-12).
            period_year: Год.

        Returns:
            Дата конца периода.
        """
        if period_month == 12:
            return date(period_year, 12, 31)
        next_month = date(period_year, period_month + 1, 1)
        return next_month - timedelta(days=1)

    @staticmethod
    def get_month_name(month: int) -> str:
        """
        Возвращает название месяца на русском языке.

        Args:
            month: Номер месяца (1-12).

        Returns:
            Название месяца.
        """
        months = {
            1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
            5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
            9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
        }
        return months.get(month, "Неизвестно")

