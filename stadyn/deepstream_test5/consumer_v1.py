from kafka import KafkaConsumer
import json
import time
import datetime

def insert_db(registers):
    if registers:
        for idx, reg in enumerate(registers):
            print(f"{idx:<5} || {reg['date']} |||  {reg['time']}  ||| {reg['cc']:<2} ||  {reg['camera']}  ||   {reg['in']}    ||   {reg['out']}    ||")

# ------------------------------------------------------- KAFKA FUNCTIONS ----------------------------------------

def construct_register(messages):
    combined = {}
    if messages:
        for message in messages:
            cc = message['cc']
            cam = message['camera']
            ingreso = message['in']
            salida = message['out']
            if (cc, cam) in combined.keys():
                    combined[(cc, cam)]['in'] += ingreso
                    combined[(cc, cam)]['out'] += salida
            else:
                timestamp = datetime.datetime.now()
                date = timestamp.strftime("%Y-%m-%d")
                time = timestamp.strftime("%H:%M:%S")
                combined[(cc, cam)] = {'date': date, 'time': time, 'cc': cc, 'camera': cam, 'in': ingreso, 'out': salida}

        combined_list = list(combined.values())
        return combined_list           

def clean_messages(partitions):
    messages = []
    if partitions:
        for partition in partitions:
            message = partition.value
            if message is None:
                    continue
            else:
                messages.append(message)
        return messages

def consume_messages():
    try:
        while True:
            start_time = time.time()
            partitions = []
            while time.time() - start_time < 5:
                partition = consumer.poll(0).values()
                if partition:
                    partition = list(partition)[0]
                    partitions.extend(partition)

            messages = clean_messages(partitions)
            registers = construct_register(messages)
            insert_db(registers)

    except KeyboardInterrupt:
        exit()

# --------------------------------------- MAIN CODE ---------------------------------------------

topic = 'quickstart-events'
consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'], 
                        value_deserializer=lambda v: json.loads(v.decode('utf-8')))

print("Index ||    Date    |||    Time    ||| CC || CAM || Ingreso || Salida ")
print("------++------------+++------------+++----++-----++---------++--------")

consume_messages()