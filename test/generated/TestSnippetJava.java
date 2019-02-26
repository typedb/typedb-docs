
package generated;

import grakn.core.client.GraknClient;
import grakn.core.rule.GraknTestServer;
import grakn.core.server.Transaction;

import graql.lang.Graql;
import static graql.lang.Graql.*;
import graql.lang.query.GraqlQuery;
import graql.lang.query.GraqlCompute;
import graql.lang.query.GraqlDefine;
import graql.lang.query.GraqlUndefine;
import graql.lang.query.GraqlGet;
import graql.lang.query.GraqlDelete;
import graql.lang.query.GraqlInsert;
import graql.lang.query.GraqlCompute.Argument;
import static graql.lang.query.GraqlCompute.Argument.*;
import static graql.lang.Graql.Token.Compute.Algorithm.*;

import org.junit.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDate;

public class TestSnippetJava {
    @ClassRule
    public static final GraknTestServer server = new GraknTestServer(
            Paths.get("test/grakn-test-server/conf/grakn.properties"),
            Paths.get("test/grakn-test-server/conf/cassandra-embedded.yaml")
    );

    static GraknClient client;
    static GraknClient.Session session ;
    GraknClient.Transaction transaction;


    @BeforeClass
    public static void loadSocialNetwork() {
        client = new GraknClient(server.grpcUri().toString());
        session = client.session("social_network");
        GraknClient.Transaction transaction = session.transaction(Transaction.Type.WRITE);

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.execute((GraqlQuery) parse(query));
            transaction.commit();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Before
    public void openTransaction(){
        transaction = session.transaction(Transaction.Type.WRITE);
    }

    @After
    public void abortTransaction(){
        transaction.abort();
    }

    @AfterClass
    public static void closeSession() {
        session.close();
    }


    @Test
    public void test_0() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("person").sub("entity")
        );


    }

    @Test
    public void test_1() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("person").sub("entity").has("full-name").has("nickname").has("gender")
        );


    }

    @Test
    public void test_2() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("person").sub("entity").key("email")
        );


    }

    @Test
    public void test_3() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("person").sub("entity").plays("employee"),
                type("organisation").sub("entity").plays("employer")
        );


    }

    @Test
    public void test_4() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("post").sub("entity").plays("replied-to").plays("tagged-in").plays("reacted-to"),
                type("comment").sub("post").has("content").plays("attached-to"),
                type("media").sub("post").has("caption").has("file").plays("attached"),
                type("video").sub("media"),
                type("photo").sub("media")
        );


    }

    @Test
    public void test_5() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("post").sub("entity").isAbstract(),
                type("media").sub("post").isAbstract()
        );


    }

    @Test
    public void test_6() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("employment").sub("relationship").relates("employee").relates("employer")
        );


    }

    @Test
    public void test_7() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("friendship").sub("relationship").relates("friend").plays("requested-friendship"),
                type("friend-request").sub("relationship").relates("requested-friendship").relates("friendship-requester").relates("friendship-respondent"),
                type("person").sub("entity").plays("friend").plays("friendship-requester").plays("friendship-respondent")
        );


    }

    @Test
    public void test_8() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("reaction").sub("relationship").relates("reacted-emotion").relates("reacted-to").relates("reacted-by"),
                type("emotion").sub("attribute").datatype("string").plays("reacted-emotion"),
                type("post").sub("entity").plays("reacted-to"),
                type("person").sub("entity").plays("reacted-by")
        );


    }

    @Test
    public void test_9() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("friend-request").sub("relationship").has("approved-date").relates("requested-friendship").relates("friendship-requester").relates("friendship-respondent")
        );


    }

    @Test
    public void test_10() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("employment").sub("relationship").key("reference-id").relates("employer").relates("employee")
        );


    }

    @Test
    public void test_11() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("location-of-everything").sub("relationship").relates("located-subject").relates("subject-location"),
                type("located-birth").sub("located-subject"),
                type("birth-location").sub("subject-location"),
                type("location-of-birth").sub("location-of-everything").relates("located-birth").relates("birth-location"),
                type("located-residence").sub("located-subject"),
                type("residence").sub("subject-location")
        );


    }

    @Test
    public void test_12() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("location-of-everything").sub("relationship").isAbstract().relates("located-subject").relates("subject-location")
        );


    }

    @Test
    public void test_13() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("name").sub("attribute").datatype("string")
        );


    }

    @Test
    public void test_14() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("start-date").sub("attribute").datatype("date"),
                type("residency").sub("relationship").has("start-date"),
                type("travel").sub("relationship").has("start-date")
        );


    }

    @Test
    public void test_15() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("phone-number").sub("attribute").datatype("string"),
                type("person").sub("entity").has("phone-number")
        );


    }

    @Test
    public void test_16() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("emotion").sub("attribute").datatype("string").regex("[like, love, funny, shocking, sad, angry]")
        );


    }

    @Test
    public void test_17() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("content").sub("attribute").datatype("string").has("language"),
                type("language").sub("attribute").datatype("string")
        );


    }

    @Test
    public void test_18() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("language").sub("attribute").datatype("string").plays("spoken"),
                type("person").sub("entity").plays("speaker"),
                type("speaking-of-language").sub("relationship").relates("speaker").relates("spoken")
        );

    }

    @Test
    public void test_19() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("event-date").sub("attribute").datatype("date"),
                type("birth-date").sub("event-date"),
                type("start-date").sub("event-date"),
                type("end-date").sub("event-date")
        );


    }

    @Test
    public void test_20() {
        // 09-schema/01-concepts.md
        GraqlDefine query = Graql.define(
                type("event-date").sub("attribute").datatype("date")
        );


    }

    @Test
    public void test_21() {
        // 09-schema/01-concepts.md
        GraqlUndefine query = Graql.undefine(
                type("person").has("nickname")
        );


    }

    @Test
    public void test_22() {
        // 09-schema/01-concepts.md
        GraqlUndefine query = Graql.undefine(
                type("speaking-of-language").relates("speaker").relates("spoken"),
                type("person").plays("speaker"),
                type("language").plays("spoken"),
                type("speaker").sub("role"),
                type("spoken").sub("role"),
                type("speaking-of-language").sub("relationship")
        );


    }

    @Test
    public void test_23() {
        // 09-schema/03-rules.md
        GraqlDefine query = Graql.define(
                type("people-with-same-parents-are-siblings").sub("rule").when(
                        and(
                                var().rel("mother", "m").rel("x").isa("parentship"),
                                var().rel("mother", "m").rel("y").isa("parentship"),
                                var().rel("father", "f").rel("x").isa("parentship"),
                                var().rel("father", "f").rel("y").isa("parentship"),
                                var("x").neq("y")
                        )
                ).then(
                        var().isa("siblings").rel("x").rel("y")
                )
        );


    }

    @Test
    public void test_24() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                Graql.var("p").isa("person")
        ).get();


    }

    @Test
    public void test_25() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("p").isa("person").has("full-name", var("n"))
        ).get();


    }

    @Test
    public void test_26() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("emp").isa("employment").rel("employer", "x").rel("employee", "y")
        ).get();


    }

    @Test
    public void test_27() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("emp").isa("employment").rel("employer", "x").rel("employee", "y").has("reference-id", var("ref"))
        ).get();


    }

    @Test
    public void test_28() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var().isa("employment").rel("employer", "x").rel("employee", "y")
        ).get();


    }

    @Test
    public void test_29() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("fr").isa("friendship").rel("x").rel("y")
        ).get();


    }

    @Test
    public void test_30() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("x").val("like")
        ).get();


    }

    @Test
    public void test_31() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("x").isa("nickname").val("Mitzi")
        ).get();


    }

    @Test
    public void test_32() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("phone-number").contains("+44")
        ).get();


    }

    @Test
    public void test_33() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("phone-number").regex("(Miriam Morton|Solomon Tran)")
        ).get();


    }

    @Test
    public void test_34() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("p").isa("person").has("nickname", var("nn")).has("full-name", var("fn"))
        ).get();


    }

    @Test
    public void test_35() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("p").isa("person").has("nickname", "Mitzi").has("phone-number", Graql.contains("+44"))
        ).get();


    }

    @Test
    public void test_36() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("p").isa("person").has("nickname", "Mitzi").has("phone-number", var("pn")),
                var("pn").contains("+44")
        ).get();


    }

    @Test
    public void test_37() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("p").isa("person").has("full-name", var("fn")),
                or(
                        var("fn").contains("Miriam"),
                        var("fn").contains("Solomon")
                )
        ).get();


    }

    @Test
    public void test_38() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("rr").isaX("romantic-relationship")
        ).get();


    }

    @Test
    public void test_39() {
        // 10-query/01-match-clause.md
        GraqlGet query_a = Graql.match(
                var("x").sub("thing")
        ).get();

        GraqlGet query_b = Graql.match(
                var("x").sub("attribute")
        ).get();

        GraqlGet query_c = Graql.match(
                var("x").sub("entity")
        ).get();

        GraqlGet query_d = Graql.match(
                var("x").sub("role")
        ).get();

        GraqlGet query_e = Graql.match(
                var("x").sub("relationship")
        ).get();


    }

    @Test
    public void test_40() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                type("employment").relates(var("x"))
        ).get();


    }

    @Test
    public void test_41() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                type("location-of-office").relates(var("x")),
                var("x").sub("located-subject")
        ).get();


    }

    @Test
    public void test_42() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("x").plays("employee")
        ).get();


    }

    @Test
    public void test_43() {
        // 10-query/01-match-clause.md
        GraqlGet query = Graql.match(
                var("x").has("title")
        ).get();


    }

    @Test
    public void test_44() {
        // 10-query/02-get-query.md
        GraqlGet query = Graql.match(
                var("fr").isa("friendship").rel("x").rel("y"),
                var("x").isa("person").has("full-name", var("x-fn")),
                var("x-fn").contains("Miriam"),
                var("y").isa("person").has("full-name", var("y-fn")).has("phone-number", var("y-pn"))
        ).get("x-fn", "y-fn", "y-pn");


    }

    @Test
    public void test_45() {
        // 10-query/03-insert-query.md
        GraqlInsert query = Graql.insert(
                var("p").isa("person").has("full-name", "John Parkson").has("email", "john.parkson@gmail.com").has("phone-number", "+44-1234-567890")
        );


    }

    @Test
    public void test_46() {
        // 10-query/03-insert-query.md
        GraqlInsert query = Graql.insert(
                var("x").isa("emotion").val("like")
        );


    }

    @Test
    public void test_47() {
        // 10-query/03-insert-query.md
        GraqlInsert query = Graql.match(
                var("org").isa("organisation").has("name", "Facelook"),
                var("p").isa("person").has("email", "tanya.arnold@gmail.com")
        ).insert(
                var("emp").isa("employment").rel("employer", "org").rel("employee", "p").has("reference-id", "WGFTSH")
        );


    }

    @Test
    public void test_48() {
        // 10-query/04-delete-query.md
        GraqlDelete query = Graql.match(
                var("p").isa("person").has("email", "raphael.santos@gmail.com")
        ).delete("p");


    }

    @Test
    public void test_49() {
        // 10-query/04-delete-query.md
        GraqlDelete query = Graql.match(
                var("org").isa("organisation").has("name", "Pharos"),
                var("emp").isa("employment").rel("employer", "org").rel("employee", "p")
        ).delete("emp");


    }

    @Test
    public void test_50() {
        // 10-query/04-delete-query.md
        GraqlDelete query = Graql.match(
                var("t").isa("travel").has("start-date", var("st"), var("r")),
                var("st").val(LocalDate.of(2013, 12, 22).atStartOfDay())
        ).delete("r");


    }

    @Test
    public void test_51() {
        // 10-query/05-updating-data.md
        GraqlDelete delete_query = Graql.match(
                var("org").isa("organisation").has("name", "Medicely").has("registration-number", var("rn"), var("r"))
        ).delete("r");

        GraqlInsert insert_query = Graql.match(
                var("org").isa("organisation").has("name", "Medicely")
        ).insert(
                var("org").has("registration-number", "81726354")
        );


    }

    @Test
    public void test_52() {
        // 10-query/05-updating-data.md
        GraqlInsert insert_query = Graql.match(
                var("m").isa("media").has("caption", var("c")),
                var("c").contains("inappropriate word")
        ).insert(
                var("m").has("caption", "deleted")
        );

        GraqlDelete delete_query = Graql.match(
                var("c").isa("caption").contains("inappropriate word")
        ).delete("c");


    }

    @Test
    public void test_53() {
        // 10-query/05-updating-data.md
        GraqlInsert insert_query = Graql.match(
                var("p").isa("person").has("name", "Amabo"),
                var("org").isa("organisation").has("name", "Wieth Souhe")
        ).insert(
                var("emp").isa("employment").rel("employer", var("org")).rel("employee", var("p"))
        );

        GraqlDelete delete_query = Graql.match(
                var("p").isa("person").has("name", "Prumt"),
                var("org").isa("organisation").has("name", "Wieth Souhe"),
                var("emp").isa("employment").rel("employer", var("org")).rel("employee", var("p"))
        ).delete("emp");


    }

    @Test
    public void test_54() {
        // 10-query/06-aggregate-query.md
        GraqlGet.Aggregate query = Graql.match(
                var("sce").isa("school-course-enrollment").has("score", var("sco")),
                var("sco").gt(7.0)
        ).get().count();


    }

    @Test
    public void test_55() {
        // 10-query/06-aggregate-query.md
        GraqlGet.Aggregate query = Graql.match(
                var("org").isa("organisation").has("name", var("orn")),
                var("orn").val("Medicely"),
                var().rel("org").isa("employment").has("salary", var("sal"))
        ).get("sal").sum("sal");


    }

    @Test
    public void test_56() {
        // 10-query/06-aggregate-query.md
        GraqlGet.Aggregate query = Graql.match(
                var("sch").isa("school").has("ranking", var("ran"))
        ).get("ran").max("ran");


    }

    @Test
    public void test_57() {
        // 10-query/06-aggregate-query.md
        GraqlGet.Aggregate query = Graql.match(
                var().rel(var("per")).isa("marriage"),
                var().rel(var("per")).isa("employment").has("salary", var("sal"))
        ).get("sal").min("sal");


    }

    @Test
    public void test_58() {
        // 10-query/06-aggregate-query.md
        GraqlGet.Aggregate query = Graql.match(
                var("emp").isa("employment").has("salary", var("sal"))
        ).get("sal").mean("sal");


    }

    @Test
    public void test_59() {
        // 10-query/06-aggregate-query.md
        GraqlGet.Aggregate query = Graql.match(
                var("org").isa("organisation").has("name", var("orn")),
                var("orn").val("Facelook"),
                var().rel("employer", var("org")).rel("employee", var("per")).isa("employment"),
                var().rel(var("per")).isa("school-course-enrollment").has("score", var("sco"))
        ).get("sco").median("sco");


    }

    @Test
    public void test_60() {
        // 10-query/06-aggregate-query.md
        GraqlGet.Group query = Graql.match(
                var("per").isa("person"),
                var("scc").isa("school-course").has("title", var("tit")),
                var().rel("student", var("per")).rel("enrolled-course", var("scc")).isa("school-course-enrollment")
        ).get().group("tit");


    }

    @Test
    public void test_61() {
        // 10-query/06-aggregate-query.md
        GraqlGet.Group.Aggregate query = Graql.match(
                var("per").isa("person"),
                var("scc").isa("school-course").has("title", var("tit")),
                var().rel("student", var("per")).rel("enrolled-course", var("scc")).isa("school-course-enrollment")
        ).get().group("tit").count();


    }

    @Test
    public void test_62() {
        // 10-query/07-compute-query.md
        GraqlCompute.Statistics query = Graql.compute().count().in("person");


    }

    @Test
    public void test_63() {
        // 10-query/07-compute-query.md
        GraqlCompute.Statistics query = Graql.compute().sum().of("salary").in("employment");


    }

    @Test
    public void test_64() {
        // 10-query/07-compute-query.md
        GraqlCompute.Statistics query = Graql.compute().max().of("score").in("school-course-enrollment");


    }

    @Test
    public void test_65() {
        // 10-query/07-compute-query.md
        GraqlCompute.Statistics query = Graql.compute().min().of("ranking").in("school");


    }

    @Test
    public void test_66() {
        // 10-query/07-compute-query.md
        GraqlCompute.Statistics query = Graql.compute().mean().of("salary").in("employment");


    }

    @Test
    public void test_67() {
        // 10-query/07-compute-query.md
        GraqlCompute.Statistics query = Graql.compute().median().of("score").in("school-course-enrollment");


    }

    @Test
    public void test_68() {
        // 10-query/07-compute-query.md
        GraqlCompute.Statistics query = Graql.compute().std().of("salary").in("employment");


    }

    @Test
    public void test_69() {
        // 10-query/07-compute-query.md
        GraqlCompute.Path query = Graql.compute().path().from("V229424").to("v446496");


    }

    @Test
    public void test_70() {
        // 10-query/07-compute-query.md
        GraqlCompute.Path query = Graql.compute().path().from("V229424").to("v446496").in("person","friendship");


    }

    @Test
    public void test_71() {
        // 10-query/07-compute-query.md
        GraqlCompute.Centrality query = Graql.compute().centrality().using(DEGREE);


    }

    @Test
    public void test_72() {
        // 10-query/07-compute-query.md
        GraqlCompute.Centrality query = Graql.compute().centrality().in("organisation", "person", "employment").using(DEGREE);


    }

    @Test
    public void test_73() {
        // 10-query/07-compute-query.md
        GraqlCompute.Centrality query = Graql.compute().centrality().of("organisation").in("organisation", "person", "employment").using(DEGREE);


    }

    @Test
    public void test_74() {
        // 10-query/07-compute-query.md
        GraqlCompute.Centrality query = Graql.compute().centrality().using(K_CORE);


    }

    @Test
    public void test_75() {
        // 10-query/07-compute-query.md
        GraqlCompute.Centrality query = Graql.compute().centrality().using(K_CORE).where(min_k(5));


    }

    @Test
    public void test_76() {
        // 10-query/07-compute-query.md
        GraqlCompute.Cluster query = Graql.compute().cluster().in("person", "employment", "organisation").using(CONNECTED_COMPONENT);


    }

    @Test
    public void test_77() {
        // 10-query/07-compute-query.md
        GraqlCompute.Cluster query = Graql.compute().cluster().in("person", "employment", "organisation").using(CONNECTED_COMPONENT).where(Argument.contains("V12488"));


    }

    @Test
    public void test_78() {
        // 10-query/07-compute-query.md
        GraqlCompute.Cluster query = Graql.compute().cluster().in("person", "friendship").using(K_CORE);


    }

    @Test
    public void test_79() {
        // 10-query/07-compute-query.md
        GraqlCompute.Cluster query = Graql.compute().cluster().in("person", "friendship").using(K_CORE).where(k(5));


    }

}
