exports_files(["requirements.txt"])

load("@rules_python//python:pip.bzl", "pip3_import")
load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@test_links_pip//:requirements.bzl",
       test_links_requirement = "requirement")

py_test(
    name = "test",
    main = "links_test.py",
    srcs = ["links_test.py"],
    deps = [
        test_links_requirement("PyYAML"),
        test_links_requirement("nested-lookup"),
        test_links_requirement("six")
    ],
    data = [
        "//:content",
        "//:template",
        "//:autolink-keywords"
    ],
    python_version = "PY3",
)
