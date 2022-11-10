#!/usr/bin/env python

"""
This example shows on how to enable the adhoc mode
Alternatively, you can use the manet routing protocol of your choice
"""

import sys

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology(args):
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    kwargs = {}
    if '-a' in args:
        kwargs['range'] = 100

    sta1 = net.addStation('sta1', ip='10.10.0.1/8',
                          position='10,10,0', mac='02:00:00:00:65:01', **kwargs)
    sta2 = net.addStation('sta2', ip='10.10.0.2/8',
                          position='75,10,0', mac='02:00:00:00:65:02', **kwargs)
    sta3 = net.addStation('sta3', ip='10.10.0.3/8',
                          position='140,10,0', mac='02:00:00:00:65:03', **kwargs)
    sta4 = net.addStation('sta4', ip='10.10.0.4/8',
                          position='205,10,0', mac='02:00:00:00:65:04', **kwargs)
    sta5 = net.addStation('sta5', ip='10.10.0.5/8',
                          position='10,75,0', mac='02:00:00:00:65:05', **kwargs)
    sta6 = net.addStation('sta6', ip='10.10.0.6/8',
                          position='75,75,0', mac='02:00:00:00:65:06', **kwargs)
    sta7 = net.addStation('sta7', ip='10.10.0.7/8',
                          position='140,75,0', mac='02:00:00:00:65:07', **kwargs)
    sta8 = net.addStation('sta8', ip='10.10.0.8/8',
                          position='205,75,0', mac='02:00:00:00:65:08', **kwargs)
    sta9 = net.addStation('sta9', ip='10.10.0.9/8',
                          position='250, 10, 0', mac='02:00:00:00:65:09', **kwargs)
    sta10 = net.addStation('sta10', ip='10.10.0.10/8',
                           position='250, 75, 0', mac='02:00:00:00:65:10', **kwargs)

    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    # MANET routing protocols supported by proto:
    # babel, batman_adv, batmand and olsr
    # WARNING: we may need to stop Network Manager if you want
    # to work with babel
    protocols = ['babel', 'batman_adv', 'batmand', 'olsrd', 'olsrd2']
    kwargs = {}
    for proto in args:
        if proto in protocols:
            kwargs['proto'] = proto
    if 'proto' not in kwargs:
        info("*INFO: Not protocol selected*\n")

    net.addLink(sta1, cls=adhoc, intf='sta1-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', **kwargs)
    net.addLink(sta2, cls=adhoc, intf='sta2-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                **kwargs)
    net.addLink(sta3, cls=adhoc, intf='sta3-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', **kwargs)
    net.addLink(sta4, cls=adhoc, intf='sta4-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', **kwargs)
    net.addLink(sta5, cls=adhoc, intf='sta5-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', **kwargs)
    net.addLink(sta6, cls=adhoc, intf='sta6-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', **kwargs)
    net.addLink(sta7, cls=adhoc, intf='sta7-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', **kwargs)
    net.addLink(sta8, cls=adhoc, intf='sta8-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', **kwargs)
    net.addLink(sta9, cls=adhoc, intf='sta9-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', **kwargs)
    net.addLink(sta10, cls=adhoc, intf='sta10-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', **kwargs)

    if '-telemetry' not in args:
        net.plotGraph(min_x=0, min_y=0, max_x=500, max_y=500)

    info("*** Starting network\n")
    net.build()


    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
