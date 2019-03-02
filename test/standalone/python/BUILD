exports_files(["requirements.txt"])

load("@io_bazel_rules_python//python:python.bzl", "py_library", "py_test")
load("@pypi_dependencies//:requirements.bzl", "requirement")
load("@local_pypi_dependencies//:requirements.bzl", "requirement")

py_library(
    name = "python-library-standalone-python-common",
    deps = [
        "@graknlabs_client_python//:client_python"
    ]
)

#################################
## phone_calls Standalones Test #
#################################

py_library(
    name = "python-library-standalone-python-phone-calls",
    deps = [
        requirement("ijson")
    ]
)

py_test(
    name = "standalone-python-phone-calls",
    main = "generated/test_standalone_phone_calls.py",
    srcs = [
        ":generate-standalones-python-phone-calls",
        ":move-test-standalone-python-phone-calls"
    ],
    deps = [
        ":python-library-standalone-python-common",
        ":python-library-standalone-python-phone-calls"
    ],
    data = [
        "//files:phone-calls-kg"
    ]
)

genrule(
    name = "generate-standalones-python-phone-calls",
    srcs = [
        "generate_standalone_tests.py",
        "//:content"
    ],
    cmd = "python $(location generate_standalone_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        ## examples/migration-python
        "generated/phone_calls_csv_migration.py",
        "generated/phone_calls_json_migration.py",
        "generated/phone_calls_xml_migration.py",
        ## examples/queries
        "generated/phone_calls_first_query.py",
        "generated/phone_calls_second_query.py",
        "generated/phone_calls_third_query.py",
        "generated/phone_calls_forth_query.py",
        "generated/phone_calls_fifth_query.py",
    ]
)

genrule(
    name = "move-test-standalone-python-phone-calls",
    srcs = ["phone_calls.py"],
    cmd = "cp $(location phone_calls.py) $(location generated/test_standalone_phone_calls.py)",
    outs = ["generated/test_standalone_phone_calls.py"]
)

####################################
## social_network Standalones Test #
####################################

py_test(
    name = "standalone-social-network",
    main = "generated/test_standalone_social_network.py",
    srcs = [
        ":generate-standalones-python-social-network",
        ":move-test-standalone-python-social-network"
    ],
    deps = [
        ":python-library-standalone-python-common"
    ],
    data = [
        "//files:social-network-kg"
    ]
)

genrule(
    name = "generate-standalones-python-social-network",
    srcs = [
        "generate_standalone_tests.py",
        "//:content"
    ],
    cmd = "python $(location generate_standalone_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        # general/quickstart
        "generated/social_network_quickstart_query.py",
        # client-api/python
        "generated/social_network_python_client_a.py",
        "generated/social_network_python_client_b.py",
        "generated/social_network_python_client_c.py",
        "generated/social_network_python_client_d.py",
    ]
)

genrule(
    name = "move-test-standalone-python-social-network",
    srcs = ["social_network.py"],
    cmd = "cp $(location social_network.py) $(location generated/test_standalone_social_network.py)",
    outs = ["generated/test_standalone_social_network.py"]
)