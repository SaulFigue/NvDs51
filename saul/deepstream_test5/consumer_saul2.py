from kafka import KafkaConsumer
import json
import time
import datetime
import psycopg2



idx = 0

def insert_db(registers):
    global idx

    if registers:
        for reg in registers:
            idx += 1
            print(f"{idx:<2} ||   {reg['id_cc']}   ||  {reg['id_cam']}  ||  {reg['acceso_id']}  ||       {reg['nombre_comercial_acceso']}       || {reg['timestamp']} || {reg['date']} || {reg['year']} ||    {reg['month']}  ||   {reg['day']} ||   {reg['hour']}  ||    {reg['in']}     ||    {reg['out']}    ||")
            
            # Query para ingresar datos a la base
            # serie = f"select setval('"ing_vm_id_seq"', (select MAX(id) from ing_vm)+1);"
            # cadena = f"insert into ing_vm(id_cc, id_cam, acceso_id, nombre_comercial_acceso, timestamp, date, year, month, day, hour, ingresos, salidas) VALUES ({reg['id_cc']}, {reg['id_cam']}, '{reg['acceso_id']}', '{reg['nombre_comercial_acceso']}', '{reg['timestamp']}', '{reg['date']}', {reg['year']}, {reg['month']}, {reg['day']}, {reg['hour']}, {reg['in']}, {reg['out']});"
            # cur.execute(cadena)
            # conn.commit()
            # cur2.execute(cadena)
            # conn2.commit()


def datos_analytics(path_analytics):
    # ======= LEEREMOS EL ARCHIVO ANALITYCS PARA EXTRAER EL NOMBRE_COMERCIAL DE LA PUERTA DEL CC Y SUS ACCESO_IDS
    lineas = []
    with open(path_analytics, 'r') as analytics:
        for linea in analytics:
            lineas.append(linea)

    stream_ids = []
    # BUSCAMOS Y GUARDAMOS LOS STREAMS IDS
    for i in range (len(lineas)):
        if("line-crossing-stream-" in lineas[i]):
            #Aqui extraigo todo el line-crossing con el stream-x
            lc_stream = lineas[i]
            #Aca sacamos solo el id_number
            stream = ""#(0,1,2,3)
            for c in lc_stream:
                if c.isdigit():
                    stream += c
            stream_ids.append(stream)
    
    camaras = {}

    #camaras = {'cam0':{nm:[nm1,nm2,nm3],lc:[lc1,lc2,lc3]}, ...} 
    #           'cam0':{nm:[Fybeca,Fybeca,El Comercio], lc:[QN_CP_0,QN_CP_0,QN_CP_1]}
    for stream_id in stream_ids:
        cam_prt = "#cam"+stream_id
        nm = [] #lista para Nombre_comercial
        lc = [] #lista para acceso_id
        
        for i in range (len(lineas)):    
            if cam_prt in lineas[i]:
                aux = lineas[i].split("=")  # dividir variable y nombre [cam0-nm1,Fybeca]
                if len(aux)>1:
                    if "nm" in aux[0]:
                        nm.append(aux[1].strip()) #Guardar name/nombre_comercial
                    elif "lc" in aux[0]:
                        lc.append(aux[1].strip()) #Guardar lc/acceso_id

        #Creamos diccionario con todas las camaras y sus names nm y accesos_id lc
        camaras[cam_prt[1:]] = {'names':nm, 'lcs':lc} 

    #Devolvemos [{},{},{},{}] donde cada diccionario hace referencia a una cam, y sus names y lcs guardados
    return list(camaras.values())


# ------------------------------------------------------- KAFKA FUNCTIONS ----------------------------------------

