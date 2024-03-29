**Server Setup:**

1. **Clone and Configure `server.py`**: Begin by cloning the `server.py` program to the computer you wish to monitor. Customize the script to include the necessary data you want to transmit over to the client for display.

2. **Enable Automatic Startup**:
   - Open the Task Scheduler by pressing Win + R, typing `taskschd.msc`, and pressing Enter.
   - Create a new task by selecting "Create Task..." from the Actions pane on the right.
   - Provide a name and description for the task in the General tab.
   - Configure the trigger by going to the Triggers tab, clicking "New", and selecting "At startup" from the dropdown menu.
   - Set the action to "Start a program" in the Actions tab, browsing to the location of your Python executable or script file, and adding any necessary arguments.
   - Optionally, configure additional conditions and settings in the corresponding tabs.
   - Save the task by clicking OK.

Now, your Python program will run automatically every time your Windows 10 computer starts up. Test the task to ensure it runs correctly.

**Client Setup:**

1. **Clone and Configure `client.py`**: Clone the code to your Raspberry Pi and configure the GPIO pins as needed. Install any necessary dependencies and customize the code to display the desired information. Ensure to update the IP address of the server stored in the `addr` variable.

2. **Automate Client Startup with Cron**:
   - Open the Crontab editor in the terminal by running:
     ```bash
     sudo crontab -e
     ```
   - Scroll to the bottom of the Crontab file and add the following line:
     ```bash
     @reboot python /home/pi/client.py &
     ```
     This line instructs Cron to execute the `client.py` script using Python upon system boot, running it in the background without interrupting the boot process.
   - Save the changes and exit the Crontab editor as instructed.

![Client Setup Image](https://github.com/LSuds/AnalogMeterProject/assets/46835310/0410d6fa-2098-439e-9ccc-f05c09e41ed2)
