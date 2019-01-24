# This file is part of obs_lsst.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Metadata translation support code for LSST headers"""

__all__ = ("ROLLOVERTIME", "TZERO", "LSST_LOCATION", "read_detector_ids",
           "compute_detector_exposure_id_generic")

import os.path
import yaml

from astropy.time import Time, TimeDelta
from astropy.coordinates import EarthLocation

from lsst.utils import getPackageDir

# LSST day clock starts at UTC+8
ROLLOVERTIME = TimeDelta(8*60*60, scale="tai", format="sec")
TZERO = Time("2010-01-01T00:00", format="isot", scale="utc")

# LSST Default location in the absence of headers
LSST_LOCATION = EarthLocation.from_geodetic(-30.244639, -70.749417, 2663.0)

obs_lsst_packageDir = getPackageDir("obs_lsst")


def read_detector_ids(policyFile):
    """Read a camera policy file and retrieve the mapping from CCD name
    to ID.

    Parameters
    ----------
    policyFile : `str`
        Name of YAML policy file to read, relative to the obs_lsst
        package.

    Returns
    -------
    mapping : `dict` of `str` to `int`
        A `dict` with keys being the full names of the detectors, and the
        value is the integer detector number.

    Notes
    -----
    Reads the camera YAML definition file directly and extracts just the
    IDs.  This routine does not use the standard
    `~lsst.obs.base.yamlCamera.YAMLCamera` infrastructure or
    `lsst.afw.cameraGeom`.  This is because the translators are intended to
    have minimal dependencies on LSST infrastructure.
    """

    file = os.path.join(obs_lsst_packageDir, policyFile)
    with open(file) as fh:
        # Use the fast parser since these files are large
        camera = yaml.load(fh, Loader=yaml.CLoader)

    mapping = {}
    for ccd, value in camera["CCDs"].items():
        mapping[ccd] = int(value["id"])

    return mapping


def compute_detector_exposure_id_generic(exposure_id, detector_num, max_num=1000, mode="concat"):
    """Compute the detector_exposure_id from the exposure id and the
    detector number.

    Parameters
    ----------
    exposure_id : `int`
        The exposure ID.
    detector_num : `int`
        The detector number.
    max_num : `int`, optional
        Maximum number of detectors to make space for. Defaults to 1000.
    mode : `str`, optional
        Computation mode. Defaults to "concat".
        - concat : Concatenate the exposure ID and detector number, making
                   sure that there is space for max_num and zero padding.
        - multiply : Multiply the exposure ID by the maximum detector
                     number and add the detector number.

    Returns
    -------
    detector_exposure_id : `int`
        Computed ID.
    """

    if detector_num >= max_num:
        raise ValueError(f"Detector number has value {detector_num} >= {max_num}")

    if mode == "concat":
        npad = len(str(max_num))
        return int(f"{exposure_id}{detector_num:0{npad}d}")
    elif mode == "multiply":
        return max_num*exposure_id + detector_num
    else:
        raise ValueError(f"Computation mode of '{mode}' is not understood")
