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
Once you launch studio, head to the top right-hand corner and click 'Connect to TypeDB'.

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
[footer:start]This is the database manager. Enter your database name then hit create. For the purposes of this example, we will use the name `github`.[footer:end]
[slide:end]

[slide:start]
[body:start]![Database Manager With GitHub Database](/docs/images/studio/databases-interface-github-database.png)[body:end]
[footer:start]Now you've successfully created a database named `github`![footer:end]
[slide:end]
</div>

Select the database you just created by clicking the dropdown menu titled 'Select Databases' immediately right of the databases icon.

[//]: # (<img height='1em' width='1em' src="/docs/images/studio/databases-icon.png"></img>.)

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
You may have noticed that now you have connected to TypeDB and open a project folder, Studio has sprung to life. Now we need to write a 'schema' to our database. 
You can learn more about what a schema is and how to write one [here](/docs/schema/overview). In short, a schema is a description of the structure of your data and how various entities relate to each other.

For now, we've got a pre-made schema for you to use. We've also got data and queries for this later, so keep following along if you want to get the full experience from this guide.

```typeql
define
    repo-id sub attribute,
        value long;
    repo-name sub attribute,
        value string;
    repo-description sub attribute,
        value string;
    
    commit-hash sub attribute,
        value string;
    commit-message sub attribute,
        value string;
    commit-date sub attribute,
        value string;
    
    user-name sub attribute,
        value string;

    file-name sub attribute,
        value string;

    repo-file sub relation,
        relates file,
        relates repo;
    
    repo-creator sub relation,
        relates repo,
        relates owner;

    commit-author sub relation,
        relates author,
        relates commit;

    commit-file sub relation,
        relates file,
        relates commit;

    commit-repo sub relation,
        relates commit,
        relates repo;

    file-collaborator sub relation,
        relates file,
        relates collaborator;

    repo sub entity,
        plays commit-repo:repo,
        plays repo-creator:repo,
        plays repo-file:repo,
        owns repo-id,
        owns repo-name,
        owns repo-description;
    
    commit sub entity,
        plays commit-author:commit,
        plays commit-file:commit,
        plays commit-repo:commit,
        owns commit-hash,
        owns commit-date;

    user sub entity,
        plays commit-author:author,
        plays repo-creator:owner,
        plays file-collaborator:collaborator,
        owns user-name;

    file sub entity,
        plays repo-file:file,
        plays commit-file:file,
        plays file-collaborator:file,
        owns file-name;

    rule file-collaborator-rule:
        when
    	{
            (file: $f, commit: $c) isa commit-file;
            (commit: $c, author: $a) isa commit-author;
        }
    	then
    	{
            (file: $f, collaborator: $a) isa file-collaborator;
    	};
```

If you're familiar with GitHub, parts of this schema should make sense to you. If not, the basics are: 
- A `repo` (also known as a repository) is a place where files, generally code, are stored.  It has an id, a name, a description, an author and contains a number of files and commits.
- A `commit` is a change to the contained files and that has a hash (a piece of text derived from those changes and a few other details) and a date as well as a relation to the repo it was made in, the files it touched and its author.
- A `file` is a file. It has a name and a relation to the repo it was made in, the commits it was touched by and the users that have collaborated on it.

Now, lets write this schema to our newly created database.

<div class="slideshow">

[slide:start]
[body:start]![Create a New File](/docs/images/studio/project-new-file.png)[body:end]
[footer:start]Create a new file by clicking the '+' icon in the section right of the project view. It should look like this.[footer:end]
[slide:end]

[slide:start]
[body:start]![Paste in Our Schema](/docs/images/studio/project-new-file-with-schema.png)[body:end]
[footer:start]Copy the above schema and paste it into this file.[footer:end]
[slide:end]

[slide:start]
[body:start]![Write the Schema](/docs/images/studio/project-new-file-query-run.png)[body:end]
[footer:start]Now, make sure your session and transaction types are set to `schema` and `write` respectively. These can be found to the right of the database selector. Then click the green play button to run the query.[footer:end]
[slide:end]

[slide:start]
[body:start]![Commit the Transaction](/docs/images/studio/studio-schema-committed.png)[body:end]
[footer:start]Finally, commit your transaction by clicking the green tick.[footer:end]
[slide:end]

</div>

You'll notice the types view has updated to reflect our schema write once committed.

## Inserting Data

Here's some data concerning [vaticle/typedb-behaviour](https://github.com/vaticle/typedb-behaviour).

```typeql
insert $user isa user, has user-name "dmitrii-ubskii";
insert $user isa user, has user-name "lolski";
insert $user isa user, has user-name "vaticle";
insert $user isa user, has user-name "jmsfltchr";
insert $user isa user, has user-name "krishnangovindraj";
insert $user isa user, has user-name "haikalpribadi";
match $user isa user, has user-name "vaticle"; insert $repo isa repo, has repo-id 208812506, has repo-name "typedb-behaviour", has repo-description "TypeDB Behaviour Test Specification"; $repo-creator(repo: $repo, owner: $user) isa repo-creator; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "concept/type/relationtype.feature"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "concept/type/entitytype.feature"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "typeql/language/undefine.feature"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "typeql/language/define.feature"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "dependencies/vaticle/repositories.bzl"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "typeql/language/rule-validation.feature"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "typeql/reasoner/relation-inference.feature"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "typeql/reasoner/schema-queries.feature"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "concept/type/attributetype.feature"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "typeql/reasoner/negation.feature"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $repo isa repo, has repo-name "typedb-behaviour"; insert $file isa file, has file-name "typeql/reasoner/variable-roles.feature"; $repo-file(repo: $repo, file: $file) isa repo-file; 
match $author isa user, has user-name "krishnangovindraj"; $repo isa repo, has repo-name "typedb-behaviour"; insert $commit isa commit, has commit-hash "8c92af7cd6dd6fc84dc7238cd7ddf0748d5531b1", has commit-date "Wed Jun 08 17:13:09 BST 2022"; $commit-author(commit: $commit, author: $author) isa commit-author; $commit-repo(commit: $commit, repo: $repo) isa commit-repo; 
match $file isa file, has file-name "typeql/reasoner/negation.feature"; $commit isa commit, has commit-hash "8c92af7cd6dd6fc84dc7238cd7ddf0748d5531b1";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $author isa user, has user-name "lolski"; $repo isa repo, has repo-name "typedb-behaviour"; insert $commit isa commit, has commit-hash "e3efb4813cd4baa7b80d976045fd1c81ffdf81ca", has commit-date "Fri Jun 03 16:12:45 BST 2022"; $commit-author(commit: $commit, author: $author) isa commit-author; $commit-repo(commit: $commit, repo: $repo) isa commit-repo; 
match $file isa file, has file-name "dependencies/vaticle/repositories.bzl"; $commit isa commit, has commit-hash "e3efb4813cd4baa7b80d976045fd1c81ffdf81ca";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $author isa user, has user-name "jmsfltchr"; $repo isa repo, has repo-name "typedb-behaviour"; insert $commit isa commit, has commit-hash "2a712c4470ccaaaa9f8d7aa5f70b114385c0a47a", has commit-date "Wed May 25 12:03:18 BST 2022"; $commit-author(commit: $commit, author: $author) isa commit-author; $commit-repo(commit: $commit, repo: $repo) isa commit-repo; 
match $file isa file, has file-name "typeql/language/rule-validation.feature"; $commit isa commit, has commit-hash "2a712c4470ccaaaa9f8d7aa5f70b114385c0a47a";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $file isa file, has file-name "typeql/reasoner/negation.feature"; $commit isa commit, has commit-hash "2a712c4470ccaaaa9f8d7aa5f70b114385c0a47a";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $file isa file, has file-name "typeql/reasoner/relation-inference.feature"; $commit isa commit, has commit-hash "2a712c4470ccaaaa9f8d7aa5f70b114385c0a47a";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $file isa file, has file-name "typeql/reasoner/schema-queries.feature"; $commit isa commit, has commit-hash "2a712c4470ccaaaa9f8d7aa5f70b114385c0a47a";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $file isa file, has file-name "typeql/reasoner/variable-roles.feature"; $commit isa commit, has commit-hash "2a712c4470ccaaaa9f8d7aa5f70b114385c0a47a";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $author isa user, has user-name "dmitrii-ubskii"; $repo isa repo, has repo-name "typedb-behaviour"; insert $commit isa commit, has commit-hash "6e462bcbef73c75405264777069a22bca696a644", has commit-date "Tue May 24 13:03:09 BST 2022"; $commit-author(commit: $commit, author: $author) isa commit-author; $commit-repo(commit: $commit, repo: $repo) isa commit-repo; 
match $file isa file, has file-name "concept/type/attributetype.feature"; $commit isa commit, has commit-hash "6e462bcbef73c75405264777069a22bca696a644";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $file isa file, has file-name "concept/type/entitytype.feature"; $commit isa commit, has commit-hash "6e462bcbef73c75405264777069a22bca696a644";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $file isa file, has file-name "concept/type/relationtype.feature"; $commit isa commit, has commit-hash "6e462bcbef73c75405264777069a22bca696a644";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $author isa user, has user-name "haikalpribadi"; $repo isa repo, has repo-name "typedb-behaviour"; insert $commit isa commit, has commit-hash "184bc8a64aa69e383bf496c70b11f02201d33616", has commit-date "Fri May 13 20:24:46 BST 2022"; $commit-author(commit: $commit, author: $author) isa commit-author; $commit-repo(commit: $commit, repo: $repo) isa commit-repo; 
match $file isa file, has file-name "typeql/language/define.feature"; $commit isa commit, has commit-hash "184bc8a64aa69e383bf496c70b11f02201d33616";insert $commit-file(commit: $commit, file: $file) isa commit-file;
match $file isa file, has file-name "typeql/language/undefine.feature"; $commit isa commit, has commit-hash "184bc8a64aa69e383bf496c70b11f02201d33616";insert $commit-file(commit: $commit, file: $file) isa commit-file;
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

Everything is in place and we can start writing queries for our data. Open one final file and set your session and transaction settings to `data` and `read` respectively.

Also ensure that you have turned `infer` on to ensure that rules get resolved. This typically increases the time that queries take to resolve, so it is not enabled by default. However, our schema and queries use a rule.


![Visualise The Data](/docs/images/studio/git-visualisation.png)
Get a quick visualisation of the data with the following query:
```typeql
match $x isa thing;
``` 
This query gets every attribute, entity and relation.


![Query The Data](/docs/images/studio/query-visualisation.png)
Use the following example query to find users who have worked on `negation.feature`: 
```typeql
match $file isa file, has file-name "typeql/reasoner/negation.feature"; 
$file-collaborator(file: $file, collaborator: $c) isa file-collaborator; 
$c has user-name $user-name;
```
