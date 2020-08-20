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

load("@graknlabs_common//test/server:rules.bzl", "grakn_test")

############################
# Phone Calls Example Test #
############################

grakn_test(
    name = "phone-calls",
    test_class = "grakn.doc.test.example.PhoneCallsTest",
    srcs = [
        "PhoneCallsTest.java",
        ":phone-calls-tests",
    ],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
        "@maven//:org_sharegov_mjson",
        "@maven//:com_google_code_gson_gson",
        "@maven//:com_univocity_univocity_parsers",
        "@maven//:javax_xml_stream_stax_api",
    ],
    grakn_artifact = "@graknlabs_grakn_core_artifact//file",
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
grakn_test(
    name = "social-network",
    test_class = "grakn.doc.test.example.SocialNetworkTest",
    srcs = [
        "SocialNetworkTest.java",
        ":social-network-tests",
    ],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
    ],
    grakn_artifact = "@graknlabs_grakn_core_artifact//file",
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
        "GraknQuickstartA.java",
        "GraknQuickstartB.java",
        "GraknQuickstartC.java",
    ]
)
