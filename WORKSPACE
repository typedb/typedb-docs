#
# Copyright (C) 2020 Grakn Labs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

workspace(name = "graknlabs_docs")

################################
# Load @graknlabs_dependencies #
################################
load("//dependencies/graknlabs:repositories.bzl", "graknlabs_dependencies")
graknlabs_dependencies()

# Load Antlr
load("@graknlabs_dependencies//builder/antlr:deps.bzl", antlr_deps = "deps")
antlr_deps()
load("@rules_antlr//antlr:deps.bzl", "antlr_dependencies")
antlr_dependencies()

# Load Bazel
load("@graknlabs_dependencies//builder/bazel:deps.bzl","bazel_common", "bazel_deps", "bazel_toolchain")
bazel_common()
bazel_deps()
bazel_toolchain()

# Load gRPC
load("@graknlabs_dependencies//builder/grpc:deps.bzl", grpc_deps = "deps")
grpc_deps()
load("@com_github_grpc_grpc//bazel:grpc_deps.bzl",
com_github_grpc_grpc_deps = "grpc_deps")
com_github_grpc_grpc_deps()
load("@stackb_rules_proto//java:deps.bzl", "java_grpc_compile")
java_grpc_compile()
load("@stackb_rules_proto//node:deps.bzl", "node_grpc_compile")
node_grpc_compile()

# Load Java
load("@graknlabs_dependencies//builder/java:deps.bzl", java_deps = "deps")
java_deps()
load("@graknlabs_dependencies//library/maven:rules.bzl", "maven")

# Load Kotlin
load("@graknlabs_dependencies//builder/kotlin:deps.bzl", kotlin_deps = "deps")
kotlin_deps()
load("@io_bazel_rules_kotlin//kotlin:kotlin.bzl", "kotlin_repositories", "kt_register_toolchains")
kotlin_repositories()
kt_register_toolchains()

# Load NodeJS
load("@graknlabs_dependencies//builder/nodejs:deps.bzl", nodejs_deps = "deps")
nodejs_deps()
load("@build_bazel_rules_nodejs//:defs.bzl", "node_repositories", "yarn_install")

# Load Python
load("@graknlabs_dependencies//builder/python:deps.bzl", python_deps = "deps")
python_deps()
load("@rules_python//python:pip.bzl", "pip_repositories", "pip3_import")
pip_repositories()
pip3_import(
    name = "graknlabs_dependencies_ci_pip",
    requirements = "@graknlabs_dependencies//tool:requirements.txt",
)
load("@graknlabs_dependencies_ci_pip//:requirements.bzl",
graknlabs_dependencies_ci_pip_install = "pip_install")
graknlabs_dependencies_ci_pip_install()

# Load Checkstyle
load("@graknlabs_dependencies//tool/checkstyle:deps.bzl", checkstyle_deps = "deps")
checkstyle_deps()

# Load Unused Deps
load("@graknlabs_dependencies//tool/unuseddeps:deps.bzl", unuseddeps_deps = "deps")
unuseddeps_deps()

#####################################################################
# Load @graknlabs_bazel_distribution (from @graknlabs_dependencies) #
#####################################################################
load("@graknlabs_dependencies//distribution:deps.bzl", distribution_deps = "deps")
distribution_deps()

pip3_import(
    name = "graknlabs_bazel_distribution_pip",
    requirements = "@graknlabs_bazel_distribution//pip:requirements.txt",
)
load("@graknlabs_bazel_distribution_pip//:requirements.bzl",
graknlabs_bazel_distribution_pip_install = "pip_install")
graknlabs_bazel_distribution_pip_install()

###############################
# Load @graknlabs_client_java #
###############################
load("//dependencies/graknlabs:repositories.bzl", "graknlabs_client_java")
graknlabs_client_java()
load("@graknlabs_client_java//dependencies/maven:artifacts.bzl", graknlabs_client_java_artifacts = "artifacts")

##########################
# Load @graknlabs_common #
##########################
load("//dependencies/graknlabs:repositories.bzl", "graknlabs_common")
graknlabs_common()

#######################################################
# Load @graknlabs_graql (from @graknlabs_client_java) #
#######################################################
load("@graknlabs_client_java//dependencies/graknlabs:repositories.bzl", "graknlabs_graql")
graknlabs_graql()
load("@graknlabs_graql//dependencies/maven:artifacts.bzl", graknlabs_graql_artifacts = "artifacts")

##########################################################
# Load @graknlabs_protocol (from @graknlabs_client_java) #
##########################################################
load("@graknlabs_client_java//dependencies/graknlabs:repositories.bzl", "graknlabs_protocol")
graknlabs_protocol()
load("@graknlabs_protocol//dependencies/maven:artifacts.bzl", graknlabs_protocol_artifacts = "artifacts")

###############################################################
# Load @graknlabs_grabl_tracing (from @graknlabs_client_java) #
###############################################################
load("@graknlabs_client_java//dependencies/graknlabs:repositories.bzl", "graknlabs_grabl_tracing")
graknlabs_grabl_tracing()
load("@graknlabs_grabl_tracing//dependencies/maven:artifacts.bzl", graknlabs_grabl_tracing_artifacts = "artifacts")


#################################
# Load @graknlabs_client_python #
#################################
load("//dependencies/graknlabs:repositories.bzl", "graknlabs_client_python")
graknlabs_client_python()

###################################
# Load Client Python Dependencies #
###################################
pip3_import(
    name = "graknlabs_client_python_pip",
    requirements = "@graknlabs_client_python//:requirements.txt",
)

load("@graknlabs_client_python_pip//:requirements.bzl",
graknlabs_client_python_pip_install = "pip_install")
graknlabs_client_python_pip_install()

###############
# Load @maven #
###############
load("//dependencies/maven:artifacts.bzl", "artifacts")
maven(
    artifacts +
    graknlabs_graql_artifacts +
    graknlabs_protocol_artifacts +
    graknlabs_client_java_artifacts +
    graknlabs_grabl_tracing_artifacts
)

##########################################
# Load nodejs examples test dependencies #
##########################################
node_repositories(package_json = ["//test/example/nodejs:package.json"])
yarn_install(
    name = "npm",
    package_json = "//test/example/nodejs:package.json",
    yarn_lock = "//test/example/nodejs:yarn.lock",
)
load("@npm//:install_bazel_dependencies.bzl", "install_bazel_dependencies")
install_bazel_dependencies()

##########################################
# Load python examples test dependencies #
##########################################
pip3_import(
    name = "test_example_pip",
    requirements = "//test/example/python:requirements.txt",
)
load("@test_example_pip//:requirements.bzl",
test_example_pip_install = "pip_install")
test_example_pip_install()
pip3_import(
    name = "test_links_pip",
    requirements = "//test/links:requirements.txt",
)

load("@test_links_pip//:requirements.bzl",
test_links_pip_install = "pip_install")
test_links_pip_install()

#######################################
# Load @graknlabs_grakn_core_artifact #
#######################################
load("//dependencies/graknlabs:artifacts.bzl", "graknlabs_grakn_core_artifact")
graknlabs_grakn_core_artifact()
