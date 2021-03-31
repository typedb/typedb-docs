## this filegroup exposes all .md files that are placed under the sub-directories of the root directory (where this BUILD file is located at)
## given the directory structure below, test-1.md and test-2.md are INCLUDED. test-0.md is EXCLUDED.
## root_directory:
##      test-0.md
##      sub-directory:
##          test-1.md
##          sub-sub-dir:
##              test-2.md

load("@graknlabs_common//test:rules.bzl", "native_grakn_artifact")
load("@graknlabs_bazel_distribution//artifact:rules.bzl", "artifact_extractor")

filegroup(
    name = "content",
    srcs = glob(
        ["*/**/*.md"],
        exclude=[
	    "bazel-*/**/*.md",
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

native_grakn_artifact(
    name = "native-grakn-artifact",
    mac_artifact = "@graknlabs_grakn_core_artifact_mac//file",
    linux_artifact = "@graknlabs_grakn_core_artifact_linux//file",
    windows_artifact = "@graknlabs_grakn_core_artifact_windows//file",
    output = "grakn-core-server-native.tar.gz",
    visibility = ["//test:__subpackages__"],
)

artifact_extractor(
    name = "grakn-extractor",
    artifact = ":native-grakn-artifact",
)


# CI targets that are not declared in any BUILD file, but are called externally
filegroup(
    name = "ci",
    data = [
        "@graknlabs_dependencies//tool/bazelrun:rbe",
        "@graknlabs_dependencies//tool/unuseddeps:unused-deps",
        "@graknlabs_dependencies//tool/release:docs",
    ],
)
