#!/usr/bin/env python3

# Generic I/O setup
VOLUMES_DIR="/volumes"
OUTPUT_DIR="/output"
mkdir -p $VOLUMES_DIR $OUTPUT_DIR

# Custom I/O setup
INPUT_DIR=$1
INPUT_NAME=$(basename $INPUT_DIR)
INPUT_VOLUME=${VOLUMES_DIR}/${INPUT_NAME}.nrrd
OUTPUT_VOLUME=${VOLUMES_DIR}/${INPUT_NAME}_seg.nrrd

# DICOM to volumes
dicomvert $INPUT_DIR

# Run inference
python3 /deepinfer/fit.py \
  --ModelName prostate-segmenter \
  --Domain BWH_WITHOUT_ERC \
  --InputVolume $INPUT_VOLUME \
  --OutputLabel $OUTPUT_VOLUME \
  --ProcessingType Accurate\
  --Inference Ensemble\
  --verbose

# Volumes to Arterys
process_output $OUTPUT_VOLUME $OUTPUT_DIR
