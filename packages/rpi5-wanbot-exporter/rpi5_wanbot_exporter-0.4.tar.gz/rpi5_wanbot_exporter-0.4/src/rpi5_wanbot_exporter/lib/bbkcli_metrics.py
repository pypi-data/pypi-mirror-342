from importlib.resources import files
import sys
import subprocess
from platform import machine


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
            print('ERROR: bbk-cli command not found. Make sure that it is available!')
            return None

        # Search for the pattern in the input text
        try:
            latency, download, upload, measurement_id = stdout.decode().split(" ")
        except Exception:
            print(f"\t bbk-cli - Measurement failed, not data!\n\t\t{stdout.decode()}")
            return None

        return float(latency), float(download), float(upload), measurement_id

    def get_metrics():

        # Start measurement
        measurement = measure()

        # Get last measurement
        if measurement:
            latency, download, upload, measurement_id = measurement
            successful = True
        else:
            latency, download, upload, measurement_id = [None, None, None, None]
            successful = False

        print(f" INFO: bbk-cli Support id: {measurement_id}")

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
           f"--duration={duration}",
           "--quiet"]

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
