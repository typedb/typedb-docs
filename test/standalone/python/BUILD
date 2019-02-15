exports_files(["requirements.txt"])

load("@io_bazel_rules_python//python:python.bzl", "py_library", "py_test")
load("@pypi_dependencies//:requirements.bzl", "requirement")

py_library(
    name = "python-library-standalone-python-phone-calls",
    deps = [
        "@graknlabs_client_python//:client_python",
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
        ":python-library-standalone-python-phone-calls"
    ],
    data = [
        "//files:phone-calls-kg"
    ]
)

genrule(
    name = "generate-standalones-python-phone-calls",
    srcs = [
        "//test/standalone:generate_standalone_tests.py",
        "//:content"
    ],
    cmd = "python $(location //test/standalone:generate_standalone_tests.py) $(OUTS) $(locations //:content)",
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