exports_files(["package.json"])

load("@build_bazel_rules_nodejs//:defs.bzl", "nodejs_jest_test")

nodejs_jest_test(
    name = "standalone-nodejs-phone-calls",
    srcs = [
        ":generate-standalones-nodejs-phone-calls",
        ":move-test-standalone-nodejs-phone-calls"
    ],
    deps = [
        "@graknlabs_client_nodejs//:client-nodejs",
        "@nodejs_dependencies//jest",
        "@nodejs_dependencies//fs-extra",
        "@nodejs_dependencies//:node_modules"
    ],
    data = [
        "@graknlabs_client_nodejs//:package.json",
    ],
    tests_root = "generated"
)

genrule(
    name = "generate-standalones-nodejs-phone-calls",
    srcs = [
        "//test/standalone:generate_standalone_tests.py",
        "//:content"
    ],
    cmd = "python $(location //test/standalone:generate_standalone_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        ## examples/migration-nodejs
        "generated/phoneCallsCSVMigration.js",
        "generated/phoneCallsJSONMigration.js",
        "generated/phoneCallsXMLMigration.js",
        ## examples/queries
#        "generated/PhoneCallsFirstQuery.js",
#        "generated/PhoneCallsSecondQuery.js",
#        "generated/PhoneCallsThirdQuery.js",
#        "generated/PhoneCallsForthQuery.js",
#        "generated/PhoneCallsFifthQuery.js",
    ]
)

genrule(
    name = "move-test-standalone-nodejs-phone-calls",
    srcs = ["phoneCalls.js"],
    cmd = "cp $(location phoneCalls.js) $(location generated/testStandalonePhoneCalls.test.js)",
    outs = ["generated/testStandalonePhoneCalls.test.js"]
)