#!/bin/sh

echo "VirtuaPlant -- Bottle-filling Factory"
echo "- Starting World View"
./dist/oil_world -t localhost &
# ./oil_world.py -t localhost &
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

echo "- Starting HMI"
./dist/oil_hmi -t localhost &
# ./oil_hmi.py -t localhost &