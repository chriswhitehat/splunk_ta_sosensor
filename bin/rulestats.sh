#!/bin/bash

unset LD_LIBRARY_PATH

if [ -d /nsm ]
then
    /usr/bin/python $SPLUNK_HOME/etc/apps/TA-sosensor/bin/rulestats.py
fi

