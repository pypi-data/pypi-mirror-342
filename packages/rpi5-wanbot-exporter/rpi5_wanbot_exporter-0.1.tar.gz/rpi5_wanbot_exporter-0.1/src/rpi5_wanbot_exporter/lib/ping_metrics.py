import re
import subprocess
import pathlib

RE_TARGET = r'(?P<target>[^ ]+)'
RE_XMT_RCV_LOSS = r'(?P<xmt>[0-9]+)\/(?P<rcv>[0-9]+)\/(?P<loss>[0-9.]+)%'
RE_MIN_AVG_MAX = r'(?P<min>[0-9.]+)\/(?P<avg>[0-9.]+)\/(?P<max>[0-9.]+)'

RE_FPING_SUMMARY = (r'^{} +: xmt\/rcv\/%loss = {}, min\/avg\/max = {}$'
                    .format(RE_TARGET, RE_XMT_RCV_LOSS, RE_MIN_AVG_MAX))

RE_FPING_SUMMARY_LOSS = (r'^{} +: xmt\/rcv\/%loss = {}'
                         .format(RE_TARGET, RE_XMT_RCV_LOSS))

if pathlib.Path("/usr/bin/fping").is_file():
    _fping_cmd = "/usr/bin/fping"
elif pathlib.Path("/usr/sbin/fping").is_file():
    _fping_cmd = "/usr/sbin/fping"
else:
    _fping_cmd = ""
    print("ERROR: fping command not found!")


def get_ping_metrics(fping_cmd=_fping_cmd, host="LanBotPi5", target='8.8.8.8'):

    # Assemble command arguments
    cmd = [fping_cmd,
           '--count=3', '--backoff=1.0', '--timestamp', '--retry=0', '--tos=0',
           target
           ]

    # Compile regexp
    re_summary = re.compile(RE_FPING_SUMMARY)
    re_summary_loss = re.compile(RE_FPING_SUMMARY_LOSS)

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        print(' ERROR: fping command timed out!')

        return None
    except OSError:
        print(' ERROR: fping command not found. Please install fping on the system!')
        return None

    match = re_summary.match(stderr.decode().strip())
    match_loss = re_summary_loss.match(stderr.decode().strip())

    stats = dict()
    if match is not None:
        for measurement in ('target', 'min', 'avg', 'max', 'loss'):
            stats[measurement] = match.group(measurement)
        successful = True
    elif match_loss is not None:
        for measurement in ('target', 'xmt', 'rcv', 'loss'):
            stats[measurement] = match_loss.group(measurement)
        successful = False
    else:
        return None

    # Get results
    target = stats["target"]
    if successful:
        ping_avg = stats["avg"]
    else:
        ping_avg = None
    loss = stats["loss"]

    metrics = dict()
    metrics["ping_packet_loss"] = {'metric_name': "ping_packet_loss",
                                   'help_text': f"Percentage of packages lost from {host} to {target}",
                                   'unit': "Percent",
                                   'metric_type': "gauge",
                                   'measurement': loss,
                                   'successful': successful
                                   }

    metrics["ping_average_time"] = {'metric_name': "ping_average_time",
                                    'help_text': f"Average ping time of packages from {host} to {target}",
                                    'unit': "ms",
                                    'metric_type': "gauge",
                                    'measurement': ping_avg,
                                    'successful': successful
                                    }
    return metrics


if __name__ == "__main__":

    # Set measurement properties
    print(" \n Performing measurement")
    print("\n Please wait...\n")

    for metric_name, values in get_ping_metrics().items():
        for key, value in values.items():
            print(f'\t {key:12s} - {value}')
        print("")

    print("\n Measurement complete\n")
