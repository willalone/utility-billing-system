"""Модуль с классами для работы с базой данных."""

from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class Street:
    """Класс для представления улицы."""

    street_code: int
    name: str

    def __str__(self) -> str:
        """Строковое представление улицы."""
        return f"{self.name}"


@dataclass
class Service:
    """Класс для представления услуги."""

    service_code: int
    name: str
    tariff: float

    def __str__(self) -> str:
        """Строковое представление услуги."""
        return f"{self.name} (тариф: {self.tariff:.2f} руб.)"

    def calculate_cost(self, quantity: float) -> float:
        """
        Вычисляет стоимость услуги.

        Args:
            quantity: Количество услуги.

        Returns:
            Стоимость услуги.
        """
        return self.tariff * quantity


@dataclass
class PersonalAccount:
    """Класс для представления лицевого счета."""

    account_code: int
    account_number: str
    street_code: int
    house: str
    building: Optional[str]
    apartment: str
    full_name: str

    def __str__(self) -> str:
        """Строковое представление лицевого счета."""
        building_str = f", корп. {self.building}" if self.building else ""
        return (f"ЛС: {self.account_number}, "
                f"{self.apartment}{building_str}, "
                f"д. {self.house}, "
                f"{self.full_name}")

    def get_address(self, street: Optional[Street] = None) -> str:
        """
        Возвращает адрес лицевого счета.

        Args:
            street: Объект улицы (опционально).

        Returns:
            Адрес в виде строки.
        """
        street_name = street.name if street else f"Улица #{self.street_code}"
        building_str = f", корп. {self.building}" if self.building else ""
        return f"{street_name}, д. {self.house}{building_str}, кв. {self.apartment}"


@dataclass
class Charge:
    """Класс для представления начисления."""

    charge_code: int
    account_code: int
    service_code: int
    quantity: float

    def __str__(self) -> str:
        """Строковое представление начисления."""
        return (f"Начисление #{self.charge_code}: "
                f"ЛС #{self.account_code}, "
                f"Услуга #{self.service_code}, "
                f"Количество: {self.quantity}")


@dataclass
class PaymentNotice:
    """Класс для представления извещения на оплату."""

    account: PersonalAccount
    street: Street
    charges: List[Tuple[Charge, Service]]
    period_month: int
    period_year: int
    total_amount: float

    def __str__(self) -> str:
        """Строковое представление извещения."""
        return (f"Извещение на оплату для ЛС {self.account.account_number}, "
                f"период {self.period_month}/{self.period_year}, "
                f"сумма: {self.total_amount:.2f} руб.")

