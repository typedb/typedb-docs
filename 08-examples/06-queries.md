---
sidebarTitle: Queries
pageTitle: Queries the Phone Calls Knowledge Graph
permalink: /docs/examples/phone-calls-queries
---

## Goal

When we [modelled and loaded the schema into Grakn](./defining-the-schema), we had some insights in mind that we wanted to obtain from `phone_calls`; the knowledge graph.

Let’s revise:

- [Since September 14th, which customers called person X?](#since-september-14th-which-customers-called-person-x)
- [Who are the people who have received a call from a London customer aged over 50 who has previously called someone aged under 20?](#who-are-the-people-who-have-received-a-call-from-a-london-customer-aged-over-50-who-has-previously-called-someone-aged-under-20)
- [Who are the common contacts of customers X and Y?](#who-are-the-common-contacts-of-customers-x-and-y)
- [Who are the customers who 1) have all called each other and 2) have all called person X at least once?](#who-are-the-customers-who-1-have-all-called-each-other-and-2-have-all-called-person-x-at-least-once)
- [How does the average call duration among customers aged under 20 compare those aged over 40?](#how-does-the-average-call-duration-among-customers-aged-under-20-compare-with-those-aged-over-40)

For the rest of this post, we go through each of these questions to:

- understand their business value,
- write them as a statement,
- write them in [Graql](http://dev.grakn.ai/academy/graql-intro.html), and
- assess their result.

Make sure you have the [Visualisation Dashboard](http://dev.grakn.ai/docs/visualisation-dashboard/visualiser) (at [localhost:4567](http://localhost:4567/)) opened in your browser, while phone_calls selected as the keyspace (in the top-right hand corner).

Let’s begin.

### Since September 14th, which customers called person X?

#### The business value:

> The person with phone number +86 921 547 9004 has been identified as a lead. We (company "Telecom") would like to know which of our customers have been in contact with this person since September 14th. This helps us in converting this lead into a customer.

#### As a statement:

> Get me the customers of company “Telecom” who called the target person with phone number +86 921 547 9004 from September 14th onwards.

#### In Graql:
<!-- test-ignore -->
```graql
match
  $customer isa person, has phone-number $phone-number;
  $company isa company, has name "Telecom";
  (customer: $customer, provider: $company) isa contract;
  $target isa person, has phone-number "+86 921 547 9004";
  (caller: $customer, callee: $target) isa call, has started-at $started-at;
  $min-date == 2018-09-14T17:18:49; $started-at > $min-date;
get $phone-number;
```

#### The result:

```javascript
[ '+62 107 530 7500', '+370 351 224 5176', '+54 398 559 0423',
  '+7 690 597 4443',  '+263 498 495 0617', '+63 815 962 6097',
  '+81 308 988 7153', '+81 746 154 2598']
```

#### Try it yourself

![phone_calls query #1 Workbase](/docs/images/examples/phone_calls_query_1_workbase.png)
[caption:Using [Workbase](/docs/workbase/overview)]

![phone_calls query #1 Console](/docs/images/examples/phone_calls_query_1_console.png)
[caption:Using [Grakn Console](/docs/running-grakn/console)]

<div class="tabs dark">
[tab:Java]
<!-- test-standalone PhoneCallsFirstQuery.java -->
```java
package ai.grakn.examples;

import grakn.core.client.GraknClient;
import grakn.core.graql.query.query.GraqlGet;
import grakn.core.server.Transaction;
import grakn.core.server.exception.TransactionException;
import static grakn.core.graql.query.Graql.*;

import java.util.*;

public class PhoneCallsFirstQuery {
    public static void main(String[] args) throws TransactionException {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("phone_calls");
        GraknClient.Transaction transaction = session.transaction(Transaction.Type.WRITE);

        List<String> queryAsList = Arrays.asList(
                "match",
                "  $customer isa person, has phone-number $phone-number;",
                "  $company isa company, has name \"Telecom\";",
                "  (customer: $customer, provider: $company) isa contract;",
                "  $target isa person, has phone-number \"+86 921 547 9004\";",
                "  (caller: $customer, callee: $target) isa call, has started-at $started-at;",
                "  $min-date == 2018-09-14T17:18:49; $started-at > $min-date;",
                "get $phone-number;"
        );

        System.out.println("\nQuery:\n" + String.join("\n", queryAsList));
        String query = String.join("", queryAsList);

        List<String> result = new ArrayList<>();

        transaction.execute((GraqlGet) parse(query)).forEach(answer -> {
                result.add(
                        answer.asConceptMap().get("phone-number").asAttribute().value().toString()
                );
        });

        System.out.println("\nResult:\n" + String.join(", ", result));

        transaction.close();
        session.close();
    }
}
```
[tab:end]

[tab:Node.js]
<!-- test-standalone PhoneCallsFirstQuery.js -->
```javascript
const Grakn = require("grakn");
const grakn = new Grakn("localhost:48555");
const session = grakn.session("phone_calls");

ExecuteMatchQuery();

async function ExecuteMatchQuery() {
  const transaction = await session.transaction(Grakn.TxType.READ);

  let query = [
    "match",
    "  $customer isa person, has phone-number $phone-number;",
    '  $company isa company, has name "Telecom";',
    "  (customer: $customer, provider: $company) isa contract;",
    '  $target isa person, has phone-number "+86 921 547 9004";',
    "  (caller: $customer, callee: $target) isa call, has started-at $started-at;",
    "  $min-date == 2018-09-14T17:18:49; $started-at > $min-date;",
    "get $phone-number;"
  ];

  console.log("\nQuery:\n", query.join("\n"));
  query = query.join("");

  const iterator = await transaction.query(query);
  const answers = await iterator.collect();
  const result = await Promise.all(
    answers.map(answer =>
      answer
        .map()
        .get("phone-number")
        .value()
    )
  );

  console.log("\nResult:\n", result);

  await transaction.close();
  await session.close();
}
```
[tab:end]

[tab:Python]
<!-- test-standalone phone_calls_first_query.py -->
```python
import grakn

client = grakn.Grakn(uri = "localhost:48555")
with client.session(keyspace = "phone_calls") as session:
  with session.transaction(grakn.TxType.READ) as transaction:
    query = [
      'match',
      '  $customer isa person, has phone-number $phone-number;',
      '  $company isa company, has name "Telecom";',
      '  (customer: $customer, provider: $company) isa contract;',
      '  $target isa person, has phone-number "+86 921 547 9004";',
      '  (caller: $customer, callee: $target) isa call, has started-at $started-at;',
      '  $min-date == 2018-09-14T17:18:49; $started-at > $min-date;',
      'get $phone-number;'
    ]

    print("\nQuery:\n", "\n".join(query))
    query = "".join(query)

    iterator = transaction.query(query)
    answers = iterator.collect_concepts()
    result = [ answer.value() for answer in answers ]

    print("\nResult:\n", result)
```
[tab:end]

</div>


### Who are the people who have received a call from a London customer aged over 50 who has previously called someone aged under 20?

#### The business value:

> We (company "Telecom") have received a number of harassment reports, which we suspect is caused by one individual. The only thing we know about the harasser is that he/she is aged roughly over 50 and lives in London. The reports have been made by young adults all aged under 20. We wonder if there is a pattern and so would like to speak to anyone who has received a call from a suspect since he/she potentially started harassing.

#### As a statement:

> Get me the phone number of people who have received a call from a customer aged over 50 after this customer (suspect) made a call to another customer aged under 20.

#### In Graql:
<!-- test-ignore -->
```graql
match
  $suspect isa person, has city "London", has age > 50;
  $company isa company, has name "Telecom";
  (customer: $suspect, provider: $company) isa contract;
  $pattern-callee isa person, has age < 20;
  (caller: $suspect, callee: $pattern-callee) isa call, has started-at $pattern-call-date;
  $target isa person, has phone-number $phone-number, has is-customer false;
  (caller: $suspect, callee: $target) isa call, has started-at $target-call-date;
  $target-call-date > $pattern-call-date;
get $phone-number;
```

#### The result:

```javascript
[ '+30 419 575 7546',  '+86 892 682 0628', '+1 254 875 4647',
  '+351 272 414 6570', '+33 614 339 0298', '+86 922 760 0418',
  '+86 825 153 5518',  '+48 894 777 5173', '+351 515 605 7915',
  '+63 808 497 1769',  '+27 117 258 4149', '+86 202 257 8619' ]
```

#### Try it yourself

![phone_calls query #2 Workbase](/docs/images/examples/phone_calls_query_2_workbase.png)
[caption:Using [Workbase](/docs/workbase/overview)]

![phone_calls query #2 Console](/docs/images/examples/phone_calls_query_2_console.png)
[caption:Using [Grakn Console](/docs/running-grakn/console)]

<div class="tabs dark">
[tab:Java]
<!-- test-standalone PhoneCallsSecondQuery.java -->
```java
package ai.grakn.examples;

import grakn.core.client.GraknClient;
import grakn.core.graql.query.query.GraqlGet;
import grakn.core.server.Transaction;
import grakn.core.server.exception.TransactionException;
import static grakn.core.graql.query.Graql.*;

import java.util.*;

public class PhoneCallsSecondQuery {
    public static void main(String[] args) throws TransactionException {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("phone_calls");
        GraknClient.Transaction transaction = session.transaction(Transaction.Type.WRITE);

        List<String> queryAsList = Arrays.asList(
                "match ",
                "  $suspect isa person, has city \"London\", has age > 50;",
                "  $company isa company, has name \"Telecom\";",
                "  (customer: $suspect, provider: $company) isa contract;",
                "  $pattern-callee isa person, has age < 20;",
                "  (caller: $suspect, callee: $pattern-callee) isa call, has started-at $pattern-call-date;",
                "  $target isa person, has phone-number $phone-number, has is-customer false;",
                "  (caller: $suspect, callee: $target) isa call, has started-at $target-call-date;",
                "  $target-call-date > $pattern-call-date;",
                "get $phone-number;"
        );

        System.out.println("\nQuery:\n" + String.join("\n", queryAsList));
        String query = String.join("", queryAsList);

        List<String> result = new ArrayList<>();
        transaction.execute((GraqlGet) parse(query)).forEach(answer -> {
                result.add(
                        answer.asConceptMap().get("phone-number").asAttribute().value().toString()
                );
        });

        System.out.println("\nResult:\n" + String.join(", ", result));

        transaction.close();
        session.close();
    }
}

```
[tab:end]

[tab:Node.js]
<!-- test-standalone PhoneCallsSecondQuery.js -->
```javascript
const Grakn = require("grakn");
const grakn = new Grakn("localhost:48555");
const session = grakn.session("phone_calls");

ExecuteMatchQuery();

async function ExecuteMatchQuery() {
  const tx = await session.transaction(Grakn.txType.READ);

  let query = [
    "match ",
    '  $suspect isa person, has city "London", has age > 50;',
    '  $company isa company, has name "Telecom";',
    "  (customer: $suspect, provider: $company) isa contract;",
    "  $pattern-callee isa person, has age < 20;",
    "  (caller: $suspect, callee: $pattern-callee) isa call, has started-at $pattern-call-date;",
    "  $target isa person, has phone-number $phone-number, has is-customer false;",
    "  (caller: $suspect, callee: $target) isa call, has started-at $target-call-date;",
    "  $target-call-date > $pattern-call-date;",
    "get $phone-number;"
  ];

  console.log("\nQuery:\n", query.join("\n"));
  query = query.join("");

  const iterator = await tx.query(query);
  const answers = await iterator.collect();
  const result = await Promise.all(
    answers.map(answer =>
      answer
        .map()
        .get("phone-number")
        .value()
    )
  );

  console.log("\nResult:\n", result);

  await ransaction.close();
  await session.close();
}
```
[tab:end]

[tab:Python]
<!-- test-standalone phone_calls_first_query.py -->
```python
import grakn

client = grakn.Grakn(uri = "localhost:48555")
with client.session(keyspace = "phone_calls") as session:
  with session.transaction(grakn.TxType.READ) as tx:
    query = [
      'match ',
      '  $suspect isa person, has city "London", has age > 50;',
      '  $company isa company, has name "Telecom";',
      '  (customer: $suspect, provider: $company) isa contract;',
      '  $pattern-callee isa person, has age < 20;',
      '  (caller: $suspect, callee: $pattern-callee) isa call, has started-at $pattern-call-date;',
      '  $target isa person, has phone-number $phone-number, has is-customer false;',
      '  (caller: $suspect, callee: $target) isa call, has started-at $target-call-date;',
      '  $target-call-date > $pattern-call-date;',
      'get $phone-number;'
    ]

    print("\nQuery:\n", "\n".join(query))
    query = "".join(query)

    iterator = tx.query(query)
    answers = iterator.collect_concepts()
    result = [ answer.value() for answer in answers ]

    print("\nResult:\n", result)
```
[tab:end]

</div>


### Who are the common contacts of customers X and Y?

#### The business value:

> The customer with phone number +7 171 898 0853 and +370 351 224 5176 have been identified as friends. We (company "Telecom") like to know who their common contacts are in order to offer them a group promotion.

#### As a statement:

> Get me the phone number of people who have received calls from both customer with phone number +7 171 898 0853 and customer with phone number +370 351 224 5176.

#### In Graql:
<!-- test-ignore -->
```graql
match
  $common-contact isa person, has phone-number $phone-number;
  $customer-a isa person, has phone-number "+7 171 898 0853";
  $customer-b isa person, has phone-number "+370 351 224 5176";
  (caller: $customer-a, callee: $common-contact) isa call;
  (caller: $customer-b, callee: $common-contact) isa call;
get $phone-number;
```

#### The result:

```javascript
['+86 892 682 0628', '+54 398 559 0423']
```

#### Try it yourself

![phone_calls query #3 Workbase](/docs/images/examples/phone_calls_query_3_workbase.png)
[caption:Using [Workbase](/docs/workbase/overview)]

![phone_calls query #3 Console](/docs/images/examples/phone_calls_query_3_console.png)
[caption:Using [Grakn Console](/docs/running-grakn/console)]

<div class="tabs dark">
[tab:Java]
<!-- test-standalone PhoneCallsThirdQuery.java -->
```java
package ai.grakn.examples;

import grakn.core.client.GraknClient;
import grakn.core.graql.query.query.GraqlGet;
import grakn.core.server.Transaction;
import grakn.core.server.exception.TransactionException;
import static grakn.core.graql.query.Graql.*;

import java.util.*;

public class PhoneCallsThirdQuery {
    public static void main(String[] args) throws TransactionException {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("phone_calls");
        GraknClient.Transaction transaction = session.transaction(Transaction.Type.WRITE);

        List<String> queryAsList = Arrays.asList(
                "match ",
                "  $common-contact isa person, has phone-number $phone-number;",
                "  $customer-a isa person, has phone-number \"+7 171 898 0853\";",
                "  $customer-b isa person, has phone-number \"+370 351 224 5176\";",
                "  (caller: $customer-a, callee: $common-contact) isa call;",
                "  (caller: $customer-b, callee: $common-contact) isa call;",
                "get $phone-number;"
        );

        System.out.println("\nQuery:\n" + String.join("\n", queryAsList));
        String query = String.join("", queryAsList);

        List<String> result = new ArrayList<>();
        transaction.execute((GraqlGet) parse(query)).forEach(answer -> {
                result.add(
                        answer.asConceptMap().get("phone-number").asAttribute().value().toString()
                );
        });

        System.out.println("\nResult:\n" + String.join(", ", result));

        transaction.close();
        session.close();
    }
}
```
[tab:end]

[tab:Node.js]
<!-- test-standalone PhoneCallsThirdQuery.js -->
```javascript
const Grakn = require("grakn");
const grakn = new Grakn("localhost:48555");
const session = grakn.session("phone_calls");

ExecuteMatchQuery();

async function ExecuteMatchQuery() {
  const tx = await session.transaction(Grakn.txType.READ);

  let query = [
    "match ",
    "  $common-contact isa person, has phone-number $phone-number;",
    '  $customer-a isa person, has phone-number "+7 171 898 0853";',
    '  $customer-b isa person, has phone-number "+370 351 224 5176";',
    "  (caller: $customer-a, callee: $common-contact) isa call;",
    "  (caller: $customer-b, callee: $common-contact) isa call;",
    "get $phone-number;"
  ];

  console.log("\nQuery:\n", query.join("\n"));
  query = query.join("");

  const iterator = await tx.query(query);
  const answers = await iterator.collect();
  const result = await Promise.all(
    answers.map(answer =>
      answer
        .map()
        .get("phone-number")
        .value()
    )
  );

  console.log("\nResult:\n", result);

  await session.close();
  process.exit();
}
```
[tab:end]

[tab:Python]
<!-- test-standalone phone_calls_third_query.py -->
```python
import grakn

client = grakn.Grakn(uri = "localhost:48555")
with client.session(keyspace = "phone_calls") as session:
  with session.transaction(grakn.TxType.READ) as tx:
    query = [
      'match ',
      '  $common-contact isa person, has phone-number $phone-number;',
      '  $customer-a isa person, has phone-number "+7 171 898 0853";',
      '  $customer-b isa person, has phone-number "+370 351 224 5176";',
      '  (caller: $customer-a, callee: $common-contact) isa call;',
      '  (caller: $customer-b, callee: $common-contact) isa call;',
      'get $phone-number;'
    ]

    print("\nQuery:\n", "\n".join(query))
    query = "".join(query)

    iterator = tx.query(query)
    answers = iterator.collect_concepts()
    result = [ answer.value() for answer in answers ]

    print("\nResult:\n", result)
```
[tab:end]

</div>

### Who are the customers who 1) have all called each other and 2) have all called person X at least once?

#### The business value:

```
The person with phone number +48 894 777 5173 has been identified as a lead. We (company "Telecom") would like to know who his circle of  (customer) contacts are, so that we can encourage them in converting this lead to a customer.
```

#### As a statement:

```
Get me the phone phone number of all customers who have called each other as well the person with phone number +48 894 777 5173.
```

#### In Graql:
<!-- test-ignore -->
```graql
match
  $target isa person, has phone-number "+48 894 777 5173";
  $company isa company, has name "Telecom";
  $customer-a isa person, has phone-number $phone-number-a;
  $customer-b isa person, has phone-number $phone-number-b;
  (customer: $customer-a, provider: $company) isa contract;
  (customer: $customer-b, provider: $company) isa contract;
  (caller: $customer-a, callee: $customer-b) isa call;
  (caller: $customer-a, callee: $target) isa call;
  (caller: $customer-b, callee: $target) isa call;
get $phone-number-a, $phone-number-b;
```

#### The result:

```javascript
[ '+62 107 530 7500', '+261 860 539 4754', '+81 308 988 7153' ]
```

#### Try it yourself

![phone_calls query #4 Workbase](/docs/images/examples/phone_calls_query_4_workbase.png)
[caption:Using [Workbase](/docs/workbase/overview)]

![phone_calls query #4 Console](/docs/images/examples/phone_calls_query_4_console.png)
[caption:Using [Grakn Console](/docs/running-grakn/console)]

<div class="tabs dark">
[tab:Java]
<!-- test-standalone PhoneCallsForthQuery.java -->
```java
package ai.grakn.examples;

import grakn.core.client.GraknClient;
import grakn.core.graql.query.query.GraqlGet;
import grakn.core.server.Transaction;
import grakn.core.server.exception.TransactionException;
import static grakn.core.graql.query.Graql.*;

import java.util.*;

public class PhoneCallsForthQuery {
    public static void main(String[] args) throws TransactionException {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("phone_calls");
        GraknClient.Transaction transaction = session.transaction(Transaction.Type.WRITE);

        List<String> queryAsList = Arrays.asList(
                "match ",
                "  $target isa person, has phone-number \"+48 894 777 5173\";",
                "  $company isa company, has name \"Telecom\";",
                "  $customer-a isa person, has phone-number $phone-number-a;",
                "  (customer: $customer-a, provider: $company) isa contract;",
                "  (caller: $customer-a, callee: $target) isa call;",
                "  $customer-b isa person, has phone-number $phone-number-b;",
                "  (customer: $customer-b, provider: $company) isa contract;",
                "  (caller: $customer-b, callee: $target) isa call;",
                "  (caller: $customer-a, callee: $customer-b) isa call;",
                "get $phone-number-a, $phone-number-b;"
        );

        System.out.println("\nQuery:\n" + String.join("\n", queryAsList));
        String query = String.join("", queryAsList);

        Set<String> result = new HashSet<>();
        transaction.execute((GraqlGet) parse(query)).forEach(answer -> {
            result.add(answer.asConceptMap().get("phone-number-a").asAttribute().value().toString());
            result.add(answer.asConceptMap().get("phone-number-b").asAttribute().value().toString());
        });

        System.out.println("\nResult:\n" + String.join(", ", result));

        transaction.close();
        session.close();
    }
}
```
[tab:end]

[tab:Node.js]
<!-- test-standalone PhoneCallsForthQuery.js -->
```javascript
const Grakn = require("grakn");
const grakn = new Grakn("localhost:48555");
const session = grakn.session("phone_calls");

ExecuteMatchQuery();

async function ExecuteMatchQuery() {
  const tx = await session.transaction(Grakn.txType.READ);

  let query = [
    "match ",
    '  $target isa person, has phone-number "+48 894 777 5173";',
    '  $company isa company, has name "Telecom";',
    "  $customer-a isa person, has phone-number $phone-number-a;",
    "  (customer: $customer-a, provider: $company) isa contract;",
    "  (caller: $customer-a, callee: $target) isa call;",
    "  $customer-b isa person, has phone-number $phone-number-b;",
    "  (customer: $customer-b, provider: $company) isa contract;",
    "  (caller: $customer-b, callee: $target) isa call;",
    "  (caller: $customer-a, callee: $customer-b) isa call;",
    "get $phone-number-a, $phone-number-b;"
  ];

  console.log("\nQuery:\n", query.join("\n"));
  query = query.join("");

  const iterator = await tx.query(query);
  const answers = await iterator.collect();
  const result = await Promise.all(
    answers.map(answer =>
      answer
        .map()
        .get("phone-number-a")
        .value()
    )
  );

  console.log("\nResult:\n", result);

  await session.close();
  process.exit();
}
```
[tab:end]

[tab:Python]
<!-- test-standalone phone_calls_forth_query.py -->
```python
import grakn

client = grakn.Grakn(uri = "localhost:48555")
with client.session(keyspace = "phone_calls") as session:
  with session.transaction(grakn.TxType.READ) as tx:
  query = [
      'match ',
      '  $target isa person, has phone-number "+48 894 777 5173";',
      '  $company isa company, has name "Telecom";',
      '  $customer-a isa person, has phone-number $phone-number-a;',
      '  (customer: $customer-a, provider: $company) isa contract;',
      '  (caller: $customer-a, callee: $target) isa call;',
      '  $customer-b isa person, has phone-number $phone-number-b;',
      '  (customer: $customer-b, provider: $company) isa contract;',
      '  (caller: $customer-b, callee: $target) isa call;',
      '  (caller: $customer-a, callee: $customer-b) isa call;',
      'get $phone-number-a, $phone-number-b;'
    ]

    print("\nQuery:\n", "\n".join(query))
    query = "".join(query)

    iterator = tx.query(query)
    answers = iterator.collect_concepts()
    result = [ answer.value() for answer in answers ]

    print("\nResult:\n", result)
```
[tab:end]

</div>

### How does the average call duration among customers aged under 20 compare with those aged over 40?

#### The business value:

> In order to better understand our customers' behaviour, we (company "Telecom") like to know how the average phone call duration among those aged under 20 compares to those aged over 40.

Two queries need to be executed to provide this insight.

### Query 1: aged under 20

#### As a statement:

> Get me the average call duration among customers who have a contract with company "Telecom" and are aged under 20.

#### In Graql:
<!-- test-ignore -->
```graql
match
  $customer isa person, has age < 20;
  $company isa company, has name "Telecom";
  (customer: $customer, provider: $company) isa contract;
  (caller: $customer, callee: $anyone) isa call, has duration $duration;
get $duration; mean $duration;
```

#### The result:

```
1242 seconds
```

### Query 2: aged over 40

#### As a statement:

> Get me the average call duration among customers who have a contract with company "Telecom" and are aged over 40.

#### In Graql:
<!-- test-ignore -->
```graql
match
  $customer isa person, has age > 40;
  $company isa company, has name "Telecom";
  (customer: $customer, provider: $company) isa contract;
  (caller: $customer, callee: $anyone) isa call, has duration $duration;
get $duration; mean $duration;
```

#### The result:

```
1713 seconds
```

#### Try it yourself

![phone_calls query #5 Console](/docs/images/examples/phone_calls_query_5_console.png)
[caption:Using [Grakn Console](/docs/running-grakn/console)]

<div class="tabs dark">
[tab:Java]
<!-- test-standalone PhoneCallsFifthQuery.java -->
```java
package ai.grakn.examples;

import grakn.core.client.GraknClient;
import grakn.core.graql.answer.Value;
import grakn.core.graql.query.query.GraqlGet;
import grakn.core.server.Transaction;
import grakn.core.server.exception.TransactionException;
import static grakn.core.graql.query.Graql.*;

import java.util.*;

public class PhoneCallsFifthQuery {
    public static void main(String[] args) throws TransactionException {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("phone_calls");
        GraknClient.Transaction transaction = session.transaction(Transaction.Type.WRITE);

        List<String> firstQueryAsList = Arrays.asList(
                "match",
                "  $customer isa person, has age < 20;",
                "  $company isa company, has name \"Telecom\";",
                "  (customer: $customer, provider: $company) isa contract;",
                "  (caller: $customer, callee: $anyone) isa call, has duration $duration;",
                "get $duration; mean $duration;"
        );

        System.out.println("\nFirst Query:\n" + String.join("\n", firstQueryAsList));

        String firstQuery = String.join("", firstQueryAsList);

        List<Value> firstAnswers = transaction.execute((GraqlGet.Aggregate) parse(firstQuery));
        float fisrtResult = 0;
        if (firstAnswers.size() > 0) {
            fisrtResult = firstAnswers.get(0).asValue().number().floatValue();
        }

        String result = "Customers aged under 20 have made calls with average duration of " + fisrtResult + " seconds.\n";

        List<String> secondQueryAsList = Arrays.asList(
                "match",
                "  $customer isa person, has age > 40;",
                "  $company isa company, has name \"Telecom\";",
                "  (customer: $customer, provider: $company) isa contract;",
                "  (caller: $customer, callee: $anyone) isa call, has duration $duration;",
                "get $duration; mean $duration;"
        );

        System.out.println("\nSecond Query:\n" +
                String.join("\n", secondQueryAsList));

        String secondQuery = String.join("", secondQueryAsList);

        float secondResult = 0;
        List<Value> secondAnswers = transaction.execute((GraqlGet.Aggregate) parse(secondQuery));
        if (secondAnswers.size() > 0) {
            secondResult = secondAnswers.get(0).asValue().number().floatValue();
        }

        result += "Customers aged over 40 have made calls with average duration of " + secondResult + " seconds.\n";

        System.out.println("\nResult:\n" + String.join(", ", result));

        transaction.close();
        session.close();
    }
}
```
[tab:end]

[tab:Node.js]
<!-- test-standalone PhoneCallsFifthQuery.js -->
```javascript
const Grakn = require("grakn");
const grakn = new Grakn("localhost:48555");
const session = grakn.session("phone_calls");

ExecuteMatchQuery();

async function ExecuteMatchQuery() {
  const tx = await session.transaction(Grakn.txType.READ);

  let queryA = [
    "match",
    "  $customer isa person, has age < 20;",
    '  $company isa company, has name "Telecom";',
    "  (customer: $customer, provider: $company) isa contract;",
    "  (caller: $customer, callee: $anyone) isa call, has duration $duration;",
    "get $duration; mean $duration;"
  ];
  console.log("\nQuery:\n", queryA.join("\n"));
  queryA = queryA.join("");

  const iteratorA = await tx.query(queryA);
  const answersA = await iteratorA.collect();
  const resultA = answersA[0].number();
  let result =
    "Customers aged under 20 have made calls with average duration of " +
    Math.round(resultA) +
    " seconds.\n";

  let queryB = [
    "match ",
    "  $customer isa person, has age > 40;",
    '  $company isa company, has name "Telecom";',
    "  (customer: $customer, provider: $company) isa contract;",
    "  (caller: $customer, callee: $anyone) isa call, has duration $duration;",
    "get $duration; mean $duration;"
  ];
  console.log("\nQuery:\n", queryB.join("\n"));
  queryB = queryB.join("");

  const iteratorB = await tx.query(queryB);
  const answersB = await iteratorB.collect();
  const resultB = answersB[0].number();
  result +=
    "Customers aged over 40 have made calls with average duration of " +
    Math.round(resultB) +
    " seconds.\n";

  console.log("\nResult:\n", result);

  await session.close();
  process.exit();
}
```
[tab:end]

[tab:Python]
<!-- test-standalone phone_calls_fifth_query.py -->
```python
import grakn

client = grakn.Grakn(uri = "localhost:48555")
with client.session(keyspace = "phone_calls") as session:
  with session.transaction(grakn.TxType.READ) as tx:
    query_a = [
      'match',
      '  $customer isa person, has age < 20;',
      '  $company isa company, has name "Telecom";',
      '  (customer: $customer, provider: $company) isa contract;',
      '  (caller: $customer, callee: $anyone) isa call, has duration $duration;',
      'get $duration; mean $duration;'
    ]

    print("\nQuery:\n", "\n".join(query_a))
    query_a = "".join(query_a)

    iterator_a = tx.query(query_a)
    result_a = next(iterator_a).number()
    result = ("Customers aged under 20 have made calls with average duration of "
             + str(round(result_a)) + " seconds.\n")

    query_b = [
      'match ',
      '  $customer isa person, has age > 40;',
      '  $company isa company, has name "Telecom";',
      '  (customer: $customer, provider: $company) isa contract;',
      '  (caller: $customer, callee: $anyone) isa call, has duration $duration;',
      'get $duration; mean $duration;'
    ]
    print("\nQuery:\n", "\n".join(query_b))
    query_b = "".join(query_b)

    iterator_b = tx.query(query_b)
    result_b = next(iterator_b).number()
    result += ("Customers aged above 40 have made calls with average duration of "
              + str(round(result_b)) + " seconds.\n")

    print("\nResult:\n", result)
```
[tab:end]

</div>

## 👏 You’ve done it!

Five Graql queries, each written in a few lines, answered all of our questions.
Our imaginary client, Telecom, can now take these insights back to their team and, hopefully, use them responsibly to serve their customers.
And you ... are the one who made it happen!
