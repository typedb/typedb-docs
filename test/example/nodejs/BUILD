exports_files(["package.json"])

load("@build_bazel_rules_nodejs//:defs.bzl", "jasmine_node_test")

################################
# phone_calls Standalones Test #
################################

jasmine_node_test(
    name = "phone-calls",
    srcs = [":phone-calls-tests"],
    deps = [
        "@nodejs_dependencies//jasmine",
        "@nodejs_dependencies//jasmine-reporters",
        "@nodejs_dependencies//grakn-client",
        "@nodejs_dependencies//papaparse",
        "@nodejs_dependencies//stream-json",
        "@nodejs_dependencies//xml-stream"
    ],
    data = ["//files:phone-calls-kg"]
)

genrule(
    name = "phone-calls-tests",
    srcs = [
        "nodejs-tests.py",
        "PhoneCalls.template.js",
        "//:content"
    ],
    cmd = "python $(location nodejs-tests.py) $(location PhoneCalls.template.js) $(location PhoneCalls.test.js) $(locations //:content)",
    outs = ["PhoneCalls.test.js"]
)

###################################
# social_network Standalones Test #
###################################

jasmine_node_test(
    name = "social-network",
    srcs = [":social-network-tests"],
    deps = [
        "@nodejs_dependencies//jasmine",
        "@nodejs_dependencies//grakn-client",
        "@nodejs_dependencies//jasmine-reporters"
    ],
    data = ["//files:social-network-kg"]
)

genrule(
    name = "social-network-tests",
    srcs = [
        "nodejs-tests.py",
        "SocialNetwork.template.js",
        "//:content"
    ],
    cmd = "python $(location nodejs-tests.py) $(location SocialNetwork.template.js) $(location SocialNetwork.test.js) $(locations //:content)",
    outs = ["SocialNetwork.test.js"]
)