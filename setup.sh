#!/bin/bash
# setup.sh - Create project directories and log setup

# Create directories if they don't exist
mkdir -p essays
mkdir -p reports

# Log the setup
echo "Setup run at $(date) - ensured directories essays/ and reports/" >> setup.log

echo "Setup complete."
