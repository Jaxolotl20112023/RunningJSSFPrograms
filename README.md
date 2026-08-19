# RunningJSSFPrograms

The main program file that is being used is the ClassMotionDetection.py. This file is similar to the MotionDetection.py files, but manages each new electronic device as a class. This allows easier integration of new devices and overall makes the code cleaner and easier to read. Another file that will be used is the start_up.py. This file is going to be run before the ClassMotionDetection to set certain properties about the feeder itself like id, location, etc.

Inside the MotionDetection file, it'll first check for motion using the motion detector. Once it detects there is motion, it'll activate the RFID reader for 5 seconds. The reason why we make it run for only 5 seconds is that the RFID takes a good amount of power from the RaspBerryPi4. If it detects an ID, then it'll append the ID to the DataFrame and activate the load sensor. If it does not detect an ID it'll go back to the function that searches for motion. In the load sensor function, it'll get the weight 4 times and average it; if the weight is equal to 0 it'll not count it in the average. It then appends the value to the DataFrame and saves it to a CSV file. Finally, we return to the motion detection function.

# Issues and Technical Problems

## Load Sensor Inaccuracy

Load sensor inaccuracy can be caused by rapid changes in temperature, inconsistent power usage, and the wrong orientation of the amplifier. 

  1. Ensure that the load cell is getting consistent power through the 3.3V port. To do this, use a multimeter and put the positive into the 3.3V port and the neutral in the ground. If you can't, use this command in the terminal: vcgencmd get_throttled. Anything not 0x0 means there are power fluctuations in the pi.
  2. Ensure that the temperature is not changing too rapidly
  3. If the amplifier is not flat and vertical, then the readings are more susceptible to error
  4. If it still doesn't work, ensure that the wires are plugged in all the way.
  5. If it STILL doesn't work, you may have to put shields on the wire (e.g. copper tape)

## RFID 

RFID has many wires, and you need to ensure that the wires are plugged into the correct place and all the way. 

## Motion Sensor

The motion sensor is usually pretty accurate, but if it is not working, then it is most likely that the wires have become loose. Ensure that the wires are plugged in all the way. If that does not work, you may have to get a new motion sensor. 

## Servo

The servo is also prone to changes in the power, meaning that the power must be consistent (usually want to have a resistor to regulate and keep the power consistent). This can cause drifting or jittering of the servo. 

  1. To check it put the positive into the 5v port and the neutral into the ground. 
