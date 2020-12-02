import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_stats(self, days_amount):
        result = 0
        past_date = dt.date.today() - dt.timedelta(days=days_amount)
        today = dt.date.today()
        result = sum(rez.amount for rez in self.records 
                        if past_date < rez.date <= today)
        return result

    def rem(self):
        remained = self.limit - self.get_today_stats()
        return remained
        
    def get_today_stats(self):
        return self.get_stats(1)

    def get_week_stats(self):
        return self.get_stats(7)


class Record:
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, amount, comment, date=dt.date.today()):
        self.amount = amount
        self.comment = str(comment)
        if not isinstance(date, dt.date):
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()
        else:
            self.date = date


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        msg = (f'Сегодня можно съесть что-нибудь ещё, но с общей'
                f' калорийностью не более {abs(self.rem())} кКал')
        return msg if self.rem() > 0 else f'Хватит есть!'


class CashCalculator(Calculator):
    EURO_RATE = 90.0
    USD_RATE = 76.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        if round(self.rem(), 2) == 0:
            return f"Денег нет, держись"
        currency_switch = {
            'rub': (self.RUB_RATE, "руб"),
            'usd': (self.USD_RATE, "USD"),
            'eur': (self.EURO_RATE, "Euro")
        }
        cur_val = round((abs(self.rem()) / currency_switch[currency][0]), 2)
        currency_str = (f"{cur_val} {currency_switch[currency][1]}")  
        msg = f"Денег нет, держись: твой долг - {currency_str}"
        return msg if self.rem() < 0 else f"На сегодня осталось {currency_str}"


if __name__ == "__main__":
    cash_calculator = CashCalculator(3)
    cash_calculator.add_record(Record(amount=0.1, comment='кофе'))
    cash_calculator.add_record(Record(amount=0.2, comment='Сереге за обед'))
    print(cash_calculator.get_today_cash_remained('rub'))
    