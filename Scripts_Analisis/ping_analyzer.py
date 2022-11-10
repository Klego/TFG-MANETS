import sys
import matplotlib.pyplot as plt
import os
import ping_parser as pp
import collections
import pandas as pd


def get_data(path):
    id_prueba = 1
    data_protocol = collections.defaultdict(dict)
    for file in os.listdir(path):
        if file.endswith(".txt"):
            filepath = f"{path}/{file}"
            pp.clean(filepath)
            data_read = pp.read_file(filepath)
            data = pp.ping_parse(data_read)
            data_protocol[str(id_prueba)]["total_time"] = data[0]
            data_protocol[str(id_prueba)]["average_time"] = data[1]
            data_protocol[str(id_prueba)]["min_time"] = data[2]
            data_protocol[str(id_prueba)]["max_time"] = data[3]
            id_prueba += 1
    return dict(data_protocol)


def get_time_values(data_protocol):
    final_values = []
    total_time = [val["total_time"] for key, val in data_protocol.items() if "total_time" in val]
    avg_total = (sum(total_time)) / len(total_time)
    final_values.append(float("{:.2f}".format(avg_total)))
    avg_time = [val["average_time"] for key, val in data_protocol.items() if "average_time" in val]
    avg_avg = (sum(avg_time)) / len(avg_time)
    final_values.append(float("{:.2f}".format(avg_avg)))
    min_time = [val["min_time"] for key, val in data_protocol.items() if "min_time" in val]
    avg_min = (sum(min_time)) / len(min_time)
    final_values.append(float("{:.2f}".format(avg_min)))
    max_time = [val["max_time"] for key, val in data_protocol.items() if "max_time" in val]
    avg_max = (sum(max_time)) / len(min_time)
    final_values.append(float("{:.2f}".format(avg_max)))

    return final_values


def main(args):
    if len(args) != 2:
        print("Uso: ping_analyzer.py <número de escenario>")
        sys.exit(1)
    escenario = args[1]

    path_batmand = os.path.dirname(os.path.abspath(__file__)) + "/BATMAND/" + escenario
    path_batman_adv = os.path.dirname(os.path.abspath(__file__)) + "/BATMAN_ADV/" + escenario
    path_olsr = os.path.dirname(os.path.abspath(__file__)) + "/OLSR/" + escenario
    path_olsr2 = os.path.dirname(os.path.abspath(__file__)) + "/OLSRV2/" + escenario

    data_batmand = get_data(path_batmand)
    final_values_batmand = get_time_values(data_batmand)
    # print(final_values_batmand)
    data_batman_adv = get_data(path_batman_adv)
    final_values_batman_adv = get_time_values(data_batman_adv)
    # print(final_values_batman_adv)
    data_olsr = get_data(path_olsr)
    final_values_olsr = get_time_values(data_olsr)
    # print(final_values_olsr)
    data_olsr2 = get_data(path_olsr2)
    final_values_olsr2 = get_time_values(data_olsr2)

    df = pd.DataFrame([final_values_batmand, final_values_batman_adv, final_values_olsr, final_values_olsr2],
                      index=['BATMAND', 'BATMAN ADVANCED', 'OLSR', 'OLSR V2'], columns=['Total Time Disconnected',
                                                                                        'Average Time Disconnected',
                                                                                        'Min Time Disconnected',
                                                                                        'Max Time Disconnected'])

    tt = df.plot.bar(y='Total Time Disconnected', color=["lightskyblue", "lightgreen", "turquoise", "palegreen"], rot=0,
                     title="Escenario " + escenario + ": Tiempo Total de Desconexión", ylim=(0, 160), legend=False)
    tt.bar_label(tt.containers[0])
    plt.savefig(os.path.dirname(os.path.abspath(__file__)) + "/GRAFICAS/" + escenario + "/esc" + escenario + "_tiempo_total.png")

    at = df.plot.bar(y='Average Time Disconnected', color=["lightskyblue", "lightgreen", "turquoise", "palegreen"],
                     rot=0, title="Escenario " + escenario + ": Tiempo Medio de Desconexión", ylim=(0, 160), legend=False)
    at.bar_label(at.containers[0])
    plt.savefig(
        os.path.dirname(os.path.abspath(__file__)) + "/GRAFICAS/" + escenario + "/esc" + escenario + "_tiempo_medio.png")

    mt = df.plot.bar(y='Min Time Disconnected', color=["lightskyblue", "lightgreen", "turquoise", "palegreen"], rot=0,
                     title="Escenario " + escenario + ": Tiempo Mínimo de Desconexión", ylim=(0, 160), legend=False)
    mt.bar_label(mt.containers[0])
    plt.savefig(
        os.path.dirname(os.path.abspath(__file__)) + "/GRAFICAS/" + escenario + "/esc" + escenario + "_tiempo_minimo.png")

    maxt = df.plot.bar(y='Max Time Disconnected', color=["lightskyblue", "lightgreen", "turquoise", "palegreen"], rot=0,
                       title="Escenario " + escenario + ": Tiempo Máximo de Desconexión", ylim=(0, 160), legend=False)
    maxt.bar_label(maxt.containers[0])
    plt.savefig(
        os.path.dirname(os.path.abspath(__file__)) + "/GRAFICAS/" + escenario + "/esc" + escenario + "_tiempo_maximo.png")

    allt = df.plot.bar(rot=0, colormap='Accent', ylim=(0, 160), title="Escenario " + escenario + ": Tiempos de Desconexión")

    for container in allt.containers:
        allt.bar_label(container)
    plt.savefig(
        os.path.dirname(os.path.abspath(__file__)) + "/GRAFICAS/" + escenario + "/esc" + escenario + "_tiempos_desconexion.png")
    plt.show()


if __name__ == '__main__':
    main(sys.argv)