def construct_register(messages):
    combined = {}
    if messages:
        
        Nombres_list = datos_analytics(path_analytics)

        # ======= AGREGAREMOS CONTENIDO A combined = {}
        for message in messages:
            cam = message['cam']
            num_puertas = len(Nombres_list[cam]["lcs"])

            nms_id = [] # lista de Nombres_comerciales sin repetidos
            lcs_id = [] # lista de accesos_ids sin repetidos
            lcs_label_in = [] # ["in-1","in-2"]
            lcs_label_out = [] # ["out-1","out-2","out3"]
            ingreso = [0]*num_puertas
            salida = [0]*num_puertas

            #Extraigo los names y lcs sin repetirlos
            for item in Nombres_list[cam]["names"]:
                if item not in nms_id:
                    nms_id.append(item)

            for item in Nombres_list[cam]["lcs"]:
                if item not in lcs_id:
                    lcs_id.append(item)


            # Para agrupar la suma de cada lc_in de acuerdo al cam_lcid
            for i in range(1,51):
                lc_in = "in-"+str(i)
                if(lc_in in message):
                    lcs_label_in.append(lc_in)
                    ingreso[i-1] += message[lc_in]

            # Para agrupar la suma de cada lc_out de acuerdo al cam_lcid 
            for i in range(1,51):
                lc_out = "out-"+str(i)
                if(lc_out in message):
                    lcs_label_out.append(lc_out)
                    salida[i-1] += message[lc_out]


            # Agrupo la suma de cada lc_in y lc_out de acuerdo a si son del mismo ID, o NAME
            ins = {} #{"QN_CP1": x}
            outs = {} #{"QN_CP1": x, "QN_CP12": x}

            for i in range(len(Nombres_list[cam]["lcs"])):
                key = Nombres_list[cam]["lcs"][i]
                value_in = ingreso[i]
                value_out = salida[i]
                if(value_in != 0):
                    if key in ins:
                        ins[key] += value_in
                    else:
                        ins[key] = value_in

                if(value_out != 0):
                    if key in outs:
                        outs[key] += value_out
                    else:
                        outs[key] = value_out
            
            #Aqui crearemos el conjunto de registros que se agruparon despues del tiempo = x seg
            for id,cam_lc in enumerate(lcs_id):

                #Si ya existe estallave, sumo las entradas y salidas respectivas
                if cam_lc in combined.keys():
                    if(cam_lc in ins):
                        combined[cam_lc]['in'] += ins[cam_lc]
                    if(cam_lc in outs):
                        combined[cam_lc]['out'] += outs[cam_lc]
                else:
                    #Si no, creo el registro por primera vez
                    timestamp = datetime.datetime.now()
                    date = timestamp.strftime("%Y-%m-%d")
                    year = timestamp.year
                    month = timestamp.month
                    day = timestamp.day
                    hour = timestamp.hour

                    #Quizas esto se pueda optimizar a futuro, 
                    #De momento las condiciones nos permiten controlar cuando enviar un 0 en 
                    #el conteo de in o out dependiendo si existe o no el lc-in o lc-out 
                    if ((cam_lc in ins) and (cam_lc in outs)):
                        combined[cam_lc] = {'id_cc': 1, 'id_cam': cam, 'acceso_id': cam_lc, 'nombre_comercial_acceso': nms_id[id], 'timestamp': timestamp, 'date': date, 'year': year, 'month': month, 'day': day, 'hour': hour, 'in': ins[cam_lc], 'out': outs[cam_lc]}
                    elif ((cam_lc in ins) and (cam_lc not in outs)):
                        combined[cam_lc] = {'id_cc': 1, 'id_cam': cam, 'acceso_id': cam_lc, 'nombre_comercial_acceso': nms_id[id], 'timestamp': timestamp, 'date': date, 'year': year, 'month': month, 'day': day, 'hour': hour, 'in': ins[cam_lc], 'out': 0}
                    elif ((cam_lc in outs) and (cam_lc not in ins)):
                        combined[cam_lc] = {'id_cc': 1, 'id_cam': cam, 'acceso_id': cam_lc, 'nombre_comercial_acceso': nms_id[id], 'timestamp': timestamp, 'date': date, 'year': year, 'month': month, 'day': day, 'hour': hour, 'in': 0, 'out': outs[cam_lc]}
                    
        combined_list = list(combined.values())
        return combined_list           

def clean_messages(partitions):
    # messages es una lista [] de diccionarios [{cam,in,out},{cam,in,out},{cam,in,out}]
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
            # partitions es una lista [] llena de ConsumerRecord(... values={cam,in,out}).. 
            # partitions = [ConRc(), ConRc(),...]
            partitions = []
            while time.time() - start_time < 30:
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

path_analytics = "/opt/nvidia/deepstream/deepstream-5.1/sources/apps/cc-lc/Ds-saul/deepstream_test5/configs/config_nvdsanalytics.txt"

print("id || id_cc || CAM || acceso_id || nombre_comercial_acceso ||          timestamp         ||    date    || year || month || day || hour || Ingresos || Salidas ||")
print("---++-------++-----++-----------++-------------------------++----------------------------++------------++------++-------++-----++------++----------++---------++")
consume_messages()
"""
try:
    #Conexion Azure
    conn = psycopg2.connect(
        dbname="postgres", # se puede buscar el nombre con \l
        user="postgres", # Se puede buscar el nombre con \du o SELECT usename FROM pg_user;
        password="clave", # Se puede cambiar contrasena con: ALTER USER nombre_de_usuario WITH PASSWORD 'nueva_contraseña';
        host="localhost", # por defecto
        port="10001" # por defecto, pero se puede buscar con: SELECT inet_server_addr() AS server_address, current_setting('port') AS port;p

    )
    #Conexion local
    conn2 = psycopg2.connect(
        dbname="pruebalc", # 
        user="postgres", # 
        password="12345", # 
        host="localhost", # 
        port="5432" # 

    )
    cur = conn.cursor()
    cur2 = conn2.cursor()
    consume_messages()
    cur.close()
    cur2.close()
    conn.close()
    conn2.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
"""
