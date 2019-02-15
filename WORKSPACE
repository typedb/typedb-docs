workspace( name = "docs" )

###############################################################
#                    common bazel imports                     #
###############################################################
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_jar")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

###############################################################
#                      Load Build Tools                       #
###############################################################
# Load additional build tools, such bazel-deps and unused-deps
load("//dependencies/tools:dependencies.bzl", "tools_dependencies")
tools_dependencies()

load("//dependencies/maven:dependencies.bzl", maven_dependencies_for_build = "maven_dependencies")
maven_dependencies_for_build()

###############################################################
#             grakn core + transitive dependencies            #
###############################################################
git_repository(
    name = "graknlabs_grakn_core",
    remote = "https://github.com/graknlabs/grakn",
    commit = '4a5ccbcee03023d11b4d09134ad344d0cbf14599' # grakn-dependency: do not remove this comment. this is used by the auto-update script
)

load("@graknlabs_grakn_core//dependencies/compilers:dependencies.bzl", "grpc_dependencies")
grpc_dependencies()

load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", com_github_grpc_grpc_bazel_grpc_deps = "grpc_deps")
com_github_grpc_grpc_bazel_grpc_deps()

load("@stackb_rules_proto//python:deps.bzl", "python_grpc_compile")
python_grpc_compile()


# ----- @graknlabs_grakn_core deps -----
git_repository(
 name="com_github_google_bazel_common",
 remote="https://github.com/graknlabs/bazel-common",
 commit="550f0490798a4e4b6c5ff8cac3b6f5c2a5e81e21",
)

load("@com_github_google_bazel_common//:workspace_defs.bzl", "google_common_workspace_rules")
google_common_workspace_rules()

load("@graknlabs_grakn_core//dependencies/maven:dependencies.bzl", maven_dependencies_for_build = "maven_dependencies")
maven_dependencies_for_build()

load("@graknlabs_grakn_core//dependencies/maven:dependencies.bzl", maven_dependencies_for_build = "maven_dependencies")
maven_dependencies_for_build()

# Load ANTLR dependencies for Bazel
load("@graknlabs_grakn_core//dependencies/compilers:dependencies.bzl", "antlr_dependencies")
antlr_dependencies()

# Load ANTLR dependencies for ANTLR programs
load("@rules_antlr//antlr:deps.bzl", "antlr_dependencies")
antlr_dependencies()

load("@stackb_rules_proto//java:deps.bzl", "java_grpc_compile")
java_grpc_compile()

###############################################################
#               client + python dependencies                  #
###############################################################

load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories", "pip_import")
pip_repositories()

# ----- client python + transitive dependencies -----
git_repository(
    name = "graknlabs_client_python",
    remote = "https://github.com/graknlabs/client-python",
    commit = '22c2daf1a148fabaf37b775fcf35dbca5bdd7e67' # grakn-client-python-dependency: do not remove this comment. this is used by the auto-update script
)

pip_import(
    name = "client_python_dependencies",
    requirements = "@graknlabs_client_python//:requirements.txt",
)

load("@client_python_dependencies//:requirements.bzl", "pip_install")
pip_install()

# ----- local python dependencies -----
pip_import(
    name = "pypi_dependencies",
    requirements = "//test/standalone/python:requirements.txt",
)

load("@pypi_dependencies//:requirements.bzl", "pip_install")
pip_install()

# ----- grakn bazel distribution dependencies -----
git_repository(
    name="graknlabs_bazel_distribution",
    remote="https://github.com/graknlabs/bazel-distribution",
    commit="d95bf5376adf7df904938a14ea5c75c3beda82c3"
)

pip_import(
    name = "pypi_deployment_dependencies",
    requirements = "@graknlabs_bazel_distribution//pip:requirements.txt",
)

load("@pypi_deployment_dependencies//:requirements.bzl", "pip_install")
pip_install()