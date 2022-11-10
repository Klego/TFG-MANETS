from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.replaying import ReplayingMobility
from mn_wifi.wmediumdConnector import interference
import sys
import os
import warnings


def topology(args):
    warnings.filterwarnings("ignore")
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
    info("*** Creating nodes\n")
    kwargs = {}
    sta1 = net.addStation('sta1', ip='10.10.0.1/24', position='25,250,0', mac='02:00:00:00:65:01', **kwargs)
    sta2 = net.addStation('sta2', ip='10.10.0.2/24', position='75,250,0', mac='02:00:00:00:65:02', **kwargs)
    sta3 = net.addStation('sta3', ip='10.10.0.3/24', position='125,250,0', mac='02:00:00:00:65:03', **kwargs)
    sta4 = net.addStation('sta4', ip='10.10.0.4/24', position='175,250,0', mac='02:00:00:00:65:04', **kwargs)
    sta5 = net.addStation('sta5', ip='10.10.0.5/24', position='225,250,0', mac='02:00:00:00:65:05', **kwargs)
    sta6 = net.addStation('sta6', ip='10.10.0.6/24', position='275,250,0', mac='02:00:00:00:65:06', **kwargs)
    sta7 = net.addStation('sta7', ip='10.10.0.7/24', position='325,250,0', mac='02:00:00:00:65:07', **kwargs)
    sta8 = net.addStation('sta8', ip='10.10.0.8/24', position='375,250,0', mac='02:00:00:00:65:08', **kwargs)
    sta9 = net.addStation('sta9', ip='10.10.0.9/24', position='425, 250, 0', mac='02:00:00:00:65:09', **kwargs)
    sta10 = net.addStation('sta10', ip='10.10.0.10/24', mac='02:00:00:00:65:10', **kwargs)
    net.setPropagationModel(model="logDistance", exp=4)
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")

    protocols = ['batman_adv', 'olsrd', 'olsrd2']

    for proto in args:
        if proto in protocols:
            kwargs['proto'] = proto
    if 'proto' not in kwargs:
        info("*INFO: Not protocol selected*\n")

    net.addLink(sta1, cls=adhoc, intf='sta1-wlan0',
                ssid='adhocNet', mode='g', channel=5, **kwargs)
    net.addLink(sta2, cls=adhoc, intf='sta2-wlan0',
                ssid='adhocNet', mode='g', channel=5, **kwargs)
    net.addLink(sta3, cls=adhoc, intf='sta3-wlan0',
                ssid='adhocNet', mode='g', channel=5, **kwargs)
    net.addLink(sta4, cls=adhoc, intf='sta4-wlan0',
                ssid='adhocNet', mode='g', channel=5, **kwargs)
    net.addLink(sta5, cls=adhoc, intf='sta5-wlan0',
                ssid='adhocNet', mode='g', channel=5, **kwargs)
    net.addLink(sta6, cls=adhoc, intf='sta6-wlan0',
                ssid='adhocNet', mode='g', channel=5, **kwargs)
    net.addLink(sta7, cls=adhoc, intf='sta7-wlan0',
                ssid='adhocNet', mode='g', channel=5, **kwargs)
    net.addLink(sta8, cls=adhoc, intf='sta8-wlan0',
                ssid='adhocNet', mode='g', channel=5, **kwargs)
    net.addLink(sta9, cls=adhoc, intf='sta9-wlan0',
                ssid='adhocNet', mode='g', channel=5, **kwargs)
    net.addLink(sta10, cls=adhoc, intf='sta10-wlan0',
                ssid='adhocNet', mode='g', channel=5, **kwargs)

    net.isReplaying = True
    path = os.path.dirname(os.path.abspath(__file__)) + '/replayingMobility/escenario2/'
    get_trace(sta10, '{}node.dat'.format(path), 10)

    if '-p' in args:
        net.plotGraph(max_x=500, max_y=500)

    info("*** Starting network\n")
    net.build()

    info("\n*** Replaying Mobility\n")
    ReplayingMobility(net)

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


def get_trace(sta, file_, numeral):
    file_ = open(file_, 'r')
    raw_data = file_.readlines()
    file_.close()

    sta.p = []
    sta.time = []
    if numeral == 10:
        pos = (25, 200, 0)
        tim = 30
    elif numeral == 1:
        pos = (25, 250, 0)
        tim = 30
    else:
        pos = (0, 0, 0)
        tim = 30
    sta.position = pos
    sta.time.append(tim)
    for data in raw_data:
        line = data.split()
        x = line[0]  # First Column
        y = line[1]  # Second Column
        t = line[2]  # Third column
        pos = float(x), float(y), 0.0
        tim = float(t)
        sta.p.append(pos)
        sta.time.append(tim)


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
