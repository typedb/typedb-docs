exports_files(["package.json", "yarn.lock"])

load("@npm//@bazel/jasmine:index.bzl", "jasmine_node_test")

################################
# phone_calls Standalones Test #
################################

jasmine_node_test(
    name = "phone-calls",
    srcs = [":phone-calls-tests"],
    deps = [
        "@npm//jasmine",
        "@npm//jasmine-reporters",
        "@npm//typedb-client",
        "@npm//papaparse",
        "@npm//stream-json",
        "@npm//xml-stream"
    ],
    data = ["//files:phone-calls-kg"],
    size = "enormous"
)

genrule(
    name = "phone-calls-tests",
    srcs = [
        "nodejs_tests.py",
        "PhoneCalls.template.js",
        "//:content"
    ],
    cmd = "$(location nodejs_tests.py) $(location PhoneCalls.template.js) $(location PhoneCalls.test.js) $(locations //:content)",
    outs = ["PhoneCalls.test.js"]
)

###################################
# social_network Standalones Test #
###################################

jasmine_node_test(
    name = "social-network",
    srcs = [":social-network-tests"],
    deps = [
        "@npm//jasmine",
        "@npm//typedb-client",
        "@npm//jasmine-reporters"
    ],
    data = ["//files:social-network-kg"]
)

genrule(
    name = "social-network-tests",
    srcs = [
        "nodejs_tests.py",
        "SocialNetwork.template.js",
        "//:content"
    ],
    cmd = "$(location nodejs_tests.py) $(location SocialNetwork.template.js) $(location SocialNetwork.test.js) $(locations //:content)",
    outs = ["SocialNetwork.test.js"]
)
