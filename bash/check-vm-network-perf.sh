#!/bin/bash
for i in `vsish -e ls /net/portsets/ | cut -c 1- | sed 's:/.*::'`; do for p in `vsish -e ls /net/portsets/$i/ports | cut -c 1- | sed 's:/.*::'`; do vsish -e cat /net/portsets/$i/ports/$p/status | grep "clientName" >> /tmp/buffer.txt; vsish -e cat /net/portsets/$i/ports/$p/stats | egrep -E "droppedTx|droppedRx" >> /tmp/buffer.txt; vsish -e cat /net/portsets/$i/ports/$p/vmxnet3/rxSummary 2>/dev/null  | egrep -E "running out of buffers|1st ring size|of times the 1st ring is full" >> /tmp/buffer.txt; echo "---------------------------" >> /tmp/buffer.txt; done done;

less /tmp/buffer.txt
