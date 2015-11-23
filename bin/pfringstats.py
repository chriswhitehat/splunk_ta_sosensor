#!/usr/bin/python

from glob import glob
from datetime import datetime
from os import path

def main():

    instanceCounter = {}

    sensortabs = [x.split() for x in open('/etc/nsm/sensortab').read().splitlines()]

    sensortab = {}

    for sensor in sensortabs:
        sensortab[sensor[-1].lower()] = sensor[0].upper()

    pf_ring_files = glob('/proc/net/pf_ring/*-*')

    for ring in pf_ring_files:
        pf_ring = {'ring': path.basename(ring)}

        ringLines = open(ring).read().splitlines()

        for line in ringLines:
            attribute = None

            if "Bound Device" in line:
                attribute = 'interface'
            elif "Appl. Name" in line:
                attribute = 'application'
            elif "Min Num Slots" in line:
                attribute = 'min_slots'
            elif 'Tot Packets' in line:
                attribute = 'recvd'
            elif 'Tot Pkt Lost' in line:
                attribute = 'dropped'
            elif 'Tot Memory' in line:
                attribute = 'memory'
            elif 'Num Free Slots' in line:
                attribute = 'free_slots'

            if attribute:
                pf_ring[attribute] = line.split(':')[-1].strip()
        
        pf_ring['sensorname'] = sensortab[pf_ring['interface']]

        if pf_ring['application'] in instanceCounter:
            instanceCounter[pf_ring['application']] += 1
        else:
            instanceCounter[pf_ring['application']] = 1

        pf_ring['instance'] = instanceCounter[pf_ring['application']]

        print(datetime.now().strftime('%s') + ' sensorname="%(sensorname)s" interface="%(interface)s" instance="%(instance)s" ring="%(ring)s" application="%(application)s" memory="%(memory)s" min_slots="%(min_slots)s" free_slots="%(free_slots)s" recvd="%(recvd)s" dropped="%(dropped)s"' % pf_ring) 


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt):
        print("^C")
        exit()

