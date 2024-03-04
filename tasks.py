import time

def send_message(name:str)-> None:
    print(f'sending message to {name}')
    time.sleep(3)
    print('message sent! \n')