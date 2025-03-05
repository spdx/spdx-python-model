# SPDX_License-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0


def test_import():
    import spdx_python_model

    p = spdx_python_model.v3_0_1.Person()


def test_import_rename():
    from spdx_python_model import v3_0_1 as spdx_3_0_1

    p = spdx_3_0_1.Person()


def test_version():
    from spdx_python_model import VERSION

    print(VERSION)


def test_property_exist():
    """
    Test the existence of specific properties in SPDX versions

    Based on the change log:
    https://github.com/spdx/spdx-3-model/blob/develop/CHANGELOG.md
    """
    from spdx_python_model import v3_0_1

    # "imports" replaced by "import" in 3.0.1
    d = v3_0_1.SpdxDocument()
    assert hasattr(
        d, "import_"
    ), "'import_' (import) attribute is missing from 'SpdxDocument'"

    # "parameters" replaced by "parameter" in 3.0.1
    b = v3_0_1.build_Build()
    assert hasattr(
        b, "build_parameter"
    ), "'build_parameter' attribute is missing from 'build_Build'"
    assert not hasattr(
        b, "build_parameters"
    ), "'build_parameters' attribute should not be presented in 'build_Build'"

    p = v3_0_1.ai_AIPackage()
    assert hasattr(
        p, "ai_domain"
    ), "'ai_domain' attribute is missing from 'ai_AIPackage'"
