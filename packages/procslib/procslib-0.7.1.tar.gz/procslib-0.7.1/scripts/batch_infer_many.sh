#!/bin/bash


# =================== CHANGE CONFIGS HERE ===================


# Path to the Python script
SCRIPT_PATH="./infer_many.py"

# Directory containing the path files (<num>.parquet)
PATHS_DIR="/lv0/yada/trainlib/waterfront/data/vila_todo"

# Default arguments; check src/procslib/model_builder.py for available models
MODELS="vila"  # Example multi-model

PATH_COLUMN="local_path"
SAVE_DIR="/lv0/yada/trainlib/waterfront/data/vila_todo_res"


# =================== USUALLY NO NEED TO MODIFY BELOW ===================


# Create the save directory if it doesn't exist
mkdir -p "$SAVE_DIR"
mkdir -p "./logs"

# Iterate over devices 0-7
for DEVICE in {0..7}; do
  # Select the corresponding file for each device
  PATHS_FILE="${PATHS_DIR}/${DEVICE}.parquet"

  if [ "$DEVICE" -eq 0 ]; then
    # Progress display for device 0
    echo "Running on CUDA_VISIBLE_DEVICES=$DEVICE with file $PATHS_FILE (progress shown)..."
    CUDA_VISIBLE_DEVICES=$DEVICE python "$SCRIPT_PATH" \
      --paths_file "$PATHS_FILE" \
      --models "$MODELS" \
      --path_column "$PATH_COLUMN" \
      --save_dir "$SAVE_DIR" \
      --batch_size 64 &
  else
    # Run other devices in the background (no stdout)
    echo "Running on CUDA_VISIBLE_DEVICES=$DEVICE with file $PATHS_FILE..."
    CUDA_VISIBLE_DEVICES=$DEVICE python "$SCRIPT_PATH" \
      --paths_file "$PATHS_FILE" \
      --models "$MODELS" \
      --path_column "$PATH_COLUMN" \
      --save_dir "$SAVE_DIR" \
      --batch_size 64 > "./logs/device_${DEVICE}_log.log" 2>&1 &
  fi
done

# Wait for all background jobs to complete
wait
echo "All processes completed."
