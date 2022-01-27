import pika
import json
import socket

# Incoming message will be a dict that looks like this: {"Metric": metric, "Msg": str(msg), "Ts": ts}
#


GRPHT_S = 'graphite'
GRPHT_P = 2003

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', connection_attempts=12, retry_delay=5))
GrphtQueue = connection.channel()
GrphtQueue.queue_declare(queue='Grpht_Queue', durable=True)

# TODO: On/off config for Graphite. If it's off empty into the void.
#  UPDATE: Abandoning Graphite. Sending to void implemented as "If True"

def ProcessMessage(ch, method, properties, body):
    print(" [X] Received. Processing... \n")
    j = json.loads(body.decode())
    metric = j["Metric"]
    msg = j["Msg"]
    ts = j["Ts"]
    frmtmsg = "{} {} {}\n".format(metric, str(msg), ts).encode('utf-8')
    if True:
        print("[ VOID PROTOCOL INITIATED ] \n MSG = {}".format(frmtmsg))
    else:
        sock = socket.socket()
        sock.connect((GRPHT_S, GRPHT_P))
        sock.sendall(frmtmsg)
        sock.close()
    print(" [X] Done \n")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [X] Ack'ed. Waiting for the next message. \n")


GrphtQueue.basic_qos(prefetch_count=1)
GrphtQueue.basic_consume(queue='Grpht_Queue', on_message_callback=ProcessMessage)
GrphtQueue.start_consuming()
