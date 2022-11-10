import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import collections


def get_num_packets(df, protocol):
    protocol_packets = 0
    if protocol == "batman":
        protocol_packets = df.loc[df["Protocol"] == "BAT_BATMAN"]
    elif protocol == "olsr":
        protocol_packets = df.loc[df["Protocol"] == "OLSR v1"]
    elif protocol == "batman_adv":
        protocol_packets = df.loc[(df["Protocol"] == "BATADV_IV_OGM") | (df["Protocol"] == "BATADV_UNICAST_TVLV")]
    elif protocol == "olsrv2":
        protocol_packets = df.loc[df["Protocol"] == "packetbb"]

    num_packets = len(protocol_packets.index)
    return num_packets


def calc_average_packets(num_packets):
    total_packets = [val["Total Protocol Packets"] for key, val in num_packets.items()
                     if "Total Protocol Packets" in val]
    avg_packets = (sum(total_packets)) / len(total_packets)
    return avg_packets


def get_data(path, protocol):
    id_test = 1
    data_packet = collections.defaultdict(dict)
    for packet_file in os.listdir(path):
        if packet_file.endswith(".csv"):
            filepath = f"{path}/{packet_file}"
            df = pd.read_csv(filepath)
            data_packet[str(id_test)]["Total Protocol Packets"] = get_num_packets(df, protocol)
            id_test += 1

    avg_packets = calc_average_packets(dict(data_packet))
    return avg_packets


def main(args):
    if len(args) != 2:
        print("Uso: packet_analyzer.py <número de escenario>")
        sys.exit(1)
    escenario = args[1]
    path_batmand = os.path.dirname(os.path.abspath(__file__)) + "/BATMAND/" + escenario
    path_batman_adv = os.path.dirname(os.path.abspath(__file__)) + "/BATMAN_ADV/" + escenario
    path_olsr = os.path.dirname(os.path.abspath(__file__)) + "/OLSR/" + escenario
    path_olsrv2 = os.path.dirname(os.path.abspath(__file__)) + "/OLSRV2/" + escenario

    num_avg_packets_batmand = get_data(path_batmand, "batman")
    num_avg_packets_batman_adv = get_data(path_batman_adv, "batman_adv")
    num_avg_packets_olsr = get_data(path_olsr, "olsr")
    num_avg_packets_olsrv2 = get_data(path_olsrv2, "olsrv2")

    df = pd.DataFrame([num_avg_packets_batmand, num_avg_packets_batman_adv, num_avg_packets_olsr, num_avg_packets_olsrv2],
                      index=['BATMAND', 'BATMAN ADVANCED', 'OLSR', 'OLSR V2'], columns=['Total Packets'])
    np = df.plot.bar(y="Total Packets", color=["lightskyblue", "lightgreen", "turquoise", "palegreen"], rot=0,
                     title="Escenario " + escenario + ": Media de paquetes por protocolo", ylim=(0, 55000), legend=False)
    np.bar_label(np.containers[0])
    plt.savefig(os.path.dirname(os.path.abspath(__file__)) + "/GRAFICAS/" + escenario + "/esc" + escenario + "_paquetes.png")
    plt.show()


if __name__ == '__main__':
    main(sys.argv)
