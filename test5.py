# from exchange import main as exchange
# print(exchange(3, 'PLN', 'gbp', 'aa'))

def plus(*args):
    s=0
    for i in args:
        s+=i
 
    return s

# l = [3,5,7]
# m = ''
# print(plus(*l, *m, 23))
from datetime import datetime
dt = datetime.now()
def logging_exchange(message):
    dt = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    log_message = rf'{dt} - {message}'
    return log_message

print(logging_exchange("Test message"))

