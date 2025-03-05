# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0


def test_import():
    import spdx_python_model

    p = spdx_python_model.v3_0_1.Person()


def test_import_rename():
    from spdx_python_model import v3_0_1 as spdx_3_0

    p = spdx_3_0.Person()


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
    ), "3.0.1: 'build_parameters' attribute should not be presented in 'build_Build'"

    # 3.0.1: "/Software/contentType" removed (duplicate of "/Core/contentType")
    f = v3_0_1.software_File()
    assert hasattr(
        f, "contentType"
    ), "3.0.1: 'contentType' property is missing from 'software_File'"
    assert not hasattr(
        f, "software_contentType"
    ), "3.0.1: 'software_contentType' attribute should not be presented in 'software_File'"

    p = v3_0_1.ai_AIPackage()
    assert hasattr(
        p, "ai_domain"
    ), "3.0.1: 'ai_domain' property is missing from 'ai_AIPackage'"


def test_vocab_entry_exist():
    """
    Test the existence of specific vocabulary entries in SPDX versions

    Based on the change log:
    https://github.com/spdx/spdx-3-model/blob/develop/CHANGELOG.md
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


def test_special_individual_exist():
    """
    Test the existence of specific individuals in SPDX versions

    Based on the change log:
    https://github.com/spdx/spdx-3-model/blob/develop/CHANGELOG.md
    """

    from spdx_python_model import v3_0_1

    # 3.0.1: "SpdxOrganization" added
    o = v3_0_1.Organization()
    assert (
        "SpdxOrganization" in o.NAMED_INDIVIDUALS
    ), "3.0.1: 'SpdxOrganization' is missing"
