from abc import ABC, abstractmethod
def infer_breach(value, lowerLimit, upperLimit):
        if value < lowerLimit:
            return 'TOO_LOW'
        if value > upperLimit:
            return 'TOO_HIGH'
        return 'NORMAL'
# Breach classification strategies
class CoolingType(ABC):
    @abstractmethod
    def classify_breach(self, temperature_in_c):
        pass
    

class PassiveCooling(CoolingType):
    def classify_breach(self, temperature_in_c):
        return infer_breach(temperature_in_c, 0, 35)

class HiActiveCooling(CoolingType):
    def classify_breach(self, temperature_in_c):
        return infer_breach(temperature_in_c, 0, 45)

class MedActiveCooling(CoolingType):
    def classify_breach(self, temperature_in_c):
        return infer_breach(temperature_in_c, 0, 40)

# Alert strategies
class Alert(ABC):
    @abstractmethod
    def send_alert(self, breach_type):
        pass

class ControllerAlert(Alert):
    def send_alert(self, breach_type):
        header = 0xfeed
        print(f'{header}, {breach_type}')

class EmailAlert(Alert):
    def send_alert(self, breach_type):
        recipient = "a.b@c.com"
        if breach_type == 'TOO_LOW':
            print(f'To: {recipient}')
            print('Hi, the temperature is too low')
        elif breach_type == 'TOO_HIGH':
            print(f'To: {recipient}')
            print('Hi, the temperature is too high')

# Core function using strategies
def check_and_alert(alert_strategy, cooling_type_strategy, temperature_in_c):
    breach_type = cooling_type_strategy.classify_breach(temperature_in_c)
    alert_strategy.send_alert(breach_type)

# Usage
cooling_type = HiActiveCooling()  # Or PassiveCooling(), MedActiveCooling()
alert = ControllerAlert()  # Or EmailAlert()

check_and_alert(alert, cooling_type, 50)
