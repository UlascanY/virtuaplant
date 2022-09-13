#!/bin/sh

echo "VirtuaPlant -- Bottle-filling Factory"
echo "- Starting World View"
#./oil_world.py -t localhost &
python3 ./oil_world_noGPIO.py -t 0.0.0.0 &
echo "- Starting HMI"
#./oil_hmi.py -t localhost &
