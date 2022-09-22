import sys

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology(args):
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    kwargs = dict()
    
        
    if mobility:
    	sta1 = net.addStation('sta1', ip='10.0.0.1/24', **kwargs, encrypt='wpa3')
    	#sta2 = net.addStation('sta2', ip6='fe80::2', **kwargs, encrypt='wpa3')

    else:
    	sta1 = net.addStation('sta1', ip='10.0.0.1/24', position='10,10,0', **kwargs, passwd='123456789a', encrypt='wpa3')
    	sta2 = net.addStation('sta2', ip='10.0.0.2/24', position='50,10,0', **kwargs, passwd='123456789a', encrypt='wpa3')
        
    net.setPropagationModel(model="logDistance", exp=4)
    
    info("*** Configuring wifi nodes\n")
    #net.setModule('/home/wifi/Desktop/mac80211_hwsim/mac80211_hwsim.ko')
    net.configureWifiNodes()

    info("*** Creating links\n")

    kwargs['proto'] = 'batman_adv'
    
    net.addLink(sta1, cls=mesh, ssid='meshNet', intf='sta1-wlan0', channel=5, ht_cap='HT40+', **kwargs)
    
    net.addLink(sta2, cls=mesh, ssid='meshNet', intf='sta2-wlan0', channel=5, ht_cap='HT40+', **kwargs)
    
    net.plotGraph(max_x=100, max_y=100)
    
    if mobility:
        
        net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, min_v=0.5, max_v=0.8, seed=20)

    info("*** Starting network\n")
    net.build()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    mobility = True if '-m' in sys.argv else False
    topology(mobility)
