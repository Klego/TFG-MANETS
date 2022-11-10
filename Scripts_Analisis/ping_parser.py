import re


def clean(file):
    with open(file) as f:
        lines = f.readlines()
    with open(file+"_cleaned", 'w') as write_f:
        for line in lines:
            if "Destination Host Unreachable" not in line or "Time to live exceeded" not in line:
                write_f.write(line)
    write_f.close()
    f.close()


def read_file(file):
    with open(file+"_cleaned") as f:
        data = f.read()
    return data


def ping_parse(data):
    aux = 0
    time = []
    total_t = 0
    elapsed_time = 4
    icmp_seq = re.findall(r'icmp_seq=(\d+).*?', data)

    for seq in icmp_seq:
        if aux + elapsed_time < int(seq):
            connect_time = int(seq) - aux
            time.append(connect_time)
            aux = int(seq)
        else:
            aux += 1
    for t in time:
        total_t += t
    avg_t = float("{:.2f}".format(total_t/len(time)))
    min_t = min(time)
    max_t = max(time)
    returned_values = [total_t, avg_t, min_t, max_t]
    return returned_values
