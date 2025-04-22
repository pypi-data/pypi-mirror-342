import glob
import pathlib
import psutil
import os

if os.getenv("DOCKER"):
    print(" Docker mode detected")
    FAN_SPEED_PATH_BASE = pathlib.Path('/sensors/hwmon')
    CPU_TEMP_PATH = pathlib.Path('/sensors/temp')
else:
    FAN_SPEED_PATH_BASE = pathlib.Path('/sys/devices/platform/cooling_fan/hwmon/')
    CPU_TEMP_PATH = pathlib.Path('/sys/class/thermal/thermal_zone0/temp')

pattern = os.path.join(FAN_SPEED_PATH_BASE, 'hwmon*/fan1_input')
matches = glob.glob(pattern)

if matches:
    FAN_SPEED_PATH = pathlib.Path(matches[0])  # Return first match
else:
    print("ERROR: The location of the fan speed file fan1_input could not be found!")
    FAN_SPEED_PATH = False


# Get fan speed (supports official RPi5 Active Cooler)
def get_pi5_fan_speed():
    metric_name = "rpi5_fan_speed"
    help_text = "Fan speed in RPM"
    unit = "rpm"
    metric_type = "gauge"
    try:
        if FAN_SPEED_PATH:
            with open(FAN_SPEED_PATH, "r") as file:
                speed = int(file.read().strip())
            successful = True
        else:
            raise FileNotFoundError("Fan path could not be located")
    except Exception as e:
        print(f"\n\tERROR: collecting fan speed:\n\t{e}")
        speed = None
        successful = False

    metric = dict()
    metric[metric_name] = {'metric_name': metric_name,
                           'help_text': help_text,
                           'unit': unit,
                           'metric_type': metric_type,
                           'measurement': speed,
                           'successful': successful
                           }
    return metric


def get_pi5_cpu_temperature():
    metric_name = "rpi5_cpu_temperature"
    help_text = "Raspberry Pi 5 core temperature"
    unit = "Celsius"
    metric_type = "gauge"

    try:
        with open(CPU_TEMP_PATH, 'r') as f:
            # The temperature is in millidegrees Celsius, so we divide by 1000
            cpu_temp = float(f.read()) / 1000
        successful = True
    except FileNotFoundError as e:
        # CPU temperature file is not found
        print(f"\n\tERROR: collecting CPU temperature:\n\t{e}")
        cpu_temp = None
        successful = False

    metric = dict()
    metric[metric_name] = {'metric_name': metric_name,
                           'help_text': help_text,
                           'unit': unit,
                           'metric_type': metric_type,
                           'measurement': cpu_temp,
                           'successful': successful
                           }
    return metric


def get_memory_utilization():
    metric_name = "system_memory_utilization"
    help_text = "Current system memory utilization"
    unit = "percent"
    metric_type = "gauge"

    # Using psutil to get memory usage information
    memory = psutil.virtual_memory()
    memory_usage = memory.percent  # Memory usage as a percentage

    metric = dict()
    metric[metric_name] = {'metric_name': metric_name,
                           'help_text': help_text,
                           'unit': unit,
                           'metric_type': metric_type,
                           'measurement': memory_usage,
                           'successful': True
                           }
    return metric


def get_memory_free():
    metric_name = "system_memory_free"
    help_text = "Current system memory free"
    unit = "GB"
    metric_type = "gauge"

    # Using psutil to get memory usage information
    memory = psutil.virtual_memory()
    memory_free = memory.available / (1024 ** 3)  # Free memory in GB

    metric = dict()
    metric[metric_name] = {'metric_name': metric_name,
                           'help_text': help_text,
                           'unit': unit,
                           'metric_type': metric_type,
                           'measurement': memory_free,
                           'successful': True
                           }
    return metric


def get_memory_total():
    metric_name = "system_memory_free"
    help_text = "Current system memory free"
    unit = "GB"
    metric_type = "gauge"

    # Using psutil to get memory usage information
    memory = psutil.virtual_memory()
    memory_total = memory.total / (1024 ** 3)  # Total memory in GB

    metric = dict()
    metric[metric_name] = {'metric_name': metric_name,
                           'help_text': help_text,
                           'unit': unit,
                           'metric_type': metric_type,
                           'measurement': memory_total,
                           'successful': True
                           }
    return metric


def get_disk_free_space():
    metric_name = "system_disk_free_space"
    help_text = "Disk space free on system"
    unit = "GB"
    metric_type = "gauge"

    # Using os and shutil to get free disk space
    disk = psutil.disk_usage('/')
    disk_free = disk.free / (1024 ** 3)  # Free disk space in GB

    metric = dict()
    metric[metric_name] = {'metric_name': metric_name,
                           'help_text': help_text,
                           'unit': unit,
                           'metric_type': metric_type,
                           'measurement': disk_free,
                           'successful': True
                           }
    return metric


def get_disk_total_space():
    metric_name = "system_disk_total_space"
    help_text = "Disk space total on system"
    unit = "GB"
    metric_type = "gauge"

    # Using os and shutil to get free disk space
    disk = psutil.disk_usage('/')
    disk_total = disk.total / (1024 ** 3)  # Total disk space in GB

    metric = dict()
    metric[metric_name] = {'metric_name': metric_name,
                           'help_text': help_text,
                           'unit': unit,
                           'metric_type': metric_type,
                           'measurement': disk_total,
                           'successful': True
                           }
    return metric
