import config
from logger import Logger


class BasicKettle:
    def __init__(self, name, version):
        self.model = name
        self.version = version
        self.logger = Logger(config.DB_FILEPATH, config.TXT_FILEPATH)
        self.logs = []

        self.isPowered = False
        self.isBusy = False
        self.isWaitingWater = False

        self.water_amount = 0
        self.current_temperature = config.TEMPERATURE_MIN
        self.boiling_time_left = config.SECONDS_TO_BOIL

    def __str__(self):
        return f'{self.model}-{self.version}'

    def is_full(self):
        return True if self.water_amount == config.CAPACITY else False

    def is_empty(self):
        return True if self.water_amount == 0 else False

    # Переключатели состояний
    def switch_power(self):
        self.isPowered = not self.isPowered
        self.logger.full_log(f"ЧАЙНИК {'ВКЛЮЧЕН' if self.isPowered else 'ОТКЛЮЧЕН'}")

    def switch_busy(self):
        if not self.isPowered:
            self.logger.full_log('ОШИБКА')
        elif self.is_empty() and not self.isBusy:
            self.logger.full_log('ОШИБКА: Чайник пуст. Кипятить нечего. Налейте водички.')
        else:
            self.isBusy = not self.isBusy
            self.boiling_time_left = config.SECONDS_TO_BOIL
            self.logger.full_log(f"КИПЯЧЕНИЕ {'НАЧАТО' if self.isBusy else 'ОСТАНОВЛЕНО'}")

    def switch_waiting_water(self):
        self.isWaitingWater = not self.isWaitingWater

    # ---------------

    # Основной функционал
    def boil(self):
        temperature_raising_step = round((config.TEMPERATURE_MAX - self.current_temperature) / self.boiling_time_left,
                                         1)
        self.current_temperature += temperature_raising_step
        self.boiling_time_left -= 1

        if self.boiling_time_left == 0:
            self.switch_busy()
            self.logger.full_log('ЧАЙНИК ВСКИПЕЛ')

    def cool(self):
        self.current_temperature -= config.TEMPERATURE_COOLING_STEP
        if self.current_temperature < config.TEMPERATURE_MIN:
            self.current_temperature = config.TEMPERATURE_MIN

    def add_water(self, inserted_amount):
        # Чек на валидность количества воды
        if inserted_amount <= 0:
            pass
        # Вместимость не превышена и количество воды положительное
        else:
            if self.water_amount + inserted_amount > config.CAPACITY:
                self.water_amount = config.CAPACITY
                self.logger.full_log(
                    f"В чайнике {'не было' if self.is_empty() else f'было {self.water_amount} л'} воды,"
                    f"и вы попытались влить {inserted_amount} л."
                    "Теперь у вас есть полный чайник и лужа на полу.")
            else:
                self.water_amount += inserted_amount
                self.logger.full_log(
                    f'ВНЕСЕНИЕ ВОДЫ В ЧАЙНИК: {inserted_amount} л')  # Хахаха, надо обязательно оставить именно такую формулировку

    # ---------------

    # User
    def generate_CLI_interface(self, optional_message: str | None = None):
        logs = '\n\n'.join(self.logger.select_last_x_messages_from_db())
        command_panel = f"1. {'Отключить' if self.isPowered else 'Включить'} чайник" \
                        f"2. {'Остановить' if self.isBusy else 'Начать'} кипячение" \
                        "3. Налить водички"
        input_prompt = 'Введите количество водички (число с плавающей точкой)' if self.isWaitingWater else 'Введите номер команды [1-3]'

        interface = '--------------------\n'.join()
        return interface
    # ---------------


class MiMak1(BasicKettle):
    def __init__(self):
        super().__init__('MiMak', 1)
