# Do not edit. bazel-deps autogenerates this file from dependencies/maven/dependencies.yaml.
def _jar_artifact_impl(ctx):
    jar_name = "%s.jar" % ctx.name
    ctx.download(
        output=ctx.path("jar/%s" % jar_name),
        url=ctx.attr.urls,
        sha256=ctx.attr.sha256,
        executable=False
    )
    src_name="%s-sources.jar" % ctx.name
    srcjar_attr=""
    has_sources = len(ctx.attr.src_urls) != 0
    if has_sources:
        ctx.download(
            output=ctx.path("jar/%s" % src_name),
            url=ctx.attr.src_urls,
            sha256=ctx.attr.src_sha256,
            executable=False
        )
        srcjar_attr ='\n    srcjar = ":%s",' % src_name

    build_file_contents = """
package(default_visibility = ['//visibility:public'])
java_import(
    name = 'jar',
    tags = ['maven_coordinates={artifact}'],
    jars = ['{jar_name}'],{srcjar_attr}
)
filegroup(
    name = 'file',
    srcs = [
        '{jar_name}',
        '{src_name}'
    ],
    visibility = ['//visibility:public']
)\n""".format(artifact = ctx.attr.artifact, jar_name = jar_name, src_name = src_name, srcjar_attr = srcjar_attr)
    ctx.file(ctx.path("jar/BUILD"), build_file_contents, False)
    return None

jar_artifact = repository_rule(
    attrs = {
        "artifact": attr.string(mandatory = True),
        "sha256": attr.string(mandatory = True),
        "urls": attr.string_list(mandatory = True),
        "src_sha256": attr.string(mandatory = False, default=""),
        "src_urls": attr.string_list(mandatory = False, default=[]),
    },
    implementation = _jar_artifact_impl
)

def jar_artifact_callback(hash):
    src_urls = []
    src_sha256 = ""
    source=hash.get("source", None)
    if source != None:
        src_urls = [source["url"]]
        src_sha256 = source["sha256"]
    jar_artifact(
        artifact = hash["artifact"],
        name = hash["name"],
        urls = [hash["url"]],
        sha256 = hash["sha256"],
        src_urls = src_urls,
        src_sha256 = src_sha256
    )
    native.bind(name = hash["bind"], actual = hash["actual"])


def list_dependencies():
    return [
    {"artifact": "com.google.code.findbugs:jsr305:3.0.0", "lang": "java", "sha1": "5871fb60dc68d67da54a663c3fd636a10a532948", "sha256": "bec0b24dcb23f9670172724826584802b80ae6cbdaba03bdebdef9327b962f6a", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/com/google/code/findbugs/jsr305/3.0.0/jsr305-3.0.0.jar", "source": {"sha1": "936f4430478909ed7b138d42f9ad73c919a87b26", "sha256": "4de55af3c2a78d1df2a14fb5db64b23110f74ea462c5f56db443a96df431fad5", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/com/google/code/findbugs/jsr305/3.0.0/jsr305-3.0.0-sources.jar"} , "name": "com-google-code-findbugs-jsr305", "actual": "@com-google-code-findbugs-jsr305//jar", "bind": "jar/com/google/code/findbugs/jsr305"},
    {"artifact": "com.google.code.gson:gson:2.7", "lang": "java", "sha1": "751f548c85fa49f330cecbb1875893f971b33c4e", "sha256": "2d43eb5ea9e133d2ee2405cc14f5ee08951b8361302fdd93494a3a997b508d32", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/com/google/code/gson/gson/2.7/gson-2.7.jar", "source": {"sha1": "bbb63ca253b483da8ee53a50374593923e3de2e2", "sha256": "2d3220d5d936f0a26258aa3b358160741a4557e046a001251e5799c2db0f0d74", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/com/google/code/gson/gson/2.7/gson-2.7-sources.jar"} , "name": "com-google-code-gson-gson", "actual": "@com-google-code-gson-gson//jar", "bind": "jar/com/google/code/gson/gson"},
    {"artifact": "com.google.errorprone:error_prone_annotations:2.2.0", "lang": "java", "sha1": "88e3c593e9b3586e1c6177f89267da6fc6986f0c", "sha256": "6ebd22ca1b9d8ec06d41de8d64e0596981d9607b42035f9ed374f9de271a481a", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/com/google/errorprone/error_prone_annotations/2.2.0/error_prone_annotations-2.2.0.jar", "source": {"sha1": "a8cd7823aa1dcd2fd6677c0c5988fdde9d1fb0a3", "sha256": "626adccd4894bee72c3f9a0384812240dcc1282fb37a87a3f6cb94924a089496", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/com/google/errorprone/error_prone_annotations/2.2.0/error_prone_annotations-2.2.0-sources.jar"} , "name": "com-google-errorprone-error_prone_annotations", "actual": "@com-google-errorprone-error_prone_annotations//jar", "bind": "jar/com/google/errorprone/error-prone-annotations"},
    {"artifact": "com.google.guava:guava:20.0", "lang": "java", "sha1": "89507701249388e1ed5ddcf8c41f4ce1be7831ef", "sha256": "36a666e3b71ae7f0f0dca23654b67e086e6c93d192f60ba5dfd5519db6c288c8", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/com/google/guava/guava/20.0/guava-20.0.jar", "source": {"sha1": "9c8493c7991464839b612d7547d6c263adf08f75", "sha256": "994be5933199a98e98bd09584da2bb69ed722275f6bed61d83459af88ace5cbd", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/com/google/guava/guava/20.0/guava-20.0-sources.jar"} , "name": "com-google-guava-guava", "actual": "@com-google-guava-guava//jar", "bind": "jar/com/google/guava/guava"},
    {"artifact": "com.google.protobuf:protobuf-java:3.5.1", "lang": "java", "sha1": "8c3492f7662fa1cbf8ca76a0f5eb1146f7725acd", "sha256": "b5e2d91812d183c9f053ffeebcbcda034d4de6679521940a19064714966c2cd4", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/com/google/protobuf/protobuf-java/3.5.1/protobuf-java-3.5.1.jar", "source": {"sha1": "7235a28a13938050e8cd5d9ed5133bebf7a4dca7", "sha256": "3be3115498d543851443bfa725c0c5b28140e363b3b7dec97f4028cd17040fa4", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/com/google/protobuf/protobuf-java/3.5.1/protobuf-java-3.5.1-sources.jar"} , "name": "com-google-protobuf-protobuf-java", "actual": "@com-google-protobuf-protobuf-java//jar", "bind": "jar/com/google/protobuf/protobuf-java"},
    {"artifact": "commons-io:commons-io:2.6", "lang": "java", "sha1": "815893df5f31da2ece4040fe0a12fd44b577afaf", "sha256": "f877d304660ac2a142f3865badfc971dec7ed73c747c7f8d5d2f5139ca736513", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/commons-io/commons-io/2.6/commons-io-2.6.jar", "source": {"sha1": "2566800dc841d9d2c5a0d34d807e45d4107dbbdf", "sha256": "71bc251eb4bd011b60b5ce6adc8f473de10e4851207a40c14434604b288b31bf", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/commons-io/commons-io/2.6/commons-io-2.6-sources.jar"} , "name": "commons-io-commons-io", "actual": "@commons-io-commons-io//jar", "bind": "jar/commons-io/commons-io"},
    {"artifact": "io.grpc:grpc-context:1.15.0", "lang": "java", "sha1": "bdfb1d0c90d83fa998a9f25976a71019aebe7bcc", "sha256": "512e99587fa389d7ba7830d91f1e2f949162814ec077073cd4d6766fa63896f7", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/grpc/grpc-context/1.15.0/grpc-context-1.15.0.jar", "source": {"sha1": "ba18517ab3e41edb72ff74b20e59abb7a7833dee", "sha256": "a8634faeb270a2440368b0d4a908066dee0e9903e471358575c0fa3e39fe9323", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/grpc/grpc-context/1.15.0/grpc-context-1.15.0-sources.jar"} , "name": "io-grpc-grpc-context", "actual": "@io-grpc-grpc-context//jar", "bind": "jar/io/grpc/grpc-context"},
# duplicates in io.grpc:grpc-core fixed to 1.15.0
# - io.grpc:grpc-netty-shaded:1.15.0 wanted version [1.15.0]
# - io.grpc:grpc-stub:1.15.0 wanted version 1.15.0
    {"artifact": "io.grpc:grpc-core:1.15.0", "lang": "java", "sha1": "85863284e3c56a7f7c2cf7a01963c7f4519a5295", "sha256": "dd615ae3c01481e67adf8d346beb4979becc09af78b6662b52cc8395eb2255c0", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/grpc/grpc-core/1.15.0/grpc-core-1.15.0.jar", "source": {"sha1": "bf24e9d931fbfd438a46930848946417ee6b7965", "sha256": "56706d0ebb4d4267242feeee00bb5af517fec4478167e1baf9748681b0ebc161", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/grpc/grpc-core/1.15.0/grpc-core-1.15.0-sources.jar"} , "name": "io-grpc-grpc-core", "actual": "@io-grpc-grpc-core//jar", "bind": "jar/io/grpc/grpc-core"},
    {"artifact": "io.grpc:grpc-netty-shaded:1.15.0", "lang": "java", "sha1": "c1b4c7204cf3628e0e1aa52bd724393dbc647e33", "sha256": "2361fcb57acad8479b6b478aff981cd14747cb4d8f6b67d8810ed54ff6c9d77b", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/grpc/grpc-netty-shaded/1.15.0/grpc-netty-shaded-1.15.0.jar", "source": {"sha1": "b90e45114016d4afe89d665bf1bb8c209f479c1b", "sha256": "c1ac7e9d00916f4d7cb5ab9d670a7d113d932dde712543a399441466a6896218", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/grpc/grpc-netty-shaded/1.15.0/grpc-netty-shaded-1.15.0-sources.jar"} , "name": "io-grpc-grpc-netty-shaded", "actual": "@io-grpc-grpc-netty-shaded//jar", "bind": "jar/io/grpc/grpc-netty-shaded"},
    {"artifact": "io.grpc:grpc-stub:1.15.0", "lang": "java", "sha1": "17ac6d74d9bef3dec6eddbd0772fede89865261c", "sha256": "d3fa20905203778dac4db1d8a1f1230eaa8c0c42e5e4afefc0c74afb48bacbbe", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/grpc/grpc-stub/1.15.0/grpc-stub-1.15.0.jar", "source": {"sha1": "a61e3a69182fe0e43dadacf5ff37864dd5f61833", "sha256": "b713744855c7246d4e6aea33fe5e1a65c3b86209b60d7b871533edf7604daf38", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/grpc/grpc-stub/1.15.0/grpc-stub-1.15.0-sources.jar"} , "name": "io-grpc-grpc-stub", "actual": "@io-grpc-grpc-stub//jar", "bind": "jar/io/grpc/grpc-stub"},
    {"artifact": "io.opencensus:opencensus-api:0.12.3", "lang": "java", "sha1": "743f074095f29aa985517299545e72cc99c87de0", "sha256": "8c1de62cbdaf74b01b969d1ed46c110bca1a5dd147c50a8ab8c5112f42ced802", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/opencensus/opencensus-api/0.12.3/opencensus-api-0.12.3.jar", "source": {"sha1": "09c2dad7aff8b6d139723b9181ba5da3f689213b", "sha256": "67e8b2120737c7dcfc61eef33f75319b1c4e5a2806d3c1a74cab810650ac7a19", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/opencensus/opencensus-api/0.12.3/opencensus-api-0.12.3-sources.jar"} , "name": "io-opencensus-opencensus-api", "actual": "@io-opencensus-opencensus-api//jar", "bind": "jar/io/opencensus/opencensus-api"},
    {"artifact": "io.opencensus:opencensus-contrib-grpc-metrics:0.12.3", "lang": "java", "sha1": "a4c7ff238a91b901c8b459889b6d0d7a9d889b4d", "sha256": "632c1e1463db471b580d35bc4be868facbfbf0a19aa6db4057215d4a68471746", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/opencensus/opencensus-contrib-grpc-metrics/0.12.3/opencensus-contrib-grpc-metrics-0.12.3.jar", "source": {"sha1": "9a7d004b774700837eeebff61230b8662d0e30d1", "sha256": "d54f6611f75432ca0ab13636a613392ae8b7136ba67eb1588fccdb8481f4d665", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/io/opencensus/opencensus-contrib-grpc-metrics/0.12.3/opencensus-contrib-grpc-metrics-0.12.3-sources.jar"} , "name": "io-opencensus-opencensus-contrib-grpc-metrics", "actual": "@io-opencensus-opencensus-contrib-grpc-metrics//jar", "bind": "jar/io/opencensus/opencensus-contrib-grpc-metrics"},
    {"artifact": "org.apache.logging.log4j:log4j-api:2.11.1", "lang": "java", "sha1": "268f0fe4df3eefe052b57c87ec48517d64fb2a10", "sha256": "493b37b5a6c49c4f5fb609b966375e4dc1783df436587584ca1dc7e861d0742b", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-api/2.11.1/log4j-api-2.11.1.jar", "source": {"sha1": "acf35297ef03716fc14e11e2978d7c749ed3f7e5", "sha256": "8843aaa6dcffef0fa6c270e5e579e0a2efeda6bfc153fdee45caa8ec1b4b2e15", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-api/2.11.1/log4j-api-2.11.1-sources.jar"} , "name": "org-apache-logging-log4j-log4j-api", "actual": "@org-apache-logging-log4j-log4j-api//jar", "bind": "jar/org/apache/logging/log4j/log4j-api"},
    {"artifact": "org.apache.logging.log4j:log4j-core:2.11.1", "lang": "java", "sha1": "592a48674c926b01a9a747c7831bcd82a9e6d6e4", "sha256": "a20c34cdac4978b76efcc9d0db66e95600bd807c6a0bd3f5793bcb45d07162ec", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-core/2.11.1/log4j-core-2.11.1.jar", "source": {"sha1": "23bef4ea0494ba9fb9835df0e3e23c6883d8d545", "sha256": "1cfdbe61b869c6df76d09087f3a248c5eb29fc0ccc242333e24a5a79795e30a5", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-core/2.11.1/log4j-core-2.11.1-sources.jar"} , "name": "org-apache-logging-log4j-log4j-core", "actual": "@org-apache-logging-log4j-log4j-core//jar", "bind": "jar/org/apache/logging/log4j/log4j-core"},
    {"artifact": "org.apache.logging.log4j:log4j-iostreams:2.11.1", "lang": "java", "sha1": "54219892aca8fe8b91d5c0e4e74d78b5ea613b1d", "sha256": "69298a70c7ab0d3ba9f9ff84d627d9767b308a70a338e2c205ea8d6771ad9210", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-iostreams/2.11.1/log4j-iostreams-2.11.1.jar", "source": {"sha1": "65f41edc99bff8cf3d3aeddb9555487e0c73a466", "sha256": "4716747b4b55f0f8ee4dc9a74014f2c2f7f1abd04592c14785e93ed0cfdea114", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-iostreams/2.11.1/log4j-iostreams-2.11.1-sources.jar"} , "name": "org-apache-logging-log4j-log4j-iostreams", "actual": "@org-apache-logging-log4j-log4j-iostreams//jar", "bind": "jar/org/apache/logging/log4j/log4j-iostreams"},
    {"artifact": "org.codehaus.mojo:animal-sniffer-annotations:1.17", "lang": "java", "sha1": "f97ce6decaea32b36101e37979f8b647f00681fb", "sha256": "92654f493ecfec52082e76354f0ebf87648dc3d5cec2e3c3cdb947c016747a53", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/codehaus/mojo/animal-sniffer-annotations/1.17/animal-sniffer-annotations-1.17.jar", "source": {"sha1": "8fb5b5ad9c9723951b9fccaba5bb657fa6064868", "sha256": "2571474a676f775a8cdd15fb9b1da20c4c121ed7f42a5d93fca0e7b6e2015b40", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/codehaus/mojo/animal-sniffer-annotations/1.17/animal-sniffer-annotations-1.17-sources.jar"} , "name": "org-codehaus-mojo-animal-sniffer-annotations", "actual": "@org-codehaus-mojo-animal-sniffer-annotations//jar", "bind": "jar/org/codehaus/mojo/animal-sniffer-annotations"},
    {"artifact": "org.rocksdb:rocksdbjni:5.14.2", "lang": "java", "sha1": "a6087318fab540ba0b4c6ff68475ffbedc0b3d10", "sha256": "34b7e45d18bca957e38cad0c3269dd36c9df81313f2ff41171ec2a96a3736c7f", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/rocksdb/rocksdbjni/5.14.2/rocksdbjni-5.14.2.jar", "source": {"sha1": "ac0184f4618db881be0a9aeac98535b13f36a967", "sha256": "8fdf11a3b7b19201459cbac18d7a693331a992c159f042ab6ece7e843f6ff59b", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/rocksdb/rocksdbjni/5.14.2/rocksdbjni-5.14.2-sources.jar"} , "name": "org-rocksdb-rocksdbjni", "actual": "@org-rocksdb-rocksdbjni//jar", "bind": "jar/org/rocksdb/rocksdbjni"},
    {"artifact": "org.slf4j:slf4j-api:1.7.2", "lang": "java", "sha1": "0081d61b7f33ebeab314e07de0cc596f8e858d97", "sha256": "3bae789b401333b2a1d1603b7fa573e19908628191707203f6eb708cdee2c052", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.7.2/slf4j-api-1.7.2.jar", "source": {"sha1": "58d38f68d4a867d4552ae27960bb348d7eaa1297", "sha256": "c2660815ef375224bfeb347a0da55b9e80431563d5988196869d4a50cd792f15", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.7.2/slf4j-api-1.7.2-sources.jar"} , "name": "org-slf4j-slf4j-api", "actual": "@org-slf4j-slf4j-api//jar", "bind": "jar/org/slf4j/slf4j-api"},
    {"artifact": "org.zeroturnaround:zt-exec:1.10", "lang": "java", "sha1": "6bec7a4af16208c7542d2c280207871c7b976483", "sha256": "1f8b1bca6d0f9b9ec7f9bc8fca3b45e42039bb4ea3cdd20614104085e809ec71", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/zeroturnaround/zt-exec/1.10/zt-exec-1.10.jar", "source": {"sha1": "7de1aaa7d5ee303c72001c9a65b49516bdc89904", "sha256": "262393d6a90a078a3a8a3c6c64cbf18108bd97029df7704ea29c99b4b733fb7c", "repository": "https://repo.maven.apache.org/maven2/", "url": "https://repo.maven.apache.org/maven2/org/zeroturnaround/zt-exec/1.10/zt-exec-1.10-sources.jar"} , "name": "org-zeroturnaround-zt-exec", "actual": "@org-zeroturnaround-zt-exec//jar", "bind": "jar/org/zeroturnaround/zt-exec"},
    ]

def maven_dependencies(callback = jar_artifact_callback):
    for hash in list_dependencies():
        callback(hash)
