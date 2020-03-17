exports_files(["requirements.txt"])

load("@io_bazel_rules_python//python:python.bzl", "py_library", "py_test")
load("@test_example_pip//:requirements.bzl",
       test_example_requirement = "requirement")


############################
# Phone Calls Example Test #
############################

py_test(
    name = "phone-calls",
    main = "phone_calls_test.py",
    srcs = [
        "phone_calls_test.py",
        ":phone-calls-tests",
    ],
    deps = [
        "@graknlabs_client_python//:client_python",
        test_example_requirement("ijson")
    ],
    data = ["//files:phone-calls-kg"],
    imports = ["."],
    python_version = "PY2",
)

genrule(
    name = "phone-calls-tests",
    srcs = [
        "python_tests.py",
        "//:content"
    ],
    cmd = "$(location python_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        ## examples/migration-python
        "phone_calls_csv_migration.py",
        "phone_calls_json_migration.py",
        "phone_calls_xml_migration.py",
        ## examples/queries
        "phone_calls_first_query.py",
        "phone_calls_second_query.py",
        "phone_calls_third_query.py",
        "phone_calls_forth_query.py",
        "phone_calls_fifth_query.py",
    ]
)

################################
## Social Network Example Test #
################################

py_test(
    name = "social-network",
    main = "social_network_test.py",
    srcs = [
        "social_network_test.py",
        ":social-network-tests",
    ],
    deps = ["@graknlabs_client_python//:client_python"],
    data = ["//files:social-network-kg"],
    imports = ["."],
    python_version = "PY2",
)

genrule(
    name = "social-network-tests",
    srcs = [
        "python_tests.py",
        "//:content"
    ],
    cmd = "$(location python_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        # general/quickstart
        "social_network_quickstart_query.py",
        # client-api/python
        "social_network_python_client_a.py",
        "social_network_python_client_b.py",
        "social_network_python_client_c.py",
        "social_network_python_client_d.py",
        # client-api/new-client
        "social_network_create_new_client_a.py",
        "social_network_create_new_client_b.py"
    ]
)
