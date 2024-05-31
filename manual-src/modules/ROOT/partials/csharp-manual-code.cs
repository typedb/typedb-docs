// tag::import[]
using TypeDB.Driver;
using TypeDB.Driver.Api;
using Newtonsoft.Json.Linq;
// end::import[]

class ManualProgram
{
    const string DB_NAME = "manual_db";
    const string SERVER_ADDR = "127.0.0.1:1729";
    static void Main(string[] args) {
        // tag::options[]
        TypeDBOptions options = new();
        // end::options[]
        // tag::connect_core[]
        ITypeDBDriver driver = TypeDB.Driver.Drivers.CoreDriver(SERVER_ADDR);
        // end::connect_core[]

        /*
        // tag::connect_cloud[]
        ITypeDBDriver driver = TypeDB.Driver.Drivers.CloudDriver(SERVER_ADDR, new TypeDBCredential("admin", "password", true));
        // end::connect_cloud[]
        */

        // tag::list-db[]
        foreach (IDatabase db in driver.Databases.GetAll()) {
            Console.WriteLine(db.Name);
        }
        // end::list-db[]
        if (driver.Databases.Contains(DB_NAME)) {
            // tag::delete-db[]
            driver.Databases.Get(DB_NAME).Delete();
            // end::delete-db[]
        }
        // tag::create-db[]
        driver.Databases.Create(DB_NAME);
        // end::create-db[]
        Console.WriteLine("Database created.");
        /*
        // tag::session_open[]
        ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data);
        // end::session_open[]
        // tag::tx_open[]
        ITypeDBTransaction tx = session.Transaction(TransactionType.Read, options);
        // end::tx_open[]
        // tag::tx_close[]
        tx.Close();
        // end::tx_close[]
        if (tx.IsOpen()) {
            // tag::tx_commit[]
            tx.Commit();
            // end::tx_commit[]
        }
        // tag::session_close[]
        session.Close();
        // end::session_close[]
        */
        // tag::define[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Schema)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                string define_query = @"
                            define
                            email sub attribute, value string;
                            name sub attribute, value string;
                            friendship sub relation, relates friend;
                            user sub entity,
                                owns email @key,
                                owns name,
                                plays friendship:friend;
                            admin sub user;
                            ";
                tx.Query.Define(define_query).Resolve();
                tx.Commit();
            }
        }
        // end::define[]
        // tag::undefine[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Schema)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                string undefine_query = "undefine admin sub user;";
                tx.Query.Undefine(undefine_query).Resolve();
                tx.Commit();
            }
        }
        // end::undefine[]
        // tag::insert[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                string insert_query = @"
                                        insert
                                        $user1 isa user, has name 'Alice', has email 'alice@vaticle.com';
                                        $user2 isa user, has name 'Bob', has email 'bob@vaticle.com';
                                        $friendship (friend:$user1, friend: $user2) isa friendship;";
                _ = tx.Query.Insert(insert_query).ToList();
                tx.Commit();
            }
        }
        // end::insert[]
        // tag::match-insert[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                string match_insert_query = @"
                                            match
                                            $u isa user, has name 'Bob';
                                            insert
                                            $new-u isa user, has name 'Charlie', has email 'charlie@vaticle.com';
                                            $f($u,$new-u) isa friendship;";
                List<IConceptMap> response = tx.Query.Insert(match_insert_query).ToList();
                if (response.Count == 1) {
                    tx.Commit();
                } else {
                    tx.Close();
                }
            }
        }
        // end::match-insert[]
        // tag::delete[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                string delete_query = @"
                                match
                                $u isa user, has name 'Charlie';
                                $f ($u) isa friendship;
                                delete
                                $f isa friendship;";
                tx.Query.Delete(delete_query).Resolve();
                tx.Commit();
            }
        }
        // end::delete[]
        // tag::update[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                string update_query = @"
                                match
                                $u isa user, has name 'Charlie', has email $e;
                                delete
                                $u has $e;
                                insert
                                $u has email 'charles@vaticle.com';";
                List<IConceptMap> response = tx.Query.Update(update_query).ToList();
                if (response.Count == 1) {
                    tx.Commit();
                } else {
                    tx.Close();
                }
            }
        }
        // end::update[]
        // tag::fetch[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Read)) {
                string fetch_query = @"
                                match
                                $u isa user;
                                fetch
                                $u: name, email;";
                List<JObject> response = tx.Query.Fetch(fetch_query).ToList();
                foreach (JObject answer in response) {
                    Console.WriteLine("User: " + answer.ToString());
                }
            }
        }
        // end::fetch[]
        // tag::get[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Read)) {
                string get_query = @"
                                    match
                                    $u isa user, has email $e;
                                    get
                                    $e;";
                List<IConceptMap> response = tx.Query.Get(get_query).ToList();
                foreach (IConceptMap answer in response) {
                    Console.WriteLine("Email: " + answer.Get("e").AsAttribute().Value);
                }
            }
        }
        // end::get[]
        // tag::infer-rule[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Schema)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                string define_query = @"
                                        define
                                        rule users:
                                        when {
                                            $u isa user;
                                        } then {
                                            $u has name 'User';
                                        };";
                tx.Query.Define(define_query).Resolve();
                tx.Commit();
            }
        }
        // end::infer-rule[]
        // tag::infer-fetch[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Read, options.Infer(true))) {
                string fetch_query = @"
                                        match
                                        $u isa user;
                                        fetch
                                        $u: name, email;";
                List<JObject> response = tx.Query.Fetch(fetch_query).ToList();
                foreach (JObject answer in response) {
                    Console.WriteLine("User: " + answer.ToString());
                }
            }
        }
        // end::infer-fetch[]
        // tag::types-editing[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Schema)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                IAttributeType tag = tx.Concepts.PutAttributeType("tag", IValue.ValueType.String).Resolve()!;
                IEnumerable<IType> entities = tx.Concepts.RootEntityType.GetSubtypes(tx, IConcept.Transitivity.Explicit);
                foreach (IType entity in entities) {
                    Console.WriteLine(entity.Label);
                    if (!entity.IsAbstract()) {
                        entity.AsThingType().SetOwns(tx, tag);
                    }
                }
            }
        }
        // end::types-editing[]
        // tag::types-api[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Schema)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                IEntityType userType = tx.Concepts.GetEntityType("user").Resolve()!;
                IEntityType adminType = tx.Concepts.PutEntityType("admin").Resolve()!;
                adminType.SetSupertype(tx, userType);
                IEnumerable<IType> entities = tx.Concepts.RootEntityType.GetSubtypes(tx, IConcept.Transitivity.Transitive);
                foreach (IType entity in entities) {
                    Console.WriteLine(entity.Label);
                }
                tx.Commit();
            }
        }
        // end::types-api[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Schema)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                // tag::get_type[]
                IEntityType userType = tx.Concepts.GetEntityType("user").Resolve()!;
                // end::get_type[]
                // tag::add_type[]
                IEntityType adminType = tx.Concepts.PutEntityType("admin").Resolve()!;
                // end::add_type[]
                // tag::set_supertype[]
                adminType.SetSupertype(tx, userType);
                // end::set_supertype[]
                // tag::get_instances[]
                IEnumerable<IThing> users = userType.GetInstances(tx);
                // end::get_instances[]
                foreach (IThing user in users) {
                    Console.WriteLine("User: ");
                    // tag::get_has[]
                    IEnumerable<IAttribute> attributes = user.GetHas(tx);
                    // end::get_has[]
                    foreach (IAttribute attribute in attributes) {
                        Console.WriteLine("  " + attribute.Type.Label + ": " + attribute.Value.AsString());
                    }
                }
                // tag::create[]
                IEntity newUser = tx.Concepts.GetEntityType("user").Resolve()!.Create(tx).Resolve()!;
                // end::create[]
                // tag::delete_user[]
                newUser.Delete(tx).Resolve();
                // end::delete_user[]
            }
        }
        // tag::rules-api[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Schema)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                IEnumerable<IRule> rules = tx.Logic.GetRules();
                foreach (IRule rule in rules) {
                    Console.WriteLine(rule.Label);
                    Console.WriteLine(rule.When);
                    Console.WriteLine(rule.Then);
                }
                IRule newRule = tx.Logic.PutRule("Employee", "{$u isa user, has email $e; $e contains '@vaticle.com';}","$u has name 'Employee'").Resolve()!;
                IRule oldRule = tx.Logic.GetRule("users").Resolve()!;
                Console.WriteLine(oldRule.Label);
                newRule.Delete(tx).Resolve();
                tx.Commit();
            }
        }
        // end::rules-api[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Schema)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                // tag::get_rules[]
                IEnumerable<IRule> rules = tx.Logic.GetRules();
                foreach (IRule rule in rules) {
                    Console.WriteLine(rule.Label);
                    Console.WriteLine(rule.When);
                    Console.WriteLine(rule.Then);
                }
                // end::get_rules[]
                // tag::put_rule[]
                IRule newRule = tx.Logic.PutRule("Employee", "{$u isa user, has email $e; $e contains '@vaticle.com';}","$u has name 'Employee'").Resolve()!;
                // end::put_rule[]
                // tag::get_rule[]
                IRule oldRule = tx.Logic.GetRule("users").Resolve()!;
                // end::get_rule[]
                Console.WriteLine(oldRule.Label);
                // tag::delete_rule[]
                newRule.Delete(tx).Resolve();
                // end::delete_rule[]
                tx.Commit();
            }
        }
        // tag::data-api[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                IEntityType userType = tx.Concepts.GetEntityType("user").Resolve()!;
                IEnumerable<IThing> users = userType.GetInstances(tx);
                foreach (IThing user in users) {
                    IEnumerable<IAttribute> attributes = user.GetHas(tx);
                    foreach (IAttribute attribute in attributes) {
                        Console.WriteLine("  " + attribute.Type.Label + ": " + attribute.Value.AsString());
                    }
                }
                IEntity newUser = tx.Concepts.GetEntityType("user").Resolve()!.Create(tx).Resolve()!;
                newUser.Delete(tx).Resolve();
                tx.Commit();
            }
        }
        // end::data-api[]
        // tag::explain-get[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Read, options.Infer(true).Explain(true))) {
                string getQuery = @"match
                                    $u isa user, has email $e, has name $n;
                                    $e contains 'Alice';
                                    get
                                    $u, $n;";
                IList<IConceptMap> response = tx.Query.Get(getQuery).ToList();
                Int16 i = 0;
                foreach (IConceptMap ConceptMap in response) {
                    i++;
                    Console.WriteLine("Name #" + i.ToString() + ": " + ConceptMap.Get("n").AsAttribute().Value.AsString());
                    IEnumerable<KeyValuePair<string, IConceptMap.IExplainable>> explainableRelations = ConceptMap.AllExplainables.GetRelations();
                    foreach (KeyValuePair<string, IConceptMap.IExplainable> explainable in explainableRelations) {
                        Console.WriteLine("Explained variable: " + explainable.Key);
                        Console.WriteLine("Explainable part of the query: " + ConceptMap.AllExplainables.Relation(explainable.Key).Conjunction);
                        IEnumerable<IExplanation> explainIterator = tx.Query.Explain(ConceptMap.AllExplainables.Relation(explainable.Key));
                        foreach (IExplanation explanation in explainIterator) {
                            Console.WriteLine("Rule: " + explanation.Rule.Label);
                            Console.WriteLine("Condition: " + explanation.Rule.When);
                            Console.WriteLine("Conclusion: " + explanation.Rule.Then);
                            Console.WriteLine("Variable mapping: ");
                            foreach (string var in explanation.GetQueryVariables()) {
                                Console.WriteLine("Query variable: " + var + " maps to the rule variable " + explanation.QueryVariableMapping(var).ToString());
                            }
                        }
                    }
                }
            }
        }
        // end::explain-get[]
        using (ITypeDBSession session = driver.Session(DB_NAME, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Read, options.Infer(true).Explain(true))) {
                string getQuery = @"match
                                    $u isa user, has email $e, has name $n;
                                    $e contains 'Alice';
                                    get
                                    $u, $n;";
                // tag::explainables[]
                IList<IConceptMap> response = tx.Query.Get(getQuery).ToList();
                // end::explainables[]
                Int16 i = 0;
                // tag::explainables[]
                foreach (IConceptMap ConceptMap in response) {
                    // end::explainables[]
                    i++;
                    Console.WriteLine("Name #" + i.ToString() + ": " + ConceptMap.Get("n").AsAttribute().Value.AsString());
                    // tag::explainables[]
                    IEnumerable<KeyValuePair<string, IConceptMap.IExplainable>> explainableRelations = ConceptMap.AllExplainables.GetRelations();
                    // end::explainables[]
                    // tag::explain[]
                    foreach (KeyValuePair<string, IConceptMap.IExplainable> explainable in explainableRelations) {
                        IEnumerable<IExplanation> explainIterator = tx.Query.Explain(ConceptMap.AllExplainables.Relation(explainable.Key));
                        // end::explain[]
                        Console.WriteLine("Explained variable: " + explainable.Key);
                        Console.WriteLine("Explainable part of the query: " + ConceptMap.AllExplainables.Relation(explainable.Key).Conjunction);
                        // tag::explanation[]
                        foreach (IExplanation explanation in explainIterator) {
                            Console.WriteLine("Rule: " + explanation.Rule.Label);
                            Console.WriteLine("Condition: " + explanation.Rule.When);
                            Console.WriteLine("Conclusion: " + explanation.Rule.Then);
                            Console.WriteLine("Variable mapping: ");
                            foreach (string var in explanation.GetQueryVariables()) {
                                Console.WriteLine("Query variable: " + var + " maps to the rule variable " + explanation.QueryVariableMapping(var).ToString());
                            }
                        }
                        // end::explanation[]
                    // tag::explain[]
                    }
                    // end::explain[]
                // tag::explainables[]
                }
                // end::explainables[]
            }
        }
    } // main
}
