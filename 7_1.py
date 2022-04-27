import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np
import time

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

def to_list_of_bits(num):
    return [(num >> i) & 1 for i in range(num.bit_length() - 1, -1, -1)]
	
	
def clip_to_zero(num):
    return 0 if num < 0 else num
	
	
def extend_array(array, desired_size):
    return [0] * clip_to_zero(desired_size - len(array)) + array
	
	
def extended_list_of_bits(num, desired_size = len(dac)):
    return extend_array(to_list_of_bits(num), desired_size)


def from_binary(bits):
    number = 0
    
    for bit in bits:
        number *= 2
        number += bit
    return number


def adc():
    size_in_bits = 8
    current_bits = [0] * size_in_bits
    
    for i in range(size_in_bits):
        current_bits[i] = 1
        GPIO.output(dac, current_bits)
	
        time.sleep(0.05)
        
        if GPIO.input(comp) == GPIO.LOW:
            current_bits[i] = 0
	    
    return from_binary(current_bits)



def plot_voltages (voltages, filename=None):
    fig = plt.figure (figsize=(15, 18))
    plt.plot (voltages)

    if filename is not None:
        plt.savefig (filename)

    plt.show()


def save_data (voltages, exp_time, period, freq, step):
    with open ("data.txt", "w") as file:
        str_volts = list(map(lambda x: str(x), voltages))
        file.write ("\n".join(str_volts))
    
    with open("settings.txt", "w") as file:
        file.write(f"Total time: {exp_time}")
        file.write(f"Period of one measure: {period}")
        file.write(f"Frequency: {freq}")
        file.write(f"Step: {step}")

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(leds, GPIO.OUT)
    GPIO.setup(dac, GPIO.OUT)
    GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(comp, GPIO.IN)

    voltage_values = list()

    try:
        time_start = time.time()
        GPIO.output(troyka, GPIO.HIGH)

        voltage = 0

        while voltage / 3.3 <= 0.92:
            bit_num = adc()
            voltage = bit_num * 3.3 / 256
            print (voltage)

            voltage_values.append (voltage)

        print ("LOWERING!")
        GPIO.output(troyka, GPIO.LOW)

        while voltage / 3.3 >= 0.07:
            bit_num = adc()
            voltage = bit_num * 3.3 / 256
            print (voltage)

            voltage_values.append (voltage)

        time_end = time.time()
        experiment_time = time_end - time_start
        plot_voltages(voltage_values, "plot-voltages.png")

        save_data (voltage_values, experiment_time, experiment_time / 2, experiment_time / len(voltage_values), 3.3 / 256)
        

    except KeyboardInterrupt:
        print("Finished!")        
            
    finally:
        GPIO.output(dac, 0)
        GPIO.cleanup()