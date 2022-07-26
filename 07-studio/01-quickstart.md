---
pageTitle: Quickstart
keywords: typedb, studio, studio quickstart
longTailKeywords: typedb studio preferences, typedb studio connection, typedb studio get started
Summary: Quickstart with Studio
toc: false
---

## Introduction

This guide is here to take you from no knowledge of Studio or TypeDB to a place where you can freely run queries against some pre-provided data from entirely within Studio.
By following each step, you will have the full picture on how to go from zero to full data visualisation using Studio and TypeDB.

## What You Need
- A [TypeDB Server](/docs/running-typedb/install-and-run) instance running locally on the default port (1729).
- An OS-appropriate version of [Studio](https://vaticle.com/download#typedb-studio).

## Running TypeDB Server
Downloading, installing and running a TypeDB server differs slightly platform to platform, so we've created a guide to get you started here: [Install and Run TypeDB Server](/docs/running-typedb/install-and-run).

## Connecting to TypeDB Server
Once you launch Studio, head to the top right-hand corner and click 'Connect to TypeDB'.

<div class="slideshow">

[slide:start]
[header:start][header:end]
[body:start]![Connection Manager Disconnected](/docs/images/studio/connection-interface-disconnected.png)[body:end]
[footer:start]This is the connection manager. Fill in the address of your TypeDB Server. If you've followed the above guide to install and run TypeDB, this is probably `localhost:1729`.[footer:end]
[slide:end]

[slide:start]
[body:start]![Connection Manager Connected](/docs/images/studio/connection-interface-connected.png)[body:end]
[footer:start]Once you've connected successfully, the connection manager will reflect this in with the status field in the bottom left-hand corner. Additionally, the address will be reflected in the top right-hand corner of Studio.[footer:end]
[slide:end]
</div>

Now Studio is connected to your TypeDB instance.

## Creating a Database
Now Studio and TypeDB Server are connected, but you haven't set up any databases. To do so, go to the databases icon in the top left-hand corner.

<div class="slideshow">

[slide:start]
[header:start][header:end]
[body:start]![Database Manager Empty](/docs/images/studio/studio-database.png)[body:end]
[footer:start]This icon opens the database manager.[footer:end]
[slide:end]

[header:start][header:end]
[body:start]![Database Manager Empty](/docs/images/studio/databases-interface-no-databases.png)[body:end]
[footer:start]This is the database manager. Enter your database name then hit 'Create'. For the purposes of this example, we will use the name `phone_calls`.[footer:end]
[slide:end]

[slide:start]
[body:start]![Database Manager With Phone Calls Database](/docs/images/studio/databases-interface-phone-calls-database.png)[body:end]
[footer:start]Now you've successfully created a database named `phone_calls`![footer:end]
[slide:end]
</div>

Select the database you just created by clicking the dropdown menu titled 'Select Databases' immediately right of the databases icon.

## Creating a Project Folder
We've created a database, so now would be a good time to set up a project folder. Studio will store queries you save here, so you don't need to rewrite all your queries each time you open Studio.

<div class="slideshow">

[slide:start]
[header:start][header:end]
[body:start]![Project Interface Prompt to Open](/docs/images/studio/project-interface-open.png)[body:end]
[footer:start]This is the project view. Open a local folder where you'd like to store your queries and other data associated with this project.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Project Interface With Open Folder](/docs/images/studio/project-interface-created-folder.png)[body:end]
[footer:start]Your newly created folder should look something like this.[footer:end]
[slide:end]

</div>

## Writing a Schema
You may have noticed that now you have connected to TypeDB and opened a project folder, Studio has sprung to life. Now we need to write a 'schema' to our database. 
You can learn more about what a schema is and how to write one [here](/docs/schema/overview). In short, a schema is a description of the structure of your data and how various entities relate to each other.

For now, we've got a pre-made schema for you to use. We've also got data and queries for this later, so keep following along if you want to get the full experience from this guide.

```typeql

define
    name sub attribute,
      value string;
    started-at sub attribute,
      value datetime;
    duration sub attribute,
      value long;
    first-name sub attribute,
      value string;
    last-name sub attribute,
      value string;
    phone-number sub attribute,
      value string;
    city sub attribute,
      value string;
    age sub attribute,
      value long;

    contract sub relation,
        relates provider,
        relates customer;

    call sub relation,
        relates caller,
        relates callee,
        owns started-at,
        owns duration;
        
    mutual-caller sub relation,
        relates friend1,
        relates friend2;

    company sub entity,
        plays contract:provider,
        owns name;

    person sub entity,
        plays contract:customer,
        plays call:caller,
        plays call:callee,
        owns first-name,
        owns last-name,
        owns phone-number,
        owns city,
        owns age;
```

This schema represents a simple subset of the data a telecom provider might store.
- A `call` is a phone call that took place over a duration and started at a given time, relating the person who called and the person who picked up (caller and callee respectively.)
- A `company` is a provider in a contract, and has a name.
- A `contract` is a relation between a customer and a provider.
- A `mutual-caller` is a relation between two callees who share a common caller.
- A `person` is a person. They have a first and last name, a phone number, a city they reside in and an age. They 'play' a caller, a callee or a customer in our schema.

Now, lets write this schema to our newly created database.

<div class="slideshow">

[slide:start]
[body:start]![Create a New File](/docs/images/studio/project-new-file.png)[body:end]
[footer:start]Create a new file by clicking the '+' icon in the section right of the project view. It should look like this.[footer:end]
[slide:end]

[slide:start]
[body:start]![Paste in Our Schema](/docs/images/studio/project-schema-pasted.png)[body:end]
[footer:start]Copy the above schema and paste it into this file.[footer:end]
[slide:end]

[slide:start]
[body:start]![Write the Schema](/docs/images/studio/project-schema-query-run.png)[body:end]
[footer:start]Now, make sure your session and transaction types are set to `schema` and `write` respectively. These can be found to the right of the database selector. Then click the green play button to run the query.[footer:end]
[slide:end]

[slide:start]
[body:start]![Commit the Transaction](/docs/images/studio/project-schema-committed.png)[body:end]
[footer:start]Finally, commit your transaction by clicking the green tick.[footer:end]
[slide:end]

</div>

You'll notice the types view has updated to reflect our schema write once committed.

## Inserting Data

Here's some sample data that complies with our schema.

```typeql
insert $company isa company, has name "Telecom";
insert $person isa person, has phone-number "+7 171 898 0853", has first-name "Melli", has last-name "Winchcum", has city "London", has age 55;
insert $person isa person, has phone-number "+370 351 224 5176", has first-name "Celinda", has last-name "Bonick", has city "London", has age 52;
insert $person isa person, has phone-number "+81 308 988 7153", has first-name "Chryste", has last-name "Lilywhite", has city "London", has age 66;
insert $person isa person, has phone-number "+54 398 559 0423", has first-name "D'arcy", has last-name "Byfford", has city "London", has age 19;
insert $person isa person, has phone-number "+7 690 597 4443", has first-name "Xylina", has last-name "D'Alesco", has city "Cambridge", has age 51;
insert $person isa person, has phone-number "+263 498 495 0617", has first-name "Roldan", has last-name "Cometti", has city "Oxford", has age 59;
insert $person isa person, has phone-number "+63 815 962 6097", has first-name "Cob", has last-name "Lafflin", has city "Cambridge", has age 56;
insert $person isa person, has phone-number "+81 746 154 2598", has first-name "Olag", has last-name "Heakey", has city "London", has age 45;
insert $person isa person, has phone-number "+261 860 539 4754", has first-name "Mandie", has last-name "Assender", has city "London", has age 18;
insert $person isa person, has phone-number "+62 107 530 7500", has first-name "Elenore", has last-name "Stokey", has city "Oxford", has age 35;
insert $person isa person, has phone-number "+86 921 547 9004";
insert $person isa person, has phone-number "+48 894 777 5173";
insert $person isa person, has phone-number "+86 922 760 0418";
insert $person isa person, has phone-number "+33 614 339 0298";
insert $person isa person, has phone-number "+30 419 575 7546";
insert $person isa person, has phone-number "+7 414 625 3019";
insert $person isa person, has phone-number "+57 629 420 5680";
insert $person isa person, has phone-number "+351 515 605 7915";
insert $person isa person, has phone-number "+36 318 105 5629";
insert $person isa person, has phone-number "+63 808 497 1769";
insert $person isa person, has phone-number "+62 533 266 3426";
insert $person isa person, has phone-number "+351 272 414 6570";
insert $person isa person, has phone-number "+86 825 153 5518";
insert $person isa person, has phone-number "+86 202 257 8619";
insert $person isa person, has phone-number "+27 117 258 4149";
insert $person isa person, has phone-number "+48 697 447 6933";
insert $person isa person, has phone-number "+48 195 624 2025";
insert $person isa person, has phone-number "+1 254 875 4647";
insert $person isa person, has phone-number "+7 552 196 4096";
insert $person isa person, has phone-number "+86 892 682 0628";
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+7 171 898 0853"; insert (provider: $company, customer: $customer) isa contract;
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+370 351 224 5176"; insert (provider: $company, customer: $customer) isa contract;
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+81 308 988 7153"; insert (provider: $company, customer: $customer) isa contract;
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+54 398 559 0423"; insert (provider: $company, customer: $customer) isa contract;
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+7 690 597 4443"; insert (provider: $company, customer: $customer) isa contract;
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+263 498 495 0617"; insert (provider: $company, customer: $customer) isa contract;
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+63 815 962 6097"; insert (provider: $company, customer: $customer) isa contract;
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+81 746 154 2598"; insert (provider: $company, customer: $customer) isa contract;
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+261 860 539 4754"; insert (provider: $company, customer: $customer) isa contract;
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+62 107 530 7500"; insert (provider: $company, customer: $customer) isa contract;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T22:24:19; $call has duration 122;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-18T01:34:48; $call has duration 514;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+33 614 339 0298"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T20:21:17; $call has duration 120;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+33 614 339 0298"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T22:10:34; $call has duration 144;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T20:24:59; $call has duration 556;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T22:23:25; $call has duration 336;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+351 272 414 6570"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T05:34:19; $call has duration 405;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+263 498 495 0617"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T22:58:02; $call has duration 5665;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T08:55:18; $call has duration 822;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+54 398 559 0423"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T09:10:25; $call has duration 8494;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+7 414 625 3019"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T20:31:39; $call has duration 12;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+57 629 420 5680"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T10:47:21; $call has duration 29;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+261 860 539 4754"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T06:21:55; $call has duration 2851;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T03:37:06; $call has duration 573;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+1 254 875 4647"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T08:19:36; $call has duration 66;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+63 815 962 6097"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T19:44:03; $call has duration 3682;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T13:27:42; $call has duration 32;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T00:56:31; $call has duration 1434;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+7 414 625 3019"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-18T18:47:17; $call has duration 166;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+86 202 257 8619"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T17:27:52; $call has duration 112;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T03:38:09; $call has duration 1142;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+86 202 257 8619"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T14:57:25; $call has duration 1665;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+86 922 760 0418"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-27T05:08:53; $call has duration 365;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+36 318 105 5629"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T01:44:31; $call has duration 96;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T12:27:48; $call has duration 766;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+27 117 258 4149"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-27T11:28:11; $call has duration 710;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-18T23:24:30; $call has duration 151;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T14:04:33; $call has duration 5710;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+81 308 988 7153"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T04:12:07; $call has duration 9923;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+261 860 539 4754"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T22:54:31; $call has duration 4264;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T21:17:48; $call has duration 202;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T22:55:06; $call has duration 151;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+86 922 760 0418"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T10:16:51; $call has duration 2895;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T15:37:45; $call has duration 251;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T11:34:35; $call has duration 139;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+351 272 414 6570"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T03:13:47; $call has duration 140;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+62 107 530 7500"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T19:18:32; $call has duration 3660;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+30 419 575 7546"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T21:42:00; $call has duration 582;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T01:00:38; $call has duration 141;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T03:16:48; $call has duration 89;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T19:47:20; $call has duration 21;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+48 697 447 6933"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T23:47:19; $call has duration 144;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+86 922 760 0418"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-18T04:54:04; $call has duration 163;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+62 533 266 3426"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T02:11:53; $call has duration 2681;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+36 318 105 5629"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T14:14:42; $call has duration 492;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+351 272 414 6570"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-27T04:00:59; $call has duration 384;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+7 414 625 3019"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T05:58:16; $call has duration 2575;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-27T18:02:22; $call has duration 546;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+1 254 875 4647"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T18:41:52; $call has duration 869;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+36 318 105 5629"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T04:41:12; $call has duration 139;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T06:44:17; $call has duration 53;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-27T12:32:32; $call has duration 457;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-18T03:42:30; $call has duration 157;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T21:20:56; $call has duration 207;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T15:32:57; $call has duration 500;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T23:45:04; $call has duration 30;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T19:17:54; $call has duration 161;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T02:01:08; $call has duration 306;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+57 629 420 5680"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T21:03:04; $call has duration 129;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T07:55:23; $call has duration 594;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T02:24:36; $call has duration 125;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+62 533 266 3426"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T09:21:22; $call has duration 100;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+36 318 105 5629"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T13:00:15; $call has duration 172;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+63 815 962 6097"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T23:11:52; $call has duration 6789;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+48 894 777 5173"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T07:41:23; $call has duration 66;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T17:26:29; $call has duration 950;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+7 414 625 3019"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T23:28:04; $call has duration 144;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+7 171 898 0853"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-27T17:33:06; $call has duration 4868;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+7 171 898 0853"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-15T10:03:34; $call has duration 6298;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T20:26:23; $call has duration 2606;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-28T05:06:44; $call has duration 886;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+54 398 559 0423"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T04:48:41; $call has duration 3458;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+27 117 258 4149"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T22:32:19; $call has duration 609;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T03:50:51; $call has duration 68;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+351 272 414 6570"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T09:20:33; $call has duration 212;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T16:52:29; $call has duration 156;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-18T09:21:38; $call has duration 60;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T22:11:35; $call has duration 681;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T15:12:44; $call has duration 124;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T05:39:03; $call has duration 124;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T18:08:42; $call has duration 163;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+1 254 875 4647"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T13:06:40; $call has duration 45;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+62 107 530 7500"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T05:05:43; $call has duration 3924;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T21:40:47; $call has duration 79;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+48 894 777 5173"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T04:16:21; $call has duration 79;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T03:22:12; $call has duration 988;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+86 202 257 8619"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T00:41:44; $call has duration 164;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+48 697 447 6933"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T18:55:03; $call has duration 212;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+30 419 575 7546"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T15:20:43; $call has duration 283;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+7 690 597 4443"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T00:06:19; $call has duration 2357;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+351 272 414 6570"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T13:27:01; $call has duration 157;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+1 254 875 4647"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-18T07:53:09; $call has duration 295;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+81 746 154 2598"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T07:13:25; $call has duration 9460;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-15T22:08:23; $call has duration 2308;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T02:24:15; $call has duration 1018;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+263 498 495 0617"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T17:22:34; $call has duration 10499;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T18:17:49; $call has duration 47;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T07:29:13; $call has duration 1036;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+81 308 988 7153"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-27T08:22:32; $call has duration 6468;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+33 614 339 0298"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T01:58:04; $call has duration 77;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+263 498 495 0617"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T23:16:49; $call has duration 2519;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+1 254 875 4647"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-15T07:02:32; $call has duration 914;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+81 308 988 7153"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T04:57:20; $call has duration 4455;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+62 107 530 7500"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-28T01:57:20; $call has duration 5272;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+36 318 105 5629"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-14T17:18:49; $call has duration 1111;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+86 922 760 0418"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T21:11:41; $call has duration 290;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T22:57:07; $call has duration 169;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+86 825 153 5518"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T19:43:24; $call has duration 276;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+48 894 777 5173"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T14:43:15; $call has duration 4;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T22:48:50; $call has duration 655;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+48 697 447 6933"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T13:54:54; $call has duration 146;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+30 419 575 7546"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T20:34:51; $call has duration 22;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T21:14:56; $call has duration 1177;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+7 690 597 4443"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T21:01:36; $call has duration 6227;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T11:04:36; $call has duration 67;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+1 254 875 4647"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-15T22:31:03; $call has duration 71;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+86 202 257 8619"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T02:01:36; $call has duration 60;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+86 922 760 0418"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T05:22:05; $call has duration 2544;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+62 107 530 7500"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T18:51:01; $call has duration 7444;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+81 308 988 7153"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T03:49:07; $call has duration 1696;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+54 398 559 0423"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T15:58:58; $call has duration 9465;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+30 419 575 7546"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T17:02:25; $call has duration 442;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+81 746 154 2598"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T16:46:05; $call has duration 3928;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+7 690 597 4443"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T08:11:36; $call has duration 10309;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+62 533 266 3426"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T15:41:04; $call has duration 76;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T01:13:18; $call has duration 997;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+36 318 105 5629"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T08:53:14; $call has duration 90;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T11:47:59; $call has duration 124;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+48 894 777 5173"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-15T21:44:00; $call has duration 1122;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T17:24:29; $call has duration 520;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+62 107 530 7500"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T12:10:49; $call has duration 3251;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+48 697 447 6933"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-28T08:52:06; $call has duration 599;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-18T06:03:28; $call has duration 160;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T19:51:51; $call has duration 79;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+7 171 898 0853"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T12:08:28; $call has duration 6538;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T02:19:22; $call has duration 508;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T00:35:41; $call has duration 809;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T15:16:47; $call has duration 2457;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+33 614 339 0298"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T09:48:54; $call has duration 93;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+54 398 559 0423"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T03:19:40; $call has duration 1259;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+81 746 154 2598"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T08:08:28; $call has duration 6475;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-14T22:01:01; $call has duration 547;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+81 746 154 2598"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T20:04:51; $call has duration 4941;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T03:35:49; $call has duration 134;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+7 171 898 0853"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T11:38:53; $call has duration 9705;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+81 746 154 2598"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-28T00:37:16; $call has duration 6945;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-18T23:25:20; $call has duration 3225;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+62 533 266 3426"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-14T23:33:20; $call has duration 27;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+30 419 575 7546"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T07:52:06; $call has duration 174;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T09:42:58; $call has duration 143;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+63 815 962 6097"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T02:17:35; $call has duration 5413;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+81 308 988 7153"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T06:19:03; $call has duration 3552;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+86 202 257 8619"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T08:28:51; $call has duration 170;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T06:33:20; $call has duration 108;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T10:37:27; $call has duration 556;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+7 414 625 3019"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T11:17:09; $call has duration 1051;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T21:49:34; $call has duration 802;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+62 533 266 3426"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T11:41:10; $call has duration 1903;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+7 414 625 3019"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T15:26:33; $call has duration 175;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+36 318 105 5629"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T06:23:45; $call has duration 166;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+1 254 875 4647"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T04:08:43; $call has duration 501;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T23:50:37; $call has duration 52;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+30 419 575 7546"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T01:11:29; $call has duration 1959;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+48 697 447 6933"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T18:43:42; $call has duration 29;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+86 922 760 0418"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T19:07:10; $call has duration 3196;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+86 202 257 8619"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T06:05:16; $call has duration 4362;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+63 815 962 6097"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T16:57:41; $call has duration 4016;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+86 202 257 8619"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T19:45:03; $call has duration 422;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+48 894 777 5173"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T20:00:30; $call has duration 720;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+86 922 760 0418"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T21:33:26; $call has duration 402;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T06:56:03; $call has duration 44;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+86 922 760 0418"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-28T09:45:40; $call has duration 78;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-27T13:01:03; $call has duration 113;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+57 629 420 5680"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T12:20:01; $call has duration 128;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+36 318 105 5629"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T08:07:59; $call has duration 1171;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+48 697 447 6933"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T19:41:35; $call has duration 126;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T01:48:26; $call has duration 176;
match $caller isa person, has phone-number "+261 860 539 4754"; $callee isa person, has phone-number "+7 690 597 4443"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-14T23:40:40; $call has duration 4389;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+7 414 625 3019"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-17T23:24:18; $call has duration 2391;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+86 922 760 0418"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-15T04:32:48; $call has duration 44;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+86 825 153 5518"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-28T14:57:53; $call has duration 160;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+63 815 962 6097"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T07:34:42; $call has duration 9303;
match $caller isa person, has phone-number "+7 171 898 0853"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T01:37:19; $call has duration 141;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+63 808 497 1769"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-22T08:48:48; $call has duration 83;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+62 533 266 3426"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-15T12:12:59; $call has duration 426;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T14:12:40; $call has duration 51;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+54 398 559 0423"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-21T22:45:47; $call has duration 8861;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+33 614 339 0298"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T22:18:08; $call has duration 162;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+27 117 258 4149"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-25T00:26:05; $call has duration 69;
match $caller isa person, has phone-number "+263 498 495 0617"; $callee isa person, has phone-number "+62 533 266 3426"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T03:03:46; $call has duration 12;
match $caller isa person, has phone-number "+62 107 530 7500"; $callee isa person, has phone-number "+86 892 682 0628"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T14:12:03; $call has duration 68;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+48 195 624 2025"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-26T21:20:35; $call has duration 136;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+86 921 547 9004"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-24T09:38:52; $call has duration 80;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+1 254 875 4647"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-20T12:02:37; $call has duration 9;
match $caller isa person, has phone-number "+81 308 988 7153"; $callee isa person, has phone-number "+48 894 777 5173"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-28T06:12:49; $call has duration 156;
match $caller isa person, has phone-number "+370 351 224 5176"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-16T22:31:25; $call has duration 543;
match $caller isa person, has phone-number "+7 690 597 4443"; $callee isa person, has phone-number "+48 697 447 6933"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T00:12:47; $call has duration 132;
match $caller isa person, has phone-number "+81 746 154 2598"; $callee isa person, has phone-number "+351 515 605 7915"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-19T08:10:14; $call has duration 76;
match $caller isa person, has phone-number "+54 398 559 0423"; $callee isa person, has phone-number "+81 746 154 2598"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-18T22:47:52; $call has duration 5356;
match $caller isa person, has phone-number "+63 815 962 6097"; $callee isa person, has phone-number "+7 552 196 4096"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-09-23T01:14:56; $call has duration 53;
```
<div class="slideshow">

[slide:start]
[body:start]![Create Another New File](/docs/images/studio/project-new-file-2.png)[body:end]
[footer:start]Create another file by clicking the '+' icon again.[footer:end]
[slide:end]

[slide:start]
[body:start]![Paste In The Query](/docs/images/studio/project-data-pasted.png)[body:end]
[footer:start]Copy the above queries into this new file.[footer:end]
[slide:end]

[slide:start]
[body:start]![Run the Query](/docs/images/studio/project-data-query-run.png)[body:end]
[footer:start]Ensure your session and transaction settings are set to `data` and `write` respectively, then click the green play button.[footer:end]
[slide:end]

[slide:start]
[body:start]![Commit the Transaction](/docs/images/studio/project-data-committed.png)[body:end]
[footer:start]Finally, commit your transaction by clicking the green tick.[footer:end]
[slide:end]

</div>

## Query the Data

Everything is in place and we can start writing queries for our data. Open one final file and set your session and transaction types to `data` and `read` respectively.

![Visualise The Data](/docs/images/studio/phone-calls-visualisation.png)
Get a quick visualisation of the data with the following query:
```typeql
match $x isa thing;
``` 
This query gets every attribute, entity and relation.