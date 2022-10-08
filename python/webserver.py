from flask import Flask

try:
    from ltr559 import LTR559

    ltr559 = LTR559()
except ImportError:
    import ltr559
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

from enviroplus import gas
from bme280 import BME280
from subprocess import PIPE, Popen

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)


def get_cpu_temp():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    output = output.decode()
    return float(output[output.index('=') + 1:output.rindex("'")])


def get_temp():
    # adjust factor for better results, higher factor to increase temp
    factor = 0.7
    raw_temp = bme280.get_temperature()
    cpu_temp = get_cpu_temp()
    calc_temp = cpu_temp - (cpu_temp - raw_temp) / factor
    # convert to F
    calc_temp = (calc_temp * 1.8) + 32
    return calc_temp


app = Flask(__name__)


@app.route("/")
def main():
    # 'oxidising', 'reducing', 'nh3', 'adc'
    # oxidising: chlorine, nitrous oxide
    # reducing: hydrogen, carbon monoxide
    # nh3: ammonia
    # adc: spare ADC channel value
    gas_data = gas.read_all()
    pressure = bme280.get_pressure()
    light = ltr559.get_lux()
    humidity = bme280.get_humidity()
    temp = get_temp()

    return {'temperature': temp,
            'gas': {'oxidising': gas_data.oxidising, 'reducing': gas_data.reducing, 'nh3': gas_data.nh3,
                    'adc': gas_data.adc},
            'pressure': pressure, 'humidity': humidity, 'light': light}
