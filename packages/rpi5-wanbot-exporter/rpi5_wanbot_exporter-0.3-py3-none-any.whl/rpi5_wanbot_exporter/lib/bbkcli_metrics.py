from importlib.resources import files
import re
import sys
import subprocess
from platform import machine

# Regular expression to extract metrics from bbk-cli
RE_STATISTIC = r"Support ID:\s+([a-zA-Z0-9]+)\s+Latency:\s+([0-9\.]+)\s+ms\s+Download:\s+([0-9\.]+)\s+Mbit/s\s+Upload:\s+([0-9\.]+)\s+Mbit/s\s+Measurement ID:\s+(\d+)"


def get_bbk_metrics(speedlimit=2, duration=2):
    """
    Wrapper for Bredbandskollen to check outbound and inbound connections speed as well as latency
    :param speedlimit: Maximum average speed limit in [mbps]. For continuous usage this should be significantly lower than your ISP service connection to avoid traffic congestion.
    :param duration: Duration of the test for measurement of upload and download speeds
    """

    def measure():

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(timeout=duration * 3)
        except subprocess.TimeoutExpired:
            process.kill()
            return None
        except OSError:
            print('ERROR: fping command not found. Please install fping on the system!')
            return None

        # Search for the pattern in the input text
        match = re.search(RE_STATISTIC, stdout.decode())

        if match:
            support_id = match.group(1)  # Support ID
            latency = match.group(2)  # Latency value
            download = match.group(3)  # Download value
            upload = match.group(4)  # Upload value
            measurement_id = match.group(5)  # Measurement ID

            return support_id, float(latency), float(download), float(upload), measurement_id

        else:
            print("Measurement failed, not data!")
            return None

    def get_metrics():

        # Start measurement
        measurement = measure()

        # Get last measurement
        if measurement:
            support_id, latency, download, upload, measurement_id = measurement
            successful = True
        else:
            support_id, latency, download, upload, measurement_id = [None, None, None, None, None]
            successful = False

        print(f" INFO: bbk-cli Support id: {support_id}")

        descriptions = dict()
        # descriptions['bbkcli_support_ID'] = {'metric_name': "bbkcli_support_ID",
        #                                      'help_text': "Bedbandkollen Support ID",
        #                                      'unit': None,
        #                                      'metric_type': "gauge",
        #                                      'measurement': support_id,
        #                                      'successful': successful
        #                                      }

        descriptions['bbkcli_latency'] = {'metric_name': "bbkcli_latency",
                                          'help_text': "Bedbandkollen latency",
                                          'unit': "ms",
                                          'metric_type': "gauge",
                                          'measurement': latency,
                                          'successful': successful
                                          }

        descriptions['bbkcli_download_speed'] = {'metric_name': "bbkcli_download_speed",
                                                 'help_text': f"Bedbandkollen download speed - Limit {speedlimit}",
                                                 'unit': "MBits",
                                                 'metric_type': "gauge",
                                                 'measurement': download,
                                                 'successful': successful
                                                 }

        descriptions['bbkcli_upload_speed'] = {'metric_name': "bbkcli_upload_speed",
                                               'help_text': f"Bedbandkollen upload speed - Limit {speedlimit}",
                                               'unit': "MBits",
                                               'metric_type': "gauge",
                                               'measurement': upload,
                                               'successful': successful
                                               }

        descriptions['bbkcli_measurement_ID'] = {'metric_name': "bbkcli_measurement_ID",
                                                 'help_text': "Bedbandkollen measrurement ID",
                                                 'unit': None,
                                                 'metric_type': "gauge",
                                                 'measurement': measurement_id,
                                                 'successful': successful
                                                 }

        return descriptions

    # Get architecture and correct binary file
    architecture = machine()
    if architecture == 'x86_64':
        executable = "bbk_cli_linux_amd64-1.0"
    elif architecture == "aarch64":
        executable = "bbk_cli_linux_aarch64-1.0"
    else:
        sys.exit(f" Unsupported platform: {architecture}")

    # Get location
    bbk_cli_executable = files("rpi5_wanbot_exporter.bin").joinpath(executable)

    # Get command
    cmd = [bbk_cli_executable,
           f"--speedlimit={speedlimit}",
           f"--duration={duration}", ]

    return get_metrics()


if __name__ == "__main__":

    # Set measurement properties
    _speedlimit = 2  # Maximum download and upload speed
    _duration = 2    # Duration of download and upload test respectively

    print(" \n Performing measurement")
    print(f"\n\t Duration:    {_duration} seconds per direction")
    print(f"\n\t Speed limit: {_speedlimit} MBit/S")
    print("\n Please wait...\n")

    for metric_name, values in get_bbk_metrics(duration=_duration, speedlimit=_speedlimit).items():
        for key, value in values.items():
            print(f'\t {key:12s} - {value}')
        print("")

    print("\n Measurement complete\n")
