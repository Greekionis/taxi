import json
import pickle
from random import randint
import logging
import json_log_formatter


class Observer:      # Абстрактный наблюдатель
    def update(self, message):
        pass


class Viewer(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print('Для {}: {}'.format(self.name, message))


class Observable:           # Абстрактный наблюдаемый
    def __init__(self):
        self.observers = []     # инициализация списка наблюдателей

    def add_viewer(self, observer: Observer):
        self.observers.append(observer)

    def send_notify(self, message):       # Передача сообщения всем наблюдателям
        for observer in self.observers:
            observer.update(message)


class Alarm(Observable):
    def add_notify(self, data):
        self.send_notify(data)


class Log:  # Интерфейс логирования
    def loging(self, stroke):
        pass

    @staticmethod
    def clear_log(self):
        pass


class TxtFileLog(Log):     # Запись в txt
    def __init__(self, strng):
        self.__strng = strng

    def loging(self, stroke):
        with open(self.__strng, 'a', encoding='UTF-8') as f:
            f.write(stroke)
            print("Записано в txt")

    @staticmethod
    def clear_log(stroke):
        with open(stroke, 'w', encoding='UTF-8') as f:
            f.write("")


class JsonFileLog(Log):     # Запись в Json, что-то даже пишет)
    def __init__(self, strng):
        self.__strng = strng

    def loging(self, stroke):
        json_handler = logging.FileHandler(self.__strng)
        json_handler.setFormatter(formatter)
        logger = logging.getLogger(stroke)
        logger.addHandler(json_handler)
        logger.setLevel(logging.INFO)
        logger.info(stroke)
        logger.debug(stroke)


    @staticmethod
    def clear_log(stroke):
        with open(stroke, 'w', encoding='UTF-8') as f:
            json.dumps("")


class PickleLog(Log):       # Запись в bin
    def __init__(self, strng):
        self.__strng = strng

    def loging(self, stroke):
        with open(self.__strng, 'wb') as f:
            pickle.dump(stroke, f)
            print("Записано в bin")

    @staticmethod
    def clear_log(stroke):
        pass
        # with open(stroke, 'wb') as f:
        #     pickle.dump("", f)

class TaxiLogging:
    @staticmethod
    def set_writer(type_log):
        writer_type = {1: TxtFileLog,
                       2: JsonFileLog,
                       3: PickleLog}
        try:
            return writer_type[type_log]  # ()
        except:
            return Log()


class Taxi:  # Интерфейс захвата машины
    def action(self, price):
        pass


class CatchTaxi(Taxi):  # Стратегия при подходящей машине
    def action(self, price):
        car_num = taxi_queue.index_car(price)       # Подходящая под требования машина
        p_log = "Клиент уехал на такси №{}".format(car_num) # Для протоколирования
        taxi_queue.get_car(price)  # Берем и уезжаем
        taxi_queue.append(randint(10, 100))  # Подъезжает новая
        p_log = [p_log, taxi_queue.print]
        return p_log


class NoTaxi(Taxi):     # Стратегия при неподходящей машине
    def action(self, car):
        print(f"Нет подходящей, самая дешевая: {taxi_queue.min_el}")
        taxi_queue.append(randint(10, 100))         # Подъезжает новая
        print("Список машин - {}".format(taxi_queue.print))
        yy(file).loging("Список машин - {}".format(taxi_queue.print))  # Запись в журнал


class TaxiCon:
    _success = False

    def __init__(self, price, strategy: Taxi):
        self._strategy = strategy
        self.its_my_car = taxi_queue.less_or_equal_than(price)
        self.find_car(self.its_my_car)
        self.log = None

    def find_car(self, price):
        while self._success is False:   # Пока не найду машину
            if self.its_my_car is not None:     # Найдена машина
                self.log = self._strategy.action(self, price)
                self._success = True   # Найдена машина
                self.log = str("{},  Очередь машин: {}".format(self.log[0], self.log[1][1:-1]))
                Notification.send_notify(self.log)          # Уведомление наблюдателей
                yy(file).loging(self.log)       # Запись в журнал
            else:   # Не найдена машина
                self._strategy = NoTaxi
                self._strategy.action(self, price)
                self.__init__(my_price, CatchTaxi)  # Корректен ли такой способ рекурсии? Понятно, что не O(1)


class Node:
    def __init__(self, prev=None, nxt=None, value=None):
        self.value = value
        self.nxt = nxt
        self.prev = prev

    def set_next(self, nxt):
        self.nxt = nxt

    def set_prev(self, prev):
        self.prev = prev

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class LinkedList:
    def __init__(self):
        self.first = None
        self.last = None

    def append(self, value):
        if self.first is None:
            self.last = self.first = Node(None, None, value)
        else:
            new_node = Node(self.last, None, value)
            self.last.nxt = new_node
            self.last = new_node

    def clear(self):
        self.__init__()

    def less_or_equal_than(self, value):
        if self.first is not None:
            current_node = self.first
            while current_node is not None:
                if current_node.value <= value:
                    return current_node
                else:
                    current_node = current_node.nxt

    def get_car(self, current_node):
        if current_node.nxt is not None and current_node.prev is not None:
            current_node.prev.set_next(current_node.nxt)
            current_node.nxt.set_prev(current_node.prev)
        elif current_node.nxt is not None and current_node.prev is None:
            current_node.nxt.set_prev(None)
            self.first = current_node.nxt
        else:
            current_node.prev.set_next(None)
        return current_node

    def index_car(self, price):
        i = 1
        current_node = self.first
        while current_node is not price:
            if current_node.nxt is not None:
                i += 1
                current_node = current_node.nxt
            else:
                return None
        return i

    @property
    def min_el(self):
        current_node = self.first
        minim = self.first.value
        while current_node is not self.last:
            if current_node.value < minim:
                minim = current_node.value
            current_node = current_node.nxt
        return minim

    @property
    def print(self):
        if self.first is not None:
            current_node = self.first
            out = '[' + str(current_node.value) + ', '
            while current_node.nxt is not None:
                current_node = current_node.nxt
                out += str(current_node.value) + ', '
            return out[:-2] + ']'
        return 'LinkedList []'


if __name__ == "__main__":
    taxi_queue = LinkedList()
    for i in range(10):
        taxi_queue.append(randint(10, 100))

    formatter = json_log_formatter.JSONFormatter()

    #my_price = input('Please input your price >')
    my_price = 15
    #type_log = input('Please log type(1 - txt, 2 - Json, 3 - BinFile >')
    type_log = 2
    file = "logfile.txt"

    yy = TaxiLogging().set_writer(type_log)     # Почему () у TaxiLogging ???
    yy.clear_log(file)      # Очистка лога от предыдущей информации

    Notification = Alarm()
    Notification.add_viewer(Viewer("Диспетчер"))        # Подключения наблюдателей
    Notification.add_viewer(Viewer("ОТК"))

    TaxiCon(my_price, CatchTaxi)        # Вызываю стратегию "поймать такси", мне ведь нужно "поймать", а не "не поймать"
