#!/bin/sh

echo "VirtuaPlant -- Bottle-filling Factory"
echo "- Starting World View"
./oil_world.py -t localhost &
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

#python3 ./oil_world_noGPIO.py -t 0.0.0.0 &
echo "- Starting HMI"
./oil_hmi.py -t localhost &
