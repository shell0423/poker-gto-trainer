#!/bin/bash
# Solve a flop set (2-street) across N LOW-PRIORITY workers (shard by idx % N).
# Defaults: 3 workers + nice -n 19 (leaves ~7 of 10 cores free, machine stays usable).
# Each worker saves incrementally to data/srp_turn_parts/part_<i>.json and RESUMES if restarted.
#   usage: bash run_flops_batch.sh [N_workers] [flopfile]
cd "$(dirname "$0")"
N=${1:-3}
FLOPFILE=${2:-flops_subset.json}
mkdir -p data/srp_turn_parts
echo "START $(date) | $N workers (nice -n 19) | $FLOPFILE"
pids=()
for i in $(seq 0 $((N-1))); do
  nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
    .venv/bin/python solve_srp_turn.py shard "$i" "$N" "$FLOPFILE" > "data/srp_turn_parts/log_$i.txt" 2>&1 &
  pids+=($!)
done
echo "launched pids: ${pids[*]}"
wait
echo "ALL SHARDS DONE $(date)"
.venv/bin/python merge_flops.py
