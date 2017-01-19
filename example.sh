#!/bin/bash

python georand.py -n 100 \
        -b "5.5 46.6 15.8 54.83" \
        -o random_points.geojson \
        -i 2 \
        -p "num:1-10|cat:new-old-revised|magnitude:0.1-7.0"
