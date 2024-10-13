#!/bin/sh
# Start Ganache in the background
ganache-cli -h 0.0.0.0 -p 7545 -d &

# Wait for Ganache to start
sleep 5

# Run Truffle migration
truffle migrate --network development

# Keep the container running
tail -f /dev/null
