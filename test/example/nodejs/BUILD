exports_files(["package.json"])

load("@build_bazel_rules_nodejs//:defs.bzl", "jasmine_node_test")

################################
# phone_calls Standalones Test #
################################

jasmine_node_test(
    name = "standalone-nodejs-phone-calls",
    srcs = [
        ":generate-standalone-tests-phone-calls-nodejs"
    ],
    deps = [
        "@nodejs_dependencies//jasmine",
        "@nodejs_dependencies//jasmine-reporters",
        "@nodejs_dependencies//grakn-client",
        "@nodejs_dependencies//papaparse",
        "@nodejs_dependencies//stream-json",
        "@nodejs_dependencies//xml-stream"
    ],
    data = [
        "//files:phone-calls-kg"
    ]
)

genrule(
    name = "generate-standalone-tests-phone-calls-nodejs",
    srcs = [
        "generate_standalone_tests.py",
        "phoneCallsTemplate.js",
        "//:content"
    ],
    cmd = "python $(location generate_standalone_tests.py) $(location phoneCallsTemplate.js) $(location generated/testStandalonePhoneCalls.test.js) $(locations //:content)",
    outs = ["generated/testStandalonePhoneCalls.test.js"]
)

###################################
# social_network Standalones Test #
###################################

jasmine_node_test(
    name = "standalone-nodejs-social-network",
    srcs = [
        ":generate-standalone-tests-social-network-nodejs"
    ],
    deps = [
        "@nodejs_dependencies//jasmine",
        "@nodejs_dependencies//grakn-client",
        "@nodejs_dependencies//jasmine-reporters"
    ],
    data = [
        "//files:social-network-kg"
    ]
)

genrule(
    name = "generate-standalone-tests-social-network-nodejs",
    srcs = [
        "generate_standalone_tests.py",
        "socialNetworkTemplate.js",
        "//:content"
    ],
    cmd = "python $(location generate_standalone_tests.py) $(location socialNetworkTemplate.js) $(location generated/testStandaloneSocialNetwork.test.js) $(locations //:content)",
    outs = ["generated/testStandaloneSocialNetwork.test.js"]
)