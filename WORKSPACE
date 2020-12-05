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

workspace(
    name = "graknlabs_docs",
    managed_directories = {"@npm": ["test/example/nodejs/node_modules"]}
)

################################
# Load @graknlabs_dependencies #
################################

load("//dependencies/graknlabs:repositories.bzl", "graknlabs_dependencies")
graknlabs_dependencies()

# Load //builder/bazel for RBE
load("@graknlabs_dependencies//builder/bazel:deps.bzl", "bazel_toolchain")
bazel_toolchain()

# Load //builder/antlr
load("@graknlabs_dependencies//builder/antlr:deps.bzl", antlr_deps = "deps")
antlr_deps()
load("@rules_antlr//antlr:deps.bzl", "antlr_dependencies")
antlr_dependencies()

# Load //builder/grpc
load("@graknlabs_dependencies//builder/grpc:deps.bzl", grpc_deps = "deps")
grpc_deps()
load("@com_github_grpc_grpc//bazel:grpc_deps.bzl",
com_github_grpc_grpc_deps = "grpc_deps")
com_github_grpc_grpc_deps()
load("@stackb_rules_proto//java:deps.bzl", "java_grpc_compile")
java_grpc_compile()
load("@stackb_rules_proto//node:deps.bzl", "node_grpc_compile")
node_grpc_compile()

# Load //builder/java
load("@graknlabs_dependencies//builder/java:deps.bzl", java_deps = "deps")
java_deps()

# Load //builder/kotlin
load("@graknlabs_dependencies//builder/kotlin:deps.bzl", kotlin_deps = "deps")
kotlin_deps()
load("@io_bazel_rules_kotlin//kotlin:kotlin.bzl", "kotlin_repositories", "kt_register_toolchains")
kotlin_repositories()
kt_register_toolchains()

# Load //builder/nodejs
load("@graknlabs_dependencies//builder/nodejs:deps.bzl", nodejs_deps = "deps")
nodejs_deps()
load("@build_bazel_rules_nodejs//:index.bzl", "node_repositories", "yarn_install")

# Load //builder/python
load("@graknlabs_dependencies//builder/python:deps.bzl", python_deps = "deps")
python_deps()
load("@rules_python//python:pip.bzl", "pip_repositories", "pip3_import")
pip_repositories()

# Load //tool/common
load("@graknlabs_dependencies//tool/common:deps.bzl", "graknlabs_dependencies_ci_pip",
graknlabs_dependencies_tool_maven_artifacts = "maven_artifacts")
graknlabs_dependencies_ci_pip()
load("@graknlabs_dependencies_ci_pip//:requirements.bzl", "pip_install")
pip_install()

# Load //tool/checkstyle
load("@graknlabs_dependencies//tool/checkstyle:deps.bzl", checkstyle_deps = "deps")
checkstyle_deps()

# Load //tool/unuseddeps
load("@graknlabs_dependencies//tool/unuseddeps:deps.bzl", unuseddeps_deps = "deps")
unuseddeps_deps()

# Load //tool/sonarcloud
load("@graknlabs_dependencies//tool/sonarcloud:deps.bzl", "sonarcloud_dependencies")
sonarcloud_dependencies()

######################################
# Load @graknlabs_bazel_distribution #
######################################

load("@graknlabs_dependencies//distribution:deps.bzl", "graknlabs_bazel_distribution")
graknlabs_bazel_distribution()

# Load //common
load("@graknlabs_bazel_distribution//common:deps.bzl", "rules_pkg")
rules_pkg()
load("@rules_pkg//:deps.bzl", "rules_pkg_dependencies")
rules_pkg_dependencies()

# Load //pip
load("@graknlabs_bazel_distribution//pip:deps.bzl", pip_deps = "deps")
pip_deps()
load("@graknlabs_bazel_distribution_pip//:requirements.bzl", graknlabs_bazel_distribution_pip_install = "pip_install")
graknlabs_bazel_distribution_pip_install()

################################
# Load @graknlabs dependencies #
################################

load("//dependencies/graknlabs:repositories.bzl", "graknlabs_common",  "graknlabs_client_python", "graknlabs_client_java")
graknlabs_common()
graknlabs_client_python()
graknlabs_client_java()
load("@graknlabs_client_java//dependencies/graknlabs:repositories.bzl", "graknlabs_graql", "graknlabs_protocol", "graknlabs_grabl_tracing")
graknlabs_graql()
graknlabs_protocol()
graknlabs_grabl_tracing()

# load artifacts
load("//dependencies/graknlabs:artifacts.bzl", "graknlabs_grakn_core_artifacts")
graknlabs_grakn_core_artifacts()

# load maven dependencies
load("@graknlabs_client_java//dependencies/maven:artifacts.bzl", graknlabs_client_java_artifacts = "artifacts")
load("@graknlabs_graql//dependencies/maven:artifacts.bzl", graknlabs_graql_artifacts = "artifacts")
load("@graknlabs_grabl_tracing//dependencies/maven:artifacts.bzl", graknlabs_grabl_tracing_artifacts = "artifacts")
load("//dependencies/maven:artifacts.bzl", graknlabs_docs_artifacs = "artifacts")

# load client-python dependencies
pip3_import(
    name = "graknlabs_client_python_pip",
    requirements = "@graknlabs_client_python//:requirements.txt",
)
load("@graknlabs_client_python_pip//:requirements.bzl",
graknlabs_client_python_pip_install = "pip_install")
graknlabs_client_python_pip_install()

# for Node documentation
yarn_install(
    name = "npm",
    package_json = "//test/example/nodejs:package.json",
    yarn_lock = "//test/example/nodejs:yarn.lock",
)

# for Python documentation
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

############################
# Load @maven dependencies #
############################

load("@graknlabs_dependencies//library/maven:rules.bzl", "maven")
maven(
    graknlabs_dependencies_tool_maven_artifacts +
    graknlabs_grabl_tracing_artifacts +
    graknlabs_graql_artifacts +
    graknlabs_client_java_artifacts +
    graknlabs_docs_artifacs
)

###############################
# Create @graknlabs_docs_refs #
###############################

load("@graknlabs_bazel_distribution//common:rules.bzl", "workspace_refs")
workspace_refs(
    name = "graknlabs_docs_workspace_refs"
)
