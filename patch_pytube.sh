#!/bin/bash

# Filename to search for
FILENAME="innertube.py"

# Use find to locate all instances of innertube.py within the Python environments
find / -type f -name "$FILENAME" | while read -r file_path; do
    echo "Modifying $file_path..."
    # Use sed to replace the target string
    sed -i "s/def __init__(self, client='ANDROID_MUSIC', use_oauth=False, allow_cache=True):/def __init__(self, client='WEB', use_oauth=False, allow_cache=True):/" "$file_path"
    # Check if sed completed successfully
    if [ $? -eq 0 ]; then
        echo "Modified: $file_path"
    else
        echo "Failed to modify: $file_path"
    fi
done

echo "All modifications completed."
