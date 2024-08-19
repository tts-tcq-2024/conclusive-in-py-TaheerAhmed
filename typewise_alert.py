from abc import ABC, abstractmethod

class typewise_alert:
    # Breach classification strategies
    class CoolingType(ABC):
        @abstractmethod
        def classify_breach(self, temperature_in_c):
            pass

    class PassiveCooling(CoolingType):
        def classify_breach(self, temperature_in_c):
            return typewise_alert.infer_breach(temperature_in_c, 0, 35)

    class HiActiveCooling(CoolingType):
        def classify_breach(self, temperature_in_c):
            return typewise_alert.infer_breach(temperature_in_c, 0, 45)

    class MedActiveCooling(CoolingType):
        def classify_breach(self, temperature_in_c):
            return typewise_alert.infer_breach(temperature_in_c, 0, 40)

    # Alert strategies
    class Alert(ABC):
        @abstractmethod
        def send_alert(self, breach_type):
            pass

    class ControllerAlert(Alert):
        def send_alert(self, breach_type):
            return f'Controller Alert: {breach_type}'

    class EmailAlert(Alert):
        def send_alert(self, breach_type):
            recipient = "a.b@c.com"
            if breach_type == 'TOO_LOW':
                return f'To: {recipient}\nHi, the temperature is too low'
            elif breach_type == 'TOO_HIGH':
                return f'To: {recipient}\nHi, the temperature is too high'
            return 'No action needed'

    # Function used in strategies
    @staticmethod
    def infer_breach(value, lower_limit, upper_limit):
        if value < lower_limit:
            return 'TOO_LOW'
        if value > upper_limit:
            return 'TOO_HIGH'
        return 'NORMAL'

    # Core function using strategies
    @staticmethod
    def check_and_alert(alert_strategy, cooling_type_strategy, temperature_in_c):
        breach_type = cooling_type_strategy.classify_breach(temperature_in_c)
        return alert_strategy.send_alert(breach_type)
