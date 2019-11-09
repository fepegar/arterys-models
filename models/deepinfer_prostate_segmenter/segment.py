# -*- coding: utf-8 -*-

"""Script to convert a folder with a DICOM series into a volume file."""
import sys
import click
from pathlib import Path
from subprocess import call


## Generic I/O setup
# VOLUMES_DIR is where intermediate files (NIfTI, NNRD) are saved
VOLUMES_DIR = Path('/volumes')
VOLUMES_DIR.mkdir(exist_ok=True)

# OUTPUT_DIR is where the JSON and binary files are written
OUTPUT_DIR = Path('/output')
OUTPUT_DIR.mkdir(exist_ok=True)

# Define path types
INPUT_DIR_TYPE = click.Path(exists=True, file_okay=False)


@click.command()
@click.argument('dicom-dir', type=INPUT_DIR_TYPE)
@click.option('--debug/--no-debug', default=False, help='put output dir in input parent')
def main(dicom_dir, debug):
  import arterys

  # Custom I/O setup
  dicom_dir = Path(dicom_dir)
  input_name = dicom_dir.name
  input_volume_path = VOLUMES_DIR / '{}.nrrd'.format(input_name)
  output_volume_path = VOLUMES_DIR / '{}_seg.nrrd'.format(input_name)

  # DICOM to volumes
  arterys.dicomvert(dicom_dir, input_volume_path)

  # Run inference
  cmdline = (
    'python3', '/deepinfer/fit.py',
    '--ModelName', 'prostate-segmenter',
    '--Domain', 'BWH_WITHOUT_ERC',
    '--InputVolume', input_volume_path,
    '--OutputLabel', output_volume_path,
    '--ProcessingType', 'Accurate',
    '--Inference', 'Ensemble',
    '--verbose',
  )
  cmdline = [str(arg) for arg in cmdline]
  call(cmdline)

  # Volumes to Arterys format
  output_dir = dicom_dir.parent if debug else OUTPUT_DIR
  arterys.process_output(output_volume_path, output_dir)

  return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
