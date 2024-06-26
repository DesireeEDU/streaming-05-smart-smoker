# streaming-05-smart-smoker

**Project Title: Smart BBQ Monitoring System**

**Description:**
The Smart BBQ Monitoring System is a software solution designed to monitor and manage temperature data from various sensors installed in a barbecue setup. This system aims to provide real-time monitoring of smoker and food temperatures, facilitating better control over the cooking process.

**Features:**

- Reads temperature data from a CSV file every 30 seconds.
- Sends temperature data to RabbitMQ queues for further processing.
- Utilizes RabbitMQ for message queuing and distribution.
- Offers an option to monitor RabbitMQ queues via the RabbitMQ Admin interface.
- Logs temperature data and system events using a custom logging module.

**Usage:**

1. Install RabbitMQ: Ensure that RabbitMQ is installed and running on your system. You can download RabbitMQ from the official website: https://www.rabbitmq.com/download.html

2. Install Dependencies: Make sure to install the required dependencies listed in the `requirements.txt` file. You can install them using pip:

   ```
   pip install -r requirements.txt
   ```

3. Run the Program:

   - Update the `smoker-temps.csv` file with temperature data.
   - Run the `bbq_monitoring.py` script to start monitoring the BBQ system:

     ```
     python bbq_monitoring.py
     ```

   ![Console Screenshot](https://github.com/DesireeEDU/streaming-05-smart-smoker/blob/main/console_screenshot.png)

4. Monitor RabbitMQ Queues:

   - When prompted, you can choose to monitor RabbitMQ queues by typing `y`.
   - This will open the RabbitMQ Admin interface in your default web browser.

   \*Note:

   - The program will prompt you to monitor RabbitMQ queues. This prompt is controlled by the `show_offer` parameter in the `offer_rabbitmq_admin_site` function.
   - By default, `show_offer` is set to `True`, meaning you will be asked if you want to monitor the queues. You can change this behavior by setting `show_offer` to `False` when calling the function.

5. Consumer Implementation:

   - Three callback functions are implemented to handle messages from each queue: `smoker_callback`, `foodA_callback`, and `foodB_callback`.
   - Each callback function processes the received message, extracts the timestamp and temperature, and stores them in a deque with a specific maximum length.
   - If the conditions for generating alerts are met, the system logs the appropriate alert message.
   - The main function sets up connections to the RabbitMQ server, declares the listening queues, and starts consuming messages from each queue.

   Conditions:

   - Smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert)
   - Any food temperature changes less than 1 degree F in 10 minutes (food stall alert)

**File Structure:**

- `bbq_monitoring.py`: Main script to read temperature data from CSV, send messages to RabbitMQ, and log events.
- `consumer.py`: Recieves messages from Rabbit MQ
- `util_logger.py`: Utility module for setting up logging functionality.
- `smoker-temps.csv`: Sample CSV file containing temperature data.
- `requirements.txt`: File listing the dependencies required by the project.
- `bbq_montoring.log`: Timestamped log of messages
- `bbq_monitoring_log_screenshot.png`
- `console screenshot`
- `smoker alert screenshot`
- `FoodA alert screenshot`
- `FoodB alert screenshot`
- `RabbitMQ screenshot`

**Customization:**

- You can customize the CSV file (`smoker-temps.csv`) with your temperature data.
- Modify the RabbitMQ connection parameters (`host`, `queues`) in the `bbq_monitoring.py` script as per your setup.
- Customize the logging settings in the `util_logger.py` module to suit your requirements.

**Note:**

- Ensure RabbitMQ is properly configured and running before executing the program.
- The system may require appropriate permissions to access RabbitMQ queues and other resources.

**Author:**
Desiree Thompson

**Date:**
05/29/2024

**Acknowledgments:**

- The project utilizes ChatGPT, an AI language model developed by OpenAI, for assistance in writing the README and providing guidance on software engineering practices.
