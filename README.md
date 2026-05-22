# RunningJSSFPrograms

There are two programs in here: MotionDetection is the main program where controlling/using the sensors, motors, and other electronics is done. The other file is a calibration file that'll help calibrate the best ratio for the load sensor. 

Inside the MotionDetection file, it'll first check for motion using the motion detector. Once it detects there is motion, it'll activate the RFID reader for 5 seconds. The reason why we make it run for only 5 seconds is that the RFID takes a good amount of power from the RaspBerryPi4. If it detects an ID, then it'll append the ID to the DataFrame and activate the load sensor. If it does not detect an ID it'll go back to the function that searches for motion. In the load sensor function, it'll get the weight 4 times and average it; if the weight is equal to 0 it'll not count it in the average. It then appends the value to the DataFrame and saves it to a CSV file. Finally, we return to the motion detection function.

# Issues and Technical Problems

## Load Sensor Inaccuracy

Load sensor inaccuracy can be caused by rapid changes in temperature, inconsistent power usage, and the wrong orientation of the amplifier. 

  1. Ensure that the load cell is getting consistent power through the 3.3V port. To do this, use a multimeter and put the positive into the 3.3V port and the neutral in the ground.
  2. Ensure that the temperature is not changing too rapidly
  3. If the amplifier is not flat and vertical, then the readings are more susceptible to error
  4. If it still doesn't work, ensure that the wires are plugged in all the way.
  5. If it STILL doesn't work, you may have to put shields on the wire (e.g. copper tape)

## RFID 

RFID has many wires, and you need to ensure that the wires are plugged into the correct place and all the way. 

## Motion Sensor

The motion sensor usually is pretty accurate, but if it is

