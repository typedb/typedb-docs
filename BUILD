## this filegroup exposes all .md files that are placed under the sub-directories of the root directory (where this BUILD file is located at)
## given the directory structure below, test-1.md and test-2.md are INCLUDED. test-0.md is EXCLUDED.
## root_directory:
##      test-0.md
##      sub-directory:
##          test-1.md
##          sub-sub-dir:
##              test-2.md

load("@vaticle_typedb_common//test:rules.bzl", "native_typedb_artifact")
load("@vaticle_bazel_distribution//artifact:rules.bzl", "artifact_extractor")

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

native_typedb_artifact(
    name = "native-typedb-artifact",
    mac_artifact = "@vaticle_typedb_artifact_mac//file",
    linux_artifact = "@vaticle_typedb_artifact_linux//file",
    windows_artifact = "@vaticle_typedb_artifact_windows//file",
    output = "typedb-server-native.tar.gz",
    visibility = ["//test:__subpackages__"],
)

artifact_extractor(
    name = "typedb-extractor",
    artifact = ":native-typedb-artifact",
)

# CI targets that are not declared in any BUILD file, but are called externally
filegroup(
    name = "ci",
    data = [
        "@vaticle_dependencies//tool/bazelrun:rbe",
        "@vaticle_dependencies//tool/unuseddeps:unused-deps",
        "@vaticle_dependencies//tool/release:docs",
    ],
)
