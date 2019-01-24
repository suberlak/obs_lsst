#
# LSST Data Management System
# Copyright 2017 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
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
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import os.path
import lsst.utils as utils
from lsst.obs.base.yamlCamera import YamlCamera
from . import LsstCamMapper, LsstCamMakeRawVisitInfo
from .ingest import LsstCamParseTask
from .translators import ImSimTranslator

__all__ = ["ImsimMapper", "ImsimCam", "ImsimParseTask"]


class ImsimCam(YamlCamera):
    """The imsim realisation of the real LSST 3.2Gpix Camera
    """
    packageName = 'obs_lsst'

    def __init__(self, cameraYamlFile=None):
        """Construct lsstCam for imsim
        """
        if not cameraYamlFile:
            cameraYamlFile = os.path.join(utils.getPackageDir(self.packageName), "policy", "imsim.yaml")

        YamlCamera.__init__(self, cameraYamlFile)


class ImsimMakeRawVisitInfo(LsstCamMakeRawVisitInfo):
    """Make a VisitInfo from the FITS header of a raw image."""
    metadataTranslator = ImSimTranslator


class ImsimMapper(LsstCamMapper):
    """The Mapper for the imsim simulations of the LsstCam."""
    translatorClass = ImSimTranslator
    MakeRawVisitInfoClass = ImsimMakeRawVisitInfo

    @classmethod
    def getCameraName(cls):
        return "imsim"

    def _makeCamera(self, policy, repositoryDir):
        """Make a camera (instance of lsst.afw.cameraGeom.Camera) describing the camera geometry."""
        return ImsimCam()


class ImsimParseTask(LsstCamParseTask):
    """Parser suitable for phosim data.
    """

    _cameraClass = ImsimCam           # the class to instantiate for the class-scope camera
    _translatorClass = ImSimTranslator
