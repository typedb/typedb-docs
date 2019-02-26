exports_files(["package.json"])

#load("@build_bazel_rules_nodejs//:defs.bzl", "jasmine_node_test")
#
#jasmine_node_test(
#    name = "standalone-nodejs-phone-calls",
#    srcs = [
#        ":move-test-standalone-nodejs-phone-calls"
#    ],
#    deps = [
#        "@nodejs_dependencies//jasmine",
#        "@nodejs_dependencies//grakn-client",
#        "@nodejs_dependencies//papaparse",
#        "@nodejs_dependencies//stream-json",
#        "@nodejs_dependencies//xml-stream"
#    ],
#    data = [
#        ":generate-standalones-nodejs-phone-calls",
#        "//files:phone-calls-kg"
#    ]
#)
#
#genrule(
#    name = "generate-standalones-nodejs-phone-calls",
#    srcs = [
#        "//test/standalone:generate_standalone_tests.py",
#        "//:content"
#    ],
#    cmd = "python $(location //test/standalone:generate_standalone_tests.py) $(OUTS) $(locations //:content)",
#    outs = [
#        ## examples/migration-nodejs
#        "generated/phoneCallsCSVMigration.js",
#        "generated/phoneCallsJSONMigration.js",
#        "generated/phoneCallsXMLMigration.js",
#        ## examples/queries
##        "generated/PhoneCallsFirstQuery.js",
##        "generated/PhoneCallsSecondQuery.js",
##        "generated/PhoneCallsThirdQuery.js",
##        "generated/PhoneCallsForthQuery.js",
##        "generated/PhoneCallsFifthQuery.js",
#    ]
#)
#
#genrule(
#    name = "move-test-standalone-nodejs-phone-calls",
#    srcs = ["phoneCalls.js"],
#    cmd = "cp $(location phoneCalls.js) $(location generated/testStandalonePhoneCalls.test.js)",
#    outs = ["generated/testStandalonePhoneCalls.test.js"]
#)