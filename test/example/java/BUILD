#
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#

load("@vaticle_typedb_common//test:rules.bzl", "typedb_java_test", "native_typedb_artifact")

############################
# Phone Calls Example Test #
############################

native_typedb_artifact(
    name = "native-typedb-artifact",
    mac_artifact = "@vaticle_typedb_artifact_mac//file",
    linux_artifact = "@vaticle_typedb_artifact_linux//file",
    windows_artifact = "@vaticle_typedb_artifact_windows//file",
    output = "typedb-core-native.tar.gz",
    visibility = ["//test:__subpackages__"],
)


typedb_java_test(
    name = "phone-calls",
    test_class = "com.vaticle.doc.test.example.PhoneCallsTest",
    srcs = [
        "PhoneCallsTest.java",
        ":phone-calls-tests",
    ],
    deps = [
        "@vaticle_typedb_client_java//:client-java",
        "@vaticle_typedb_client_java//api",
        "@vaticle_typeql//java:typeql-lang",
        "@vaticle_typeql//java/common",
        "@vaticle_typeql//java/query",
        "@maven//:org_sharegov_mjson",
        "@maven//:com_google_code_gson_gson",
        "@maven//:com_univocity_univocity_parsers",
        "@maven//:javax_xml_stream_stax_api",
    ],
    server_mac_artifact = "@vaticle_typedb_artifact_mac//file",
    server_linux_artifact = "@vaticle_typedb_artifact_linux//file",
    server_windows_artifact = "@vaticle_typedb_artifact_windows//file",
    data = [
        "//files:phone-calls-kg",
    ]
)

genrule(
    name = "phone-calls-tests",
    srcs = [
        "java_tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "$(location java_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        ## examples/migration-java
        "PhoneCallsCSVMigration.java",
        "PhoneCallsJSONMigration.java",
        "PhoneCallsXMLMigration.java",
        ## examples/queries
        "PhoneCallsFirstQuery.java",
        "PhoneCallsSecondQuery.java",
        "PhoneCallsThirdQuery.java",
        "PhoneCallsForthQuery.java",
        "PhoneCallsFifthQuery.java",
    ]
)

###################################
# social_network Standalones Test #
###################################
typedb_java_test(
    name = "social-network",
    test_class = "com.vaticle.doc.test.example.SocialNetworkTest",
    srcs = [
        "SocialNetworkTest.java",
        ":social-network-tests",
    ],
    deps = [
        "@vaticle_typedb_client_java//:client-java",
        "@vaticle_typedb_client_java//api",
        "@vaticle_typeql//java:typeql-lang",
        "@vaticle_typeql//java/common",
        "@vaticle_typeql//java/query",
    ],
    server_mac_artifact = "@vaticle_typedb_artifact_mac//file",
    server_linux_artifact = "@vaticle_typedb_artifact_linux//file",
    server_windows_artifact = "@vaticle_typedb_artifact_windows//file",
    data = [
        "//files:social-network-kg",
    ]
)


genrule(
    name = "social-network-tests",
    srcs = [
        "java_tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "$(location java_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        # general/quickstart
        "SocialNetworkQuickstartQuery.java",
        # client-api/java
        "TypeDBQuickstartA.java",
        "TypeDBQuickstartB.java",
        "TypeDBQuickstartC.java",
    ]
)
