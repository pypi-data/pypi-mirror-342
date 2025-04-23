# coding: utf-8

import os
import numpy
import pytest

from nxtomo.application.nxtomo import NXtomo
from nxtomo.nxobject.nxdetector import ImageKey

from tomoscan.io import HDF5File, get_swmr_mode
from tomoscan.esrf.scan.nxtomoscan import NXtomoScan

from nxtomomill import converter
from nxtomomill.converter.hdf5.acquisition.pcotomoacquisition import PCOTomoAcquisition
from nxtomomill.io.config import TomoHDF5Config
from nxtomomill.tests.utils.bliss import MockBlissAcquisition


configs = (
    {"nb_tomo": 1, "nb_loop": 5, "nb_turns": 5},
    {"nb_tomo": 5, "nb_loop": 1, "nb_turns": 5},
    {"nb_tomo": 2, "nb_loop": 3, "nb_turns": 6},
)


@pytest.mark.parametrize("pcotomo_version", (1, 2))
@pytest.mark.parametrize("config", configs)
def test_pcotomo_conversion(tmp_path, config: dict, pcotomo_version: int):
    n_darks = 10
    n_flats = 10
    bliss_scan_dir = str(tmp_path / "my_acquisition")
    nb_tomo = config["nb_tomo"]
    nb_loop = config["nb_loop"]
    nb_turns = config["nb_turns"]
    bliss_mock = MockBlissAcquisition(
        n_sample=1,
        n_sequence=1,
        n_scan_per_sequence=1,
        n_darks=n_darks,
        n_flats=n_flats,
        output_dir=bliss_scan_dir,
        acqui_type="pcotomo",
        with_rotation_motor_info=True,
        nb_tomo=nb_tomo if pcotomo_version == 1 else None,
        nb_loop=nb_loop if pcotomo_version == 1 else None,
        nb_turns=nb_turns if pcotomo_version == 2 else None,
    )
    sample_file = bliss_mock.samples[0].sample_file

    configuration = TomoHDF5Config()

    output_nx_file = os.path.join(str(tmp_path), "nexus_scans.nx")
    assert not os.path.exists(output_nx_file)
    configuration.output_file = output_nx_file
    configuration.input_file = sample_file
    configuration.request_input = False
    configuration.raises_error = False

    result = converter.from_h5_to_nx(configuration=configuration)
    assert os.path.exists(output_nx_file)
    # check we have our 5 NXtomo converted
    assert len(result) == nb_loop * nb_tomo
    # check saved datasets
    with HDF5File(sample_file, mode="r", swmr=get_swmr_mode()) as h5f:
        darks = h5f["2.1/instrument/pcolinux/data"][()]
        assert len(darks) == n_darks
        flats_1 = h5f["3.1/instrument/pcolinux/data"][()]
        assert len(flats_1) == n_flats
        projections = h5f["4.1/instrument/pcolinux/data"][()]
        assert len(projections) == 10 * nb_loop * nb_tomo
        flats_2 = h5f["5.1/instrument/pcolinux/data"][()]
        assert len(flats_2) == n_flats

    for i_nx_tomo, (file_path, data_path) in enumerate(result):
        with HDF5File(file_path, mode="r", swmr=get_swmr_mode()) as h5f:
            detector_path = "/".join([data_path, "instrument", "detector", "data"])
            detector_data = h5f[detector_path][()]
            expected_data = numpy.concatenate(
                [
                    darks,
                    flats_1,
                    projections[(10 * i_nx_tomo) : (10 * (i_nx_tomo + 1))],
                    flats_2,
                ]
            )
            numpy.testing.assert_array_equal(detector_data, expected_data)


def test_pcotomo_conversion_with_angle_subselection(tmp_path):
    bliss_scan_dir = str(tmp_path / "my_acquisition")
    nb_tomo = 1
    nb_loop = 1
    bliss_mock = MockBlissAcquisition(
        n_sample=1,
        n_sequence=1,
        n_scan_per_sequence=1,
        n_darks=1,
        n_flats=1,
        output_dir=bliss_scan_dir,
        acqui_type="pcotomo",
        with_rotation_motor_info=True,
        nb_tomo=nb_tomo,
        nb_loop=nb_loop,
    )
    sample_file = bliss_mock.samples[0].sample_file

    configuration = TomoHDF5Config()

    output_nx_file = os.path.join(str(tmp_path), "nexus_scans.nx")
    assert not os.path.exists(output_nx_file)
    configuration.output_file = output_nx_file
    configuration.input_file = sample_file
    configuration.request_input = False
    configuration.raises_error = False
    configuration.pcotomo_scan_range = 90
    configuration.pcotomo_start_angle_offset = 10
    configuration.pcotomo_n_nxtomo = 2
    configuration.raises_error = True
    configuration.pcotomo_shift_angles = False

    file_path, data_path = converter.from_h5_to_nx(configuration=configuration)[0]
    scan = NXtomoScan(file_path, data_path)
    is_proj_mask = scan.image_key == ImageKey.PROJECTION.value
    remaining_proj_angle = numpy.array(scan.rotation_angle)[is_proj_mask]
    assert remaining_proj_angle.min() >= 10
    assert remaining_proj_angle.max() <= 100

    configuration.pcotomo_shift_angles = True
    configuration.overwrite = True
    file_path, data_path = converter.from_h5_to_nx(configuration=configuration)[0]
    scan = NXtomoScan(file_path, data_path)
    is_proj_mask = scan.image_key == ImageKey.PROJECTION.value
    remaining_proj_angle = numpy.array(scan.rotation_angle)[is_proj_mask]
    assert remaining_proj_angle.min() >= 0
    assert remaining_proj_angle.max() <= 90


def test_get_projections_slices():
    """test the _get_projections_slices function"""
    nx_tomo = NXtomo("test")
    nx_tomo.instrument.detector.image_key_control = [2, 1, 0, 0, 0, 2]
    assert PCOTomoAcquisition._get_projections_slices(nx_tomo) == (slice(2, 5, 1),)
    nx_tomo.instrument.detector.image_key_control = [2, 1, 0, 0, 0, 2]
    assert PCOTomoAcquisition._get_projections_slices(nx_tomo) == (slice(2, 5, 1),)
    nx_tomo.instrument.detector.image_key_control = [2, 1]
    assert PCOTomoAcquisition._get_projections_slices(nx_tomo) == ()
    nx_tomo.instrument.detector.image_key_control = [0, 0, 2, 1, 0, 0, 1, 0, 0]
    assert PCOTomoAcquisition._get_projections_slices(nx_tomo) == (
        slice(0, 2, 1),
        slice(4, 6, 1),
        slice(7, 9, 1),
    )
