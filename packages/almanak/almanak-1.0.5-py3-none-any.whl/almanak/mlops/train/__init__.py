"""This module will import the mlops sdk that will be pre-installed in the model training environment and surface the public API to the model training code."""

import sys
from pathlib import Path


def import_mlops_sdk():
    _DEV_MLOPS_SDK_ROOT_DIRECTORY = Path(__file__).parents[3] / "almanak-mlops"
    _PROD_MLOPS_SDK_ROOT_DIRECTORY = Path("/mlops_sdk")

    if _DEV_MLOPS_SDK_ROOT_DIRECTORY.exists():
        sys.path.append(_DEV_MLOPS_SDK_ROOT_DIRECTORY)
    if _PROD_MLOPS_SDK_ROOT_DIRECTORY.exists():
        sys.path.append(_PROD_MLOPS_SDK_ROOT_DIRECTORY)


import_mlops_sdk()
