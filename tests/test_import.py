# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
#
# Class/individual/property/vocabulary entry existence tests are based on
# the change log at:
# https://github.com/spdx/spdx-3-model/blob/develop/CHANGELOG.md


def test_import():
    import spdx_python_model

    p = spdx_python_model.v3_0_1.Person()


def test_import_rename():
    from spdx_python_model import v3_0_1 as spdx_3_0

    p = spdx_3_0.Person()


def test_version():
    from spdx_python_model import VERSION

    print(VERSION)


def test_exist_class():
    """
    Test the existence of specific classes in SPDX versions
    """
    from spdx_python_model import v3_0_1

    # 3.0.1: "IndividualElement" class added
    e = v3_0_1.IndividualElement()


def test_exist_individual():
    """
    Test the existence of specific individuals in SPDX versions
    """

    from spdx_python_model import v3_0_1

    # 3.0.1: "SpdxOrganization" individual added
    o = v3_0_1.Organization()
    assert (
        "SpdxOrganization" in o.NAMED_INDIVIDUALS
    ), "3.0.1: 'SpdxOrganization' individual is missing"


def test_exist_property():
    """
    Test the existence of specific properties in SPDX versions
    """
    from spdx_python_model import v3_0_1

    # 3.0.1: "/Core/imports" replaced by "/Core/import"
    d = v3_0_1.SpdxDocument()
    assert hasattr(
        d, "import_"
    ), "3.0.1: 'import_' (import) property is missing from 'SpdxDocument'"

    # 3.0.1: "/Build/parameters" replaced by "Build/parameter"
    b = v3_0_1.build_Build()
    assert hasattr(
        b, "build_parameter"
    ), "3.0.1: 'build_parameter' property is missing from 'build_Build'"
    assert not hasattr(
        b, "build_parameters"
    ), "3.0.1: 'build_parameters' property should not be presented in 'build_Build'"

    # 3.0.1: "/Software/contentType" removed (duplicate of "/Core/contentType")
    f = v3_0_1.software_File()
    assert hasattr(
        f, "contentType"
    ), "3.0.1: 'contentType' property is missing from 'software_File'"
    assert not hasattr(
        f, "software_contentType"
    ), "3.0.1: 'software_contentType' property should not be presented in 'software_File'"

    p = v3_0_1.ai_AIPackage()
    assert hasattr(
        p, "ai_domain"
    ), "3.0.1: 'ai_domain' property is missing from 'ai_AIPackage'"


def test_exist_vocab_entry():
    """
    Test the existence of specific vocabulary entries in SPDX versions
    """

    from spdx_python_model import v3_0_1

    # 3.0.1: "adler32" added to "/Core/HashAlgorithm"
    h = v3_0_1.HashAlgorithm()
    assert hasattr(
        h, "adler32"
    ), "3.0.1: 'adler32' entry is missing from 'HashAlgorithm'"

    # 3.0.1: "hasPrerequsite" (misspelled) replaced by "hasPrerequisite"
    r = v3_0_1.RelationshipType()
    assert not hasattr(
        r, "hasPrerequsite"
    ), "3.0.1: 'hasPrerequsite' (misspelled) entry should not be presented in 'RelationshipType'"
    # 3.0.1: "hasInputs" replaced by "hasInput"
    assert not hasattr(
        r, "hasInputs"
    ), "3.0.1: 'hasInputs' entry should not be presented in 'RelationshipType'"
    # 3.0.1: "hasOutputs" replaced by "hasOutput"
    assert not hasattr(
        r, "hasOutputs"
    ), "3.0.1: 'hasOutputs' entry should not be presented in 'RelationshipType'"
