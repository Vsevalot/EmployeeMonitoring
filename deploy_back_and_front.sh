#!/bin/sh

# Save the current directory
ORIGINAL_DIR=$(pwd)

# Check if "front", "back", and "mobile" directories exist
if [ ! -d "front" ] || [ ! -d "back" ] || [ ! -d "mobile" ]; then
  echo "Error: This script must be run from a directory where 'front', 'back', and 'mobile' folders exist."
  exit 1
fi

# Navigate to "front", stop the containers, and rebuild
cd front || exit
echo "Stopping 'front' containers..."
docker compose down
echo "Starting 'front' containers with build..."
docker compose up --build

# Return to the original directory
cd "$ORIGINAL_DIR" || exit

# Navigate to "back", stop the containers, and rebuild
cd back || exit
echo "Stopping 'back' containers..."
docker compose down
echo "Starting 'back' containers with build..."
docker compose up --build

echo "All tasks completed successfully."

