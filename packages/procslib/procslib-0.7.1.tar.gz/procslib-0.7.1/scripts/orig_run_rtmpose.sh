#!/bin/bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/root/miniconda3/envs/faiss/lib/python3.10/site-packages/nvidia/cudnn/lib/:$LD_LIBRARY_PATH
# Run inference on 8 GPUs
for i in {0..7}
do
    CUDA_VISIBLE_DEVICES=$i python main.py $i &
done

# Wait for all background processes to finish
wait

# Combine all parquet files
python - <<EOF
import pandas as pd
import glob
import os

parquet_files = glob.glob('line_cnt_part_*.parquet')
dfs = [pd.read_parquet(file) for file in parquet_files]
combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_parquet('line_cnt_combined.parquet', index=False)

# Remove individual part files
for file in parquet_files:
    os.remove(file)

print("Combined results saved to line_cnt_combined.parquet")
EOF