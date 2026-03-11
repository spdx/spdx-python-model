#
# SPDX-License-Identifier: Apache-2.0
#

from .bindings import *
from .version import VERSION

from .bindings import _CONTEXT_TABLE

from pathlib import Path
import json


class LoadError(Exception):
    pass


def load_data(data):
    """
    Automatically load a SPDX 3 JSON document with the correct model based on
    its context

    :param data: The decoded JSON data as a Python dict

    :returns: A tuple that contains the model and the decoded SHACLObjectSet

    :raises LoadError: If the data is missing a context or if the context is
        not recognized
    :raises TypeError: If the data is not a dictionary
    """

    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary")

    if "@context" not in data:
        raise LoadError("No @context in data")

    context_url = None

    if isinstance(data["@context"], str):
        context_url = data["@context"]
    elif isinstance(data["@context"], list):
        for item in data["@context"]:
            if isinstance(item, str):
                context_url = item
                break

    if not context_url:
        raise LoadError("No valid @context URL string found in data")

    if context_url not in _CONTEXT_TABLE:
        raise LoadError(f"Unknown context URL '{context}'")

    model = _CONTEXT_TABLE[context_url]

    d = model.JSONLDDeserializer()
    objset = model.SHACLObjectSet()

    d.deserialize_data(data, objset)

    return model, objset


def load(path: Path):
    """
    Automatically load a SPDX 3 JSON document with the correct model based on
    its context

    :param data: The path to the SPDX 3 JSON file

    :returns: A tuple that contains the model and the decoded SHACLObjectSet

    :raises LoadError: If the data is missing a context or if the context is
        not recognized
    :raises TypeError: If the data is not a dictionary
    """
    with path.open("r") as f:
        data = json.load(f)

    return load_data(data)
