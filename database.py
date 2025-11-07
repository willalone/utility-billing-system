"""Модуль для работы с базой данных."""

from typing import Optional, Dict, List
from models import Street, PersonalAccount, Service, Charge


class Database:
    """Класс для работы с базой данных."""

    def __init__(self):
        """Инициализирует базу данных."""
        self._streets: Dict[int, Street] = {}
        self._accounts: Dict[int, PersonalAccount] = {}
        self._services: Dict[int, Service] = {}
        self._charges: Dict[int, Charge] = {}

    def add_street(self, street: Street) -> None:
        """
        Добавляет улицу в базу данных.

        Args:
            street: Объект улицы.
        """
        self._streets[street.street_code] = street

    def get_street(self, street_code: int) -> Optional[Street]:
        """
        Получает улицу по коду.

        Args:
            street_code: Код улицы.

        Returns:
            Объект улицы или None, если не найдена.
        """
        return self._streets.get(street_code)

    def add_account(self, account: PersonalAccount) -> None:
        """
        Добавляет лицевой счет в базу данных.

        Args:
            account: Объект лицевого счета.
        """
        self._accounts[account.account_code] = account

    def get_account(self, account_code: int) -> Optional[PersonalAccount]:
        """
        Получает лицевой счет по коду.

        Args:
            account_code: Код лицевого счета.

        Returns:
            Объект лицевого счета или None, если не найден.
        """
        return self._accounts.get(account_code)

    def get_account_by_number(self, account_number: str) -> Optional[PersonalAccount]:
        """
        Получает лицевой счет по номеру.

        Args:
            account_number: Номер лицевого счета.

        Returns:
            Объект лицевого счета или None, если не найден.
        """
        for account in self._accounts.values():
            if account.account_number == account_number:
                return account
        return None

    def add_service(self, service: Service) -> None:
        """
        Добавляет услугу в базу данных.

        Args:
            service: Объект услуги.
        """
        self._services[service.service_code] = service

    def get_service(self, service_code: int) -> Optional[Service]:
        """
        Получает услугу по коду.

        Args:
            service_code: Код услуги.

        Returns:
            Объект услуги или None, если не найдена.
        """
        return self._services.get(service_code)

    def add_charge(self, charge: Charge) -> None:
        """
        Добавляет начисление в базу данных.

        Args:
            charge: Объект начисления.
        """
        self._charges[charge.charge_code] = charge

    def get_charges_by_account(self, account_code: int) -> List[Charge]:
        """
        Получает все начисления по лицевому счету.

        Args:
            account_code: Код лицевого счета.

        Returns:
            Список начислений.
        """
        return [c for c in self._charges.values() if c.account_code == account_code]

    def get_all_streets(self) -> List[Street]:
        """
        Возвращает все улицы.

        Returns:
            Список всех улиц.
        """
        return list(self._streets.values())

    def get_all_accounts(self) -> List[PersonalAccount]:
        """
        Возвращает все лицевые счета.

        Returns:
            Список всех лицевых счетов.
        """
        return list(self._accounts.values())

    def get_all_services(self) -> List[Service]:
        """
        Возвращает все услуги.

        Returns:
            Список всех услуг.
        """
        return list(self._services.values())

    def get_all_charges(self) -> List[Charge]:
        """
        Возвращает все начисления.

        Returns:
            Список всех начислений.
        """
        return list(self._charges.values())

