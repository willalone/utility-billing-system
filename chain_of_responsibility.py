"""Модуль с реализацией паттерна Chain of Responsibility для обработки начислений."""

from abc import ABC, abstractmethod
from typing import Optional
from models import Charge, Service, PaymentNotice


class ChargeHandler(ABC):
    """Абстрактный обработчик начислений (звено цепи ответственности)."""

    def __init__(self):
        """Инициализирует обработчик."""
        self._next_handler: Optional['ChargeHandler'] = None

    def set_next(self, handler: 'ChargeHandler') -> 'ChargeHandler':
        """
        Устанавливает следующий обработчик в цепи.

        Args:
            handler: Следующий обработчик.

        Returns:
            Установленный обработчик (для удобства цепочки).
        """
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, charge: Charge, service: Service) -> Optional[float]:
        """
        Обрабатывает начисление.

        Args:
            charge: Объект начисления.
            service: Объект услуги.

        Returns:
            Обработанная стоимость или None, если обработка не выполнена.
        """
        pass

    def _process_next(self, charge: Charge, service: Service) -> Optional[float]:
        """
        Передает обработку следующему звену цепи.

        Args:
            charge: Объект начисления.
            service: Объект услуги.

        Returns:
            Результат обработки следующего звена или None.
        """
        if self._next_handler:
            return self._next_handler.handle(charge, service)
        return None


class StandardChargeHandler(ChargeHandler):
    """Стандартный обработчик начислений (базовая обработка)."""

    def handle(self, charge: Charge, service: Service) -> Optional[float]:
        """
        Обрабатывает начисление стандартным способом.

        Args:
            charge: Объект начисления.
            service: Объект услуги.

        Returns:
            Стоимость услуги.
        """
        return service.calculate_cost(charge.quantity)


class DiscountChargeHandler(ChargeHandler):
    """Обработчик начислений с применением скидки."""

    def __init__(self, discount_threshold: float, discount_percent: float):
        """
        Инициализирует обработчик скидок.

        Args:
            discount_threshold: Порог суммы для применения скидки.
            discount_percent: Процент скидки (0-100).
        """
        super().__init__()
        self.discount_threshold = discount_threshold
        self.discount_percent = discount_percent

    def handle(self, charge: Charge, service: Service) -> Optional[float]:
        """
        Обрабатывает начисление с учетом скидки.

        Args:
            charge: Объект начисления.
            service: Объект услуги.

        Returns:
            Стоимость услуги со скидкой или передача следующему звену.
        """
        base_cost = service.calculate_cost(charge.quantity)
        if base_cost >= self.discount_threshold:
            discount = base_cost * (self.discount_percent / 100)
            return base_cost - discount
        return self._process_next(charge, service)


class PenaltyChargeHandler(ChargeHandler):
    """Обработчик начислений с применением пени за просрочку."""

    def __init__(self, penalty_percent: float):
        """
        Инициализирует обработчик пени.

        Args:
            penalty_percent: Процент пени за просрочку (0-100).
        """
        super().__init__()
        self.penalty_percent = penalty_percent

    def handle(self, charge: Charge, service: Service) -> Optional[float]:
        """
        Обрабатывает начисление с учетом пени.

        Args:
            charge: Объект начисления.
            service: Объект услуги.

        Returns:
            Стоимость услуги с пеней (всегда применяется).
        """
        base_cost = service.calculate_cost(charge.quantity)
        penalty = base_cost * (self.penalty_percent / 100)
        return base_cost + penalty


class ValidationChargeHandler(ChargeHandler):
    """Обработчик начислений для валидации данных."""

    def handle(self, charge: Charge, service: Service) -> Optional[float]:
        """
        Валидирует начисление перед обработкой.

        Args:
            charge: Объект начисления.
            service: Объект услуги.

        Returns:
            Передает обработку следующему звену или None при ошибке.
        """
        if charge.quantity < 0:
            raise ValueError(f"Отрицательное количество для начисления #{charge.charge_code}")
        if service.tariff < 0:
            raise ValueError(f"Отрицательный тариф для услуги #{service.service_code}")
        return self._process_next(charge, service)


class ChargeProcessor:
    """Класс для обработки начислений с использованием Chain of Responsibility."""

    def __init__(self):
        """Инициализирует процессор начислений."""
        # Создаем цепочку обработчиков
        validation = ValidationChargeHandler()
        discount = DiscountChargeHandler(discount_threshold=5000.0, discount_percent=5.0)
        standard = StandardChargeHandler()

        # Формируем цепочку: валидация -> скидка -> стандартная обработка
        validation.set_next(discount).set_next(standard)
        self._handler = validation

    def process_charge(self, charge: Charge, service: Service) -> float:
        """
        Обрабатывает начисление через цепочку ответственности.

        Args:
            charge: Объект начисления.
            service: Объект услуги.

        Returns:
            Итоговая стоимость начисления.

        Raises:
            ValueError: Если начисление не может быть обработано.
        """
        result = self._handler.handle(charge, service)
        if result is None:
            raise ValueError(f"Не удалось обработать начисление #{charge.charge_code}")
        return result

    def process_notice(self, notice: PaymentNotice) -> PaymentNotice:
        """
        Обрабатывает все начисления в извещении.

        Args:
            notice: Объект извещения на оплату.

        Returns:
            Извещение с обработанными начислениями.
        """
        processed_charges = []
        total_amount = 0.0

        for charge, service in notice.charges:
            cost = self.process_charge(charge, service)
            processed_charges.append((charge, service))
            total_amount += cost

        notice.total_amount = total_amount
        return notice

