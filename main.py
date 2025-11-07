"""Главный модуль программы для работы с извещениями на оплату."""

from database import Database
from models import Street, PersonalAccount, Service, Charge, PaymentNotice
from chain_of_responsibility import ChargeProcessor
from excel_generator import ExcelGenerator
from date_time_utils import DateTimeHandler


def init_database() -> Database:
    """
    Инициализирует базу данных тестовыми данными.

    Returns:
        База данных с тестовыми данными.
    """
    db = Database()

    # Добавляем улицы
    streets = [
        Street(street_code=1, name="Ленина"),
        Street(street_code=2, name="Пушкина"),
        Street(street_code=3, name="Гагарина"),
    ]
    for street in streets:
        db.add_street(street)

    # Добавляем услуги
    services = [
        Service(service_code=1, name="Холодное водоснабжение", tariff=45.50),
        Service(service_code=2, name="Горячее водоснабжение", tariff=180.30),
        Service(service_code=3, name="Электроэнергия", tariff=4.65),
        Service(service_code=4, name="Отопление", tariff=2200.00),
        Service(service_code=5, name="Газоснабжение", tariff=6.40),
    ]
    for service in services:
        db.add_service(service)

    # Добавляем лицевые счета
    accounts = [
        PersonalAccount(
            account_code=1,
            account_number="ЛС-001",
            street_code=1,
            house="10",
            building="А",
            apartment="15",
            full_name="Иванов Иван Иванович"
        ),
        PersonalAccount(
            account_code=2,
            account_number="ЛС-002",
            street_code=2,
            house="25",
            building=None,
            apartment="42",
            full_name="Петрова Мария Сергеевна"
        ),
        PersonalAccount(
            account_code=3,
            account_number="ЛС-003",
            street_code=3,
            house="5",
            building="Б",
            apartment="8",
            full_name="Сидоров Петр Александрович"
        ),
    ]
    for account in accounts:
        db.add_account(account)

    # Добавляем начисления
    charges = [
        Charge(charge_code=1, account_code=1, service_code=1, quantity=15.5),
        Charge(charge_code=2, account_code=1, service_code=2, quantity=12.3),
        Charge(charge_code=3, account_code=1, service_code=3, quantity=350.0),
        Charge(charge_code=4, account_code=2, service_code=1, quantity=10.0),
        Charge(charge_code=5, account_code=2, service_code=3, quantity=280.0),
        Charge(charge_code=6, account_code=2, service_code=4, quantity=2.5),
        Charge(charge_code=7, account_code=3, service_code=1, quantity=18.0),
        Charge(charge_code=8, account_code=3, service_code=2, quantity=14.5),
        Charge(charge_code=9, account_code=3, service_code=3, quantity=420.0),
        Charge(charge_code=10, account_code=3, service_code=5, quantity=25.0),
    ]
    for charge in charges:
        db.add_charge(charge)

    return db


def create_payment_notice(
    db: Database,
    account_code: int,
    period_month: int,
    period_year: int
) -> PaymentNotice:
    """
    Создает извещение на оплату для указанного лицевого счета.

    Args:
        db: База данных.
        account_code: Код лицевого счета.
        period_month: Месяц периода начисления.
        period_year: Год периода начисления.

    Returns:
        Объект извещения на оплату.

    Raises:
        ValueError: Если лицевой счет не найден.
    """
    account = db.get_account(account_code)
    if not account:
        raise ValueError(f"Лицевой счет с кодом {account_code} не найден")

    street = db.get_street(account.street_code)
    if not street:
        raise ValueError(f"Улица с кодом {account.street_code} не найдена")

    charges = db.get_charges_by_account(account_code)
    charge_service_pairs = []
    for charge in charges:
        service = db.get_service(charge.service_code)
        if service:
            charge_service_pairs.append((charge, service))

    if not charge_service_pairs:
        raise ValueError(f"Начисления для лицевого счета {account_code} не найдены")

    return PaymentNotice(
        account=account,
        street=street,
        charges=charge_service_pairs,
        period_month=period_month,
        period_year=period_year,
        total_amount=0.0
    )


def main():
    """Главная функция программы."""
    print("Программа для генерации извещений на оплату")
    print("=" * 50)

    # Инициализация базы данных
    db = init_database()
    print("База данных инициализирована")

    # Инициализация процессора начислений
    processor = ChargeProcessor()
    print("Процессор начислений инициализирован (Chain of Responsibility)")

    # Инициализация генератора Excel
    excel_gen = ExcelGenerator()
    print("Генератор Excel инициализирован")

    # Получение текущего месяца и года
    date_handler = DateTimeHandler()
    current_date = date_handler.get_current_date()
    period_month = current_date.month
    period_year = current_date.year

    # Пример: создание извещения для первого лицевого счета
    try:
        account_code = 1
        notice = create_payment_notice(db, account_code, period_month, period_year)
        print(f"\nСоздано извещение для лицевого счета {notice.account.account_number}")

        # Обработка начислений через Chain of Responsibility
        notice = processor.process_notice(notice)
        print(f"Начисления обработаны. Итоговая сумма: {notice.total_amount:.2f} руб.")

        # Генерация Excel-файла
        file_path = f"извещение_ЛС_{notice.account.account_number}.xlsx"
        excel_gen.generate_payment_notice(notice, file_path)
        print(f"Excel-файл создан: {file_path}")

        # Дополнительные примеры для других счетов
        print("\n" + "=" * 50)
        print("Создание извещений для других счетов...")
        
        for acc_code in [2, 3]:
            try:
                notice = create_payment_notice(db, acc_code, period_month, period_year)
                notice = processor.process_notice(notice)
                file_path = f"извещение_ЛС_{notice.account.account_number}.xlsx"
                excel_gen.generate_payment_notice(notice, file_path)
                print(f"  - Извещение для ЛС {notice.account.account_number}: {notice.total_amount:.2f} руб.")
            except ValueError as e:
                print(f"  - Ошибка для счета {acc_code}: {e}")

    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    print("\n" + "=" * 50)
    print("Программа завершена успешно!")


if __name__ == "__main__":
    main()

