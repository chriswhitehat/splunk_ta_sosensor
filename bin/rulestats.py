#!/usr/bin/python

from glob import glob
from os import path

def normalize(sline):
    if len(sline) == 12:
        return sline
    elif len(sline) == 11:
        nline = [sline[0], sline[1]]
        nline.extend([sline[2][0], sline[2][1:]])
        nline.extend(sline[3:])
        return nline
    return []

def main():

    rulePaths = glob('/nsm/sensor_data/*/snort-*/rules_stats.txt*')

    rules = {}
    for rulePath in sorted(rulePaths):
        rules[path.dirname(rulePath)] = rulePath

    for rule in rules.values():
        srule = rule.split('/')
        sensorname = srule[3]
        instance = srule[4].split('snort-')[-1]
        timestamp = srule[-1].split('rules_stats.txt.')[-1]

        for stats in [y for y in [normalize(x.split()) for x in open(rule, 'r').read().splitlines()] if len(y) == 12][2:]:
            vals = [timestamp, sensorname, instance]
            vals.extend(stats[1:])
            print('%s sensorname="%s" instance=%s sid=%s gid=%s revision=%s checks=%s matches=%s alerts=%s microsecs=%s avg_per_check=%s avg_per_match=%s avg_per_nonmatch=%s disabled=%s' % tuple(vals))

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt):
        print("^C")
        exit()


