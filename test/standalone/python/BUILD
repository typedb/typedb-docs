exports_files(["requirements.txt"])

load("@io_bazel_rules_python//python:python.bzl", "py_library", "py_test")
load("@pypi_dependencies//:requirements.bzl", "requirement")

py_library(
    name = "standalone-python-phone-calls",
    deps = [
        requirement('grakn'),
        requirement('csv')
  ]
)

py_test(
    name = "standalone-python-phone-calls",
    srcs = [
        "generated/phone_calls_csv_migration.py",
        "generated/test_standalone_phone_calls.py"
    ],
    deps = [
        "standalone-python-phone-calls"
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
        "generated/phone_calls_csv_migration.py"
    ]
)