#!/bin/sh

echo "VirtuaPlant -- Bottle-filling Factory"
echo "- Starting World View"
./dist/world &
echo "- Starting HMI"
./dist/hmi &
