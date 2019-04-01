exports_files(["package.json"])

load("@build_bazel_rules_nodejs//:defs.bzl", "jasmine_node_test")

################################
# phone_calls Standalones Test #
################################

jasmine_node_test(
    name = "phone-calls",
    srcs = [":phone-calls-tests"],
    deps = [
        "@test_example_npm//jasmine",
        "@test_example_npm//jasmine-reporters",
        "@test_example_npm//grakn-client",
        "@test_example_npm//papaparse",
        "@test_example_npm//stream-json",
        "@test_example_npm//xml-stream"
    ],
    data = ["//files:phone-calls-kg"]
)

genrule(
    name = "phone-calls-tests",
    srcs = [
        "nodejs_tests.py",
        "PhoneCalls.template.js",
        "//:content"
    ],
    cmd = "python $(location nodejs_tests.py) $(location PhoneCalls.template.js) $(location PhoneCalls.test.js) $(locations //:content)",
    outs = ["PhoneCalls.test.js"]
)

###################################
# social_network Standalones Test #
###################################

jasmine_node_test(
    name = "social-network",
    srcs = [":social-network-tests"],
    deps = [
        "@test_example_npm//jasmine",
        "@test_example_npm//grakn-client",
        "@test_example_npm//jasmine-reporters"
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
    cmd = "python $(location nodejs_tests.py) $(location SocialNetwork.template.js) $(location SocialNetwork.test.js) $(locations //:content)",
    outs = ["SocialNetwork.test.js"]
)