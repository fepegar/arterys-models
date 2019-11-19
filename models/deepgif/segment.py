# -*- coding: utf-8 -*-

"""Script to convert a folder with a DICOM series into a volume file."""
import sys
import click
from pathlib import Path
from subprocess import call


## Generic I/O setup
# VOLUMES_DIR is where intermediate files (NIfTI, NNRD) are saved
VOLUMES_DIR = Path('/volumes')

# OUTPUT_DIR is where the JSON and binary files are written
OUTPUT_DIR = Path('/output')

# Define path types
INPUT_DIR_TYPE = click.Path(exists=True, file_okay=False)


@click.command()
@click.argument('dicom-dir', type=INPUT_DIR_TYPE)
@click.option(
    '--debug/--no-debug',
    default=False,
    help='put output dirs in mounted volume',
)
@click.option(
    '--filter/--no-filter',
    default=False,
    help='remove some labels and small connected components',
)
def main(dicom_dir, debug, filter):
    import arterys

    # Custom I/O setup
    dicom_dir = Path(dicom_dir)
    input_name = dicom_dir.name
    volumes_dir = dicom_dir.parent / VOLUMES_DIR.name if debug else VOLUMES_DIR
    volumes_dir.mkdir(exist_ok=True)
    input_volume_path = volumes_dir / '{}.nii.gz'.format(input_name)
    output_volume_path = volumes_dir / '{}_seg.nii.gz'.format(input_name)

    # DICOM to volumes
    arterys.dicomvert(dicom_dir, input_volume_path)

    # Run inference
    cmdline = (
        'deepgif', input_volume_path,
        '--output-path', output_volume_path,
        '--hist-niftynet',
    )
    cmdline = [str(arg) for arg in cmdline]
    call(cmdline)

    # Filter segmentation for RSNA
    name = output_volume_path.name.replace('.nii', '_filtered.nii')
    output_volume_filtered_path = output_volume_path.parent / name
    filter_segmentation(output_volume_path, output_volume_filtered_path)

    # Volumes to Arterys format
    output_dir = dicom_dir.parent / OUTPUT_DIR.name if debug else OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    arterys.process_output(output_volume_filtered_path, output_dir)

    return 0


def filter_segmentation(
        input_path,
        output_path,
        minimum_label=5,
        minimum_size=50,
        ):
    """
    Hack for RSNA demo to avoid massive output folder
    """
    import numpy as np
    from tqdm import tqdm
    import SimpleITK as sitk
    image = sitk.ReadImage(str(input_path))
    result_array = sitk.GetArrayFromImage(image)
    result_array[result_array < minimum_label] = 0

    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(image)
    num_labels = stats.GetNumberOfLabels()
    progress_labels = tqdm(stats.GetLabels())
    for label in progress_labels:
        if label < minimum_label: continue
        progress_labels.set_description(
            'Processing label {}'.format(label))
        binary_image = image == label
        connected_components = sitk.ConnectedComponent(binary_image)
        cc_stats = sitk.LabelShapeStatisticsImageFilter()
        cc_stats.Execute(connected_components)
        num_cc = cc_stats.GetNumberOfLabels()
        txt = 'Connected components in label {}: {}'.format(label, num_cc)
        tqdm.write(txt)
        progress_cc = tqdm(cc_stats.GetLabels(), leave=False)
        for cc_label in progress_cc:
            progress_cc.set_description(
                'Processing connected component {}'.format(cc_label))
            connected_component = connected_components == cc_label
            array = sitk.GetArrayFromImage(connected_component).astype(bool)
            if array.sum() < minimum_size:
                result_array[array] = 0
    result_image = sitk.GetImageFromArray(result_array)
    result_image.SetDirection(image.GetDirection())
    result_image.SetSpacing(image.GetSpacing())
    result_image.SetOrigin(image.GetOrigin())
    sitk.WriteImage(result_image, str(output_path))


if __name__ == "__main__":
        sys.exit(main())    # pragma: no cover
