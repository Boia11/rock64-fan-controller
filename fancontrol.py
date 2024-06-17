#!/usr/bin/env python3

import time
import R64.GPIO as GPIO

ON_THRESHOLD = 55  #(°C) Fan kicks on at this temperature.
OFF_THRESHOLD = 50  #(°C) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  #[seconds] How often we check the core temperature.
FAN2_INTERVAL_CHECK = 12 #N° of check (6 check x 5 sec = 30 sec)
FAN1_MIN_CYCLE = 12 #N° of check (12 check x 5 sec = 60 sec)

# GPIO PIN is 9 using to control the fan. [Physical PIN 16 on board]

# Set Variables
var_gpio_fan1 = 15              # Pin of Fan 1
var_gpio_fan2 = 16              # Pin of Fan 2

# GPIO Setup
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(var_gpio_fan1, GPIO.OUT, initial=GPIO.LOW)       # Set up GPIO as an output, with an initial state of HIGH
GPIO.setup(var_gpio_fan2, GPIO.OUT, initial=GPIO.LOW)  # Set up GPIO as an input, pullup enabled

def get_temp():
    """Get the core temperature.

    Read file from /sys to get CPU temp in temp in C *1000

    Returns:
        int: The core temperature in thousanths of degrees Celsius.
    """
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temp_str = f.read()

    try:
        return int(temp_str) / 1000
    except (IndexError, ValueError,) as e:
        raise RuntimeError('Could not parse temperature output.') from e

if __name__ == '__main__':
    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    GPIO.output(var_gpio_fan1, GPIO.LOW)             # Turn off Fan1
    GPIO.output(var_gpio_fan2, GPIO.LOW)             # Turn off Fan2
    print("fan 1 e fan 2 off")

    fan2_check = 0

    fan1_cycle_extra_enabled = False
    fan1_cycle_extra = 0

    while True:
        fan1 = GPIO.input(var_gpio_fan1)
        fan2 = GPIO.input(var_gpio_fan2)  
        temp = get_temp()
        print("temp: °C " + str(temp) + " - fan 1: " + str(fan1) + " - fan 2 check: " + str(fan2_check) + " - fan 2: " + str(fan2) + " - fan 1_extra cycle_enable: " + str(fan1_cycle_extra_enabled) + " - fan 1_extra cycle: " + str(fan1_cycle_extra))

        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        # NOTE: `fan` returns 1 for "on" and 0 for "off"
        if temp > ON_THRESHOLD and fan1==0:
            GPIO.output(var_gpio_fan1, GPIO.HIGH)            # Turn on Fan1
            print("fan 1 on")
            fan1_cycle_extra_enabled = True
        # Stop the fan if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        if temp > OFF_THRESHOLD and fan1==1:
            if fan1_cycle_extra != 0:
                fan1_cycle_extra = 0
     
            if temp >= ON_THRESHOLD + 5:  
                if fan2==0:
                    if fan2_check >= FAN2_INTERVAL_CHECK:
                        GPIO.output(var_gpio_fan2, GPIO.HIGH)        # Turn on Fan2
                        print("fan 2 on")
                    else:
                        fan2_check += 1
            else:
                if fan2_check != 0:
                    fan2_check = 0
                    
        if temp <= OFF_THRESHOLD and fan1==1:
            if fan2==1:
                GPIO.output(var_gpio_fan2, GPIO.LOW)             # Turn off Fan1
                print("fan 2 off")
                fan2_check = 0

            if fan1_cycle_extra_enabled==True:
                if fan1_cycle_extra >= FAN1_MIN_CYCLE:
                    GPIO.output(var_gpio_fan1, GPIO.LOW)             # Turn off Fan1
                    print("fan 1 off")
                    fan1_cycle_extra_enabled = False
                    fan1_cycle_extra = 0
                else:
                    fan1_cycle_extra += 1
                    fan2_check = 0

        time.sleep(SLEEP_INTERVAL)