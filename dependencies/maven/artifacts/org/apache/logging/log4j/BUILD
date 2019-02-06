java_library(
    name = "log4j-api",
    exports = [
        "//external:jar/org/apache/logging/log4j/log4j-api"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "log4j-core",
    exports = [
        "//external:jar/org/apache/logging/log4j/log4j-core"
    ],
    runtime_deps = [
        ":log4j-api"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "log4j-iostreams",
    exports = [
        "//external:jar/org/apache/logging/log4j/log4j-iostreams"
    ],
    runtime_deps = [
        ":log4j-api"
    ],
    visibility = [
        "//visibility:public"
    ]
)


