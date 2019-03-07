## this filegroup exposes all .md files that are placed under the sub-directories of the root directory (where this BUILD file is located at)
## given the directory structure below, test-1.md and test-2.md are INCLUDED. test-0.md is EXCLUDED.
## root_directory:
##      test-0.md
##      sub-directory:
##          test-1.md
##          sub-sub-dir:
##              test-2.md

filegroup(
    name = "content",
    srcs = glob(
        ["*/**/*.md"],
        exclude=[
            "bazel-bin/**/*.md",
            "bazel-out/**/*.md",
            "bazel-docs/**/*.md",
            ".runfiles/**/*.md"
        ]
    ),
    visibility = ["//visibility:public"]
)

# When a Bazel build or test is executed with RBE, it will be executed using the following platform.
# The platform is based on the standard rbe_ubuntu1604 from @bazel_toolchains,
# but with an additional setting dockerNetwork = standard because our tests need network access
platform(
    name = "rbe-platform",
    parents = ["@bazel_toolchains//configs/ubuntu16_04_clang/1.1:rbe_ubuntu1604"],
    remote_execution_properties = """
        {PARENT_REMOTE_EXECUTION_PROPERTIES}
        properties: {
          name: "dockerNetwork"
          value: "standard"
        }
        """,
)