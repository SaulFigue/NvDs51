from kafka import KafkaConsumer
import json
import time
import datetime

def insert_db(register):
    if register:
        print(f"0     || {register['date']} |||  {register['time']}  ||| {register['cc']:<2} ||  {register['camera']}  ||   {register['in']}    ||   {register['out']}    ||")

# ------------------------------------------------------- KAFKA FUNCTIONS ----------------------------------------

def construct_register(message):
    combined = {}
    if message:
        timestamp = datetime.datetime.now()
        date = timestamp.strftime("%Y-%m-%d")
        time = timestamp.strftime("%H:%M:%S")
        combined = {'date': date, 'time': time, 'cc': message['cc'], 'camera': message['camera'], 'in': message['in'], 'out': message['out']}

        return combined         

def consume_messages():
    try:
        for message in consumer:
            register = construct_register(message.value)
            insert_db(register)

    except KeyboardInterrupt:
        exit()

# --------------------------------------- MAIN CODE ---------------------------------------------

topic = 'quickstart-events'
consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'], 
                        value_deserializer=lambda v: json.loads(v.decode('utf-8')))

print("Index ||    Date    |||    Time    ||| CC || CAM || Ingreso || Salida ")
print("------++------------+++------------+++----++-----++---------++--------")

consume_messages()