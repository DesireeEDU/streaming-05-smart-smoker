Smart Smoker System
Overview
The Smart Smoker system is designed to monitor temperature readings from a smoker and two food compartments, named Food A and Food B. The system detects anomalies in temperature changes and generates alerts when necessary.

Author
Denise Case
Date: January 15, 2023
Requirements
RabbitMQ server running
pika installed in your active environment
Access to RabbitMQ Admin interface (http://localhost:15672/)
How it Works
The system reads temperature values every half minute and stores them in a CSV file named smoker-temps.csv.
There are three listening queues:
01-smoker: Queue for smoker temperature readings
02-food-A: Queue for Food A temperature readings
03-food-B: Queue for Food B temperature readings
The system monitors the following conditions:
Smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert)
Any food temperature changes less than 1 degree F in 10 minutes (food stall alert)
Time Windows:
Smoker time window: 2.5 minutes
Food time window: 10 minutes
Deque Max Length:
Smoker deque max length: 5 (2.5 min _ 1 reading / 0.5 min)
Food deque max length: 20 (10 min _ 1 reading / 0.5 min)
Consumer Implementation
Three callback functions are implemented to handle messages from each queue: smoker_callback, foodA_callback, and foodB_callback.
Each callback function processes the received message, extracts the timestamp and temperature, and stores them in a deque with a specific maximum length.
If the conditions for generating alerts are met, the system logs the appropriate alert message.
The main function sets up connections to the RabbitMQ server, declares the listening queues, and starts consuming messages from each queue.
How to Run
Open your existing project in your preferred IDE (e.g., VS Code).
Ensure RabbitMQ server is running.
Install the pika library in your active environment.
Run the consumer script using the following command:
bash
Copy code
python consumer.py
To exit, press CTRL+C.
Screenshots
Console Output
Screenshot of the console showing the producer and consumer processes running simultaneously.
Visible smoker alert with timestamp.
Visible Food A stall with timestamp.
Visible Food B stall with timestamp.
RabbitMQ Console
Screenshot of the RabbitMQ Admin interface showing the queues and message flow.
