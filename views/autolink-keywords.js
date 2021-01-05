/**
 * The content of codeKeywordsToLink is used to identify keywords in code blocks and turn them into a link
 * that points the user to the relevant documentation on the highlighted keyword.
 *
 * Construction of links per configuration of each keyword object is as follows:
 *      (keyword.baseUrl || codeKeywordsToLink.commonBaseUrl.replace('{client}', keyword.language)) + anchor
 *
 * Properties of a keyword object:
 *   -  baseUrl (optional): required only if the url is not pointed at one if the client pages
 *   -  "titles": variants of the keyword. ex: ["undefine"] or ["getSchemaConcept", "get_schema_concept"]
 *   -  syntaxedAs: the keyword will be recognised, only if it's syntax-highlighted as one of the given types
 *          allowed types are: function, graq-keyword, string, uncategorised
 *   -  anchor: the id of the heading, prefixed by #. the corresponding heading is preceded by the comment (!!! synced with codeKeywordsToLink)
 *   -  languages: the keyword, will be recognised, only if it's mentioned in a code block of an given language
 */

codeKeywordsToLink = {
    "commonBaseUrl": "/docs/client-api/{client}",
    "keywords": [
        // order matters for functionality. keywords that need to turn into a link first. example: undefine before define
        {
            "titles": ["undefine"],
            "baseUrl": "../schema/concepts",
            "syntaxedAs": ["graql-keyword", "string"],
            "anchor": "#undefine",
            "languages": ["graql",  "java", "javascript", "python"]
        },
        {
            "titles": ["getAttributesByValue", "get_attributes_by_value"],
            "syntaxedAs": ["function"],
            "anchor": "#retrieve-an-attribute-by-value",
            "languages": [ "java", "javascript", "python"]
        },
        {
            "titles": ["getConcept", "get_concept"],
            "syntaxedAs": ["function"],
            "anchor": "#retrieve-a-concept-by-id",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["getSchemaConcept", "get_schema_concept"],
            "syntaxedAs": ["function"],
            "anchor": "#retrieve-a-schema-concept-by-label",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["queryPattern", "query_pattern", "getPattern"],
            "syntaxedAs": ["function"],
            "anchor": "#query-pattern-that-leads-to-the-conceptmap",
            "languages": ["java", "javascript", "python"]
        },
        // alphabetic order only required for readability
        {
            "titles": ["count", "sum", "min", "max", "mean", "median", "std"],
            "baseUrl": "../query/aggregate-query",
            "syntaxedAs": ["function", "graql-keyword", "string"],
            "anchor": "",
            "languages": ["graql", "java", "javascript", "python"]
        },
        {
            "titles": ["answerIterator", "answer_iterator", "Iterator", "iterator"],
            "syntaxedAs": ["uncategorised"],
            "anchor": "#iterator",
            "languages": ["javascript", "python"]
        },
        {
            "titles": ["answers", "getAnswers"],
            "syntaxedAs": ["function"],
            "anchor": "#retrieve-source-facts-of-inference",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["collectConcepts"],
            "syntaxedAs": ["function"],
            "anchor": "#consume-the-iterator-eagerly",
            "languages": ["javascript"]
        },
        {
            "titles": ["commit"],
            "syntaxedAs": ["function"],
            "anchor": "#commit-a-write-transaction",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["compute"],
            "baseUrl": "../query/compute-query",
            "syntaxedAs": ["function", "graql-keyword", "string"],
            "anchor": "#compute-statistics",
            "languages": ["graql", "java", "javascript", "python"]
        },
        {
            "titles": ["ConceptMap", "concept_map", "conceptMap"],
            "syntaxedAs": ["uncategorised"],
            "anchor": "#conceptmap",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["define"],
            "baseUrl": "../schema/concepts",
            "syntaxedAs": ["function", "graql-keyword", "string"],
            "anchor": "#define",
            "languages": ["graql", "java", "javascript", "python"]
        },
        {
            "titles": ["delete"],
            "baseUrl": "../query/delete-query",
            "syntaxedAs": ["function", "graql-keyword", "string"],
            "anchor": "",
            "languages": ["graql", "java", "javascript", "python"]
        },
        {
            "titles": ["explanation"],
            "syntaxedAs": ["function"],
            "anchor": "#explanation",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["execute"],
            "syntaxedAs": ["function"],
            "anchor": "#eagerly-execute-a-graql-query",
            "languages": ["java"]
        },
        {
            "titles": ["get"],
            "baseUrl": "../query/get-query",
            "syntaxedAs": ["function"],
            "anchor": "",
            "languages": ["java"]
        },
        {
            "titles": ["get"],
            "baseUrl": "../query/get-query",
            "syntaxedAs": ["function", "graql-keyword", "string"],
            "anchor": "",
            "languages": ["graql", "java", "javascript", "python"]
        },
        {
            "titles": ["Graql"],
            "syntaxedAs": ["uncategorised"],
            "anchor": "#graql",
            "languages": ["java"]
        },
        {
            "titles": ["insert"],
            "baseUrl": "../query/insert-query",
            "syntaxedAs": ["function", "graql-keyword", "string"],
            "anchor": "",
            "languages": ["graql", "java", "javascript", "python"]
        },
        {
            "titles": ["isOpen", "is_open"],
            "syntaxedAs": ["function"],
            "anchor": "#checks-if-the-transaction-is-open",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["match"],
            "baseUrl": "../query/match-clause",
            "syntaxedAs": ["function", "graql-keyword", "string"],
            "anchor": "",
            "languages": ["graql", "java", "javascript", "python"]
        },
        {
            "titles": ["measurement"],
            "syntaxedAs": ["function"],
            "anchor": "#retrieve-the-numeric-value-of-a-centrality-computation",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["owner"],
            "syntaxedAs": ["function"],
            "anchor": "#retrieve-the-concept-that-is-the-group-owner",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["putAttributeType", "put_attribute_type"],
            "syntaxedAs": ["function"],
            "anchor": "#create-or-retrieve-an-attributetype",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["putEntityType", "put_entity_type"],
            "syntaxedAs": ["function"],
            "anchor": "#create-or-retrieve-an-entitytype",
            "languages": ["javascript", "python"]
        },
        {
            "titles": ["putRelationType", "put_relation_type"],
            "syntaxedAs": ["function"],
            "anchor": "#create-or-retrieve-a-relationtype",
            "languages": ["javascript", "python"]
        },
        {
            "titles": ["putRole", "put_role"],
            "syntaxedAs": ["function"],
            "anchor": "#create-or-retrieve-a-role",
            "languages": ["javascript", "python"]
        },
        {
            "titles": ["putRule", "put_rule"],
            "syntaxedAs": ["function"],
            "anchor": "#create-or-retrieve-a-rule",
            "languages": ["javascript", "python"]
        },
        {
            "titles": ["query"],
            "syntaxedAs": ["function"],
            "anchor": "#lazily-execute-a-graql-query",
            "languages": ["javascript", "python"]
        },
        {
            "titles": ["rule"],
            "baseUrl": "../schema/rules",
            "syntaxedAs": ["graql-keyword", "string"],
            "anchor": "",
            "languages": ["graql", "javascript", "python"],
        },
        {
            "titles": ["session"],
            "syntaxedAs": ["function"],
            "anchor": "#create-a-sessiondatabase",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["transaction().read()"],
            "syntaxedAs": ["function"],
            "anchor": "#open-a-read-transaction",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["transaction().write()"],
            "syntaxedAs": ["function"],
            "anchor": "#open-a-write-transaction",
            "languages": ["java", "javascript", "python"]
        }
    ]
}
