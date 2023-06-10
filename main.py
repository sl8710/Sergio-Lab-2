import machine
import time
from machine import I2C, Pin

class TrafficLight:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green

    def operate_normal_lights(self, delay):
        self.green.on()
        self.yellow.off()
        self.red.off()
        time.sleep(delay)
        
        self.green.off()
        self.yellow.on()
        time.sleep(delay)
        
        self.yellow.off()
        self.red.on()
        time.sleep(delay)

    def operate_pedestrian_crossing(self):
        self.red.on()
        time.sleep(2)
        self.yellow.on()
        time.sleep(1)
        self.green.on()
        time.sleep(3)


class PIRSensor:
    def __init__(self, pin):
        self.sensor = machine.Pin(pin, machine.Pin.IN)

    def is_motion_detected(self):
        return self.sensor.value()


class LCD:
    # Dummy class for illustration
    def __init__(self, i2c):
        pass

    def display_string(self, message, line):
        # Add code to display the message on the given line
        pass


class TwoWayTrafficLightSystem:
    def __init__(self, traffic_lights, pedestrian_buttons, pir_sensor, lcd_displays):
        self.traffic_light_system_1 = TrafficLight(*traffic_lights[0])
        self.traffic_light_system_2 = TrafficLight(*traffic_lights[1])
        self.pedestrian_buttons = pedestrian_buttons
        self.pir_sensor = pir_sensor
        self.lcd_displays = lcd_displays
        print("Two-way traffic light system initialized.")

    def operate(self, delay=10):
        while True:
            if self.pir_sensor.is_motion_detected():
                self.lcd_displays[0].display_string("Pedestrian Detected", 1)
                self.lcd_displays[1].display_string("Pedestrian Detected", 1)
                self.traffic_light_system_1.operate_pedestrian_crossing()
                self.traffic_light_system_2.operate_pedestrian_crossing()
                self.lcd_displays[0].display_string(" "*16, 1)
                self.lcd_displays[1].display_string(" "*16, 1)
            else:
                self.traffic_light_system_1.operate_normal_lights(delay)
                self.traffic_light_system_2.operate_normal_lights(delay)


# Initialize I2C for LCDs
i2c = I2C(scl=Pin(22), sda=Pin(21))

# Initialize LCD displays
lcd_1 = LCD(i2c)
lcd_2 = LCD(i2c)

# Initialize PIR sensor
pir_sensor = PIRSensor(pin=9)

# Traffic lights sets (red, yellow, green)
lights_1 = (machine.Pin(1, machine.Pin.OUT), machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT))
lights_2 = (machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT), machine.Pin(6, machine.Pin.OUT))

# Pedestrian buttons
pedestrian_buttons = [machine.Pin(7, machine.Pin.IN), machine.Pin(8, machine.Pin.IN)]

# Initialize the traffic light system
traffic_light_system = TwoWayTrafficLightSystem([lights_1, lights_2], pedestrian_buttons, pir_sensor, [lcd_1, lcd_2])

# Start operating the traffic light system
traffic_light_system.operate()
