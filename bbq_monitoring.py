"""
This program reads temperature data from a CSV file and sends the temperature
data to RabbitMQ queues for further processing

Author: Desiree Thompson
Date: May 29, 2024
"""

import pika
import sys
import webbrowser
import csv
from datetime import datetime
import time

from util_logger import setup_logger
logger, logname = setup_logger(__file__)

def offer_rabbitmq_admin_site(show_offer: bool = True):
    """Offer to open the RabbitMQ Admin website"""
    if not show_offer: 
        print("RabbitMQ Admin connection has been turned off.")
        return
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def rabbitmq_connection(host: str, queues: list):
    """
    Establishes a connection to the RabbitMQ server and declares queues.
    Parameters:
    host (str): the host name or IP address of the RabbitMQ server
    queues (list): list of queue names
    Returns:
    conn: the RabbitMQ connection object
    ch: the RabbitMQ channel object
    """
    try:
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        channel = connection.channel()
        # declare new durable queues
        for queue_name in queues:
            channel.queue_declare(queue=queue_name, durable=True)
        return connection, channel
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)

def send_message(channel, timestamp: str, temperature: float, queue_name: str):
    """Send a message to RabbitMQ"""
    try:
        # create a message string
        message = f"{timestamp}, {temperature}"
    
        # publish the message to the queue
        channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        logger.info(f"[X] Sent message to queue {queue_name}: {message}")
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Error: Failed to send message: {e}")

def read_tasks(file_path: str, host: str, queues: list):
    """Read messages from a CSV file and send them to RabbitMQ"""
    connection, channel = None, None
    try:
        connection, channel = rabbitmq_connection(host, queues)
        with open(file_path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader)  # Skip header row
            for row in reader:
                timestamp = row[0]
                smoker_temp = row[1]
                food_a_temp = row[2]
                food_b_temp = row[3]
                if smoker_temp:
                    send_message(channel, timestamp, smoker_temp, "01-smoker")
                if food_a_temp:
                    send_message(channel, timestamp, food_a_temp, "02-food-A")
                if food_b_temp:
                    send_message(channel, timestamp, food_b_temp, "03-food-B")
                #time.sleep(30)  # Sleep to simulate time intervals between messages
    except Exception as e:
        logger.error(f"Error reading tasks: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()

# Standard Python idiom to indicate main program entry point
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    offer_rabbitmq_admin_site(show_offer=True)
    # create variables   
    file_name = 'smoker-temps.csv'
    host = "localhost"
    queues = ["01-smoker", "02-food-A", "03-food-B"]
    # send messages to the queue
    read_tasks(file_name, host, queues)
