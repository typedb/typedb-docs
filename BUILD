## this filegroup exposes all .md files that are placed under the sub-directories of the root directory (where this BUILD file is located at)
## given the directory structure below, test-1.md and test-2.md are INCLUDED. test-0.md is EXCLUDED.
## root_directory:
##      test-0.md
##      sub-directory:
##          test-1.md
##          sub-sub-dir:
##              test-2.md

load("@graknlabs_dependencies//distribution/artifact:rules.bzl", "artifact_extractor")

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

filegroup(
    name = "template",
    srcs = glob(
        ["*/**/*.yml"],
        exclude=[
            "bazel-bin/**/*.yml",
            "bazel-out/**/*.yml",
            "bazel-docs/**/*.yml",
            ".runfiles/**/*.yml"
        ]
    ),
    visibility = ["//visibility:public"]
)

filegroup(
    name = "autolink-keywords",
    srcs = ["views/autolink-keywords.js"],
    visibility = ["//visibility:public"]
)

artifact_extractor(
    name = "grakn-extractor",
    artifact = "@graknlabs_grakn_core_artifact//file",
)
