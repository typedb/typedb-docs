workspace( name = "docs" )

###############################################################
#                   common bazel imports                      #
###############################################################
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_jar")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

###############################################################
#                        Load Build Tools                     #
###############################################################
# Load additional build tools, such bazel-deps and unused-deps
load("//dependencies/tools:dependencies.bzl", "tools_dependencies")
tools_dependencies()

load("//dependencies/maven:dependencies.bzl", maven_dependencies_for_build = "maven_dependencies")
maven_dependencies_for_build()

###############################################################
#               grakn + transitive dependencies               #
###############################################################
git_repository(
    name = "graknlabs_grakn",
    remote = "https://github.com/graknlabs/grakn",
    commit = '05b13d948e5e50faeb73af6e3be65fabcaaaf689' # grakn-dependency: do not remove this comment. this is used by the auto-update script
)

load("@graknlabs_grakn//dependencies/pip:dependencies.bzl", "python_dependencies")
python_dependencies()

load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories", "pip_import")
pip_repositories()

load("@graknlabs_grakn//dependencies/compilers:dependencies.bzl", "grpc_dependencies")
grpc_dependencies()

load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", com_github_grpc_grpc_bazel_grpc_deps = "grpc_deps")
com_github_grpc_grpc_bazel_grpc_deps()

load("@stackb_rules_proto//python:deps.bzl", "python_grpc_compile")
python_grpc_compile()


git_repository(
    name="graknlabs_bazel_distribution",
    remote="https://github.com/graknlabs/bazel-distribution",
    commit="df751d03b1fcbb69ed11dd1e7265020144d7233b"
)

pip_import(
    name = "pypi_deployment_dependencies",
    requirements = "@graknlabs_bazel_distribution//pip:requirements.txt",
)
load("@pypi_deployment_dependencies//:requirements.bzl", "pip_install")
pip_install()


# ----- @graknlabs_grakn deps -----
git_repository(
 name="com_github_google_bazel_common",
 remote="https://github.com/graknlabs/bazel-common",
 commit="550f0490798a4e4b6c5ff8cac3b6f5c2a5e81e21",
)

load("@com_github_google_bazel_common//:workspace_defs.bzl", "google_common_workspace_rules")
google_common_workspace_rules()

load("@graknlabs_grakn//dependencies/maven:dependencies.bzl", maven_dependencies_for_build = "maven_dependencies")
maven_dependencies_for_build()

load("@graknlabs_grakn//dependencies/maven:dependencies.bzl", maven_dependencies_for_build = "maven_dependencies")
maven_dependencies_for_build()

# Load ANTLR dependencies for Bazel
load("@graknlabs_grakn//dependencies/compilers:dependencies.bzl", "antlr_dependencies")
antlr_dependencies()

# Load ANTLR dependencies for ANTLR programs
load("@rules_antlr//antlr:deps.bzl", "antlr_dependencies")
antlr_dependencies()

load("@stackb_rules_proto//java:deps.bzl", "java_grpc_compile")
java_grpc_compile()
