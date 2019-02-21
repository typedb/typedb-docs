/**
 * The content of codeKeywordsToLink is used to identify keywords in code blocks and turn them into a link
 * that points the user to the relevant documentation on the highlighted keyword.
 *
 * Construction of links per configuration of each keyword object is as follows:
 *      (keyword.baseUrl || codeKeywordsToLink.commonBaseUrl.replace('{client}', keyword.language)) + anchor
 *
 * Properties of a keyword object:
 *   -  baseUrl (optional): required only if the url is not pointed at one if the client pages
 *   -  titles: variants of the keyword. ex: ["undefine"] or ["getSchemaConcept", "get_schema_concept"]
 *   -  syntaxedAs: the keyword will be recognised, only if it's syntax-highlighted as one of the given types
 *          allowed types are: function, graq-keyword, string, uncategorised
 *   -  anchor: the id of the heading, prefixed by #. the corresponding heading is preceded by the comment (!!! synced with codeKeywordsToLink)
 *   -  languages: the keyword, will be recognised, only if it's mentioned in a code block of an given language
 */

codeKeywordsToLink = {
    commonBaseUrl: "/docs/client-api/" + "{client}",
    keywords: [
        // order matters for functionality. keywords that need to turn into a link first. example: undefine before define
        {
            titles: ["undefine"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-manipulate-the-schema-programatically",
            languages: ["java"]
        },
        {
            titles: ["undefine"],
            baseUrl: "/docs/schema/concepts",
            syntaxedAs: ["graql-keyword", "string"],
            anchor: "#undefine",
            languages: ["graql", "javascript", "python"]
        },
        {
            titles: ["getAttributesByValue", "get_attributes_by_value"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-retrieve-an-attribute-by-value",
            languages: ["javascript", "python"]
        },
        {
            titles: ["getConcept", "get_concept"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-retrieve-a-concept-by-id",
            languages: ["javascript", "python"]
        },
        {
            titles: ["getSchemaConcept", "get_schema_concept"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-retrieve-a-schema-concept-by-label",
            languages: ["javascript", "python"]
        },
        {
            titles: ["getSchemaConcept", "get_schema_concept"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-retrieve-a-schema-concept-by-label",
            languages: ["javascript", "python"]
        },
        {
            titles: ["queryPattern", "query_pattern"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-retrieve-a-graql-explanation-of-the-answer",
            languages: ["javascript", "python"]
        },
        // alphabetic order only required for readability
        {
            titles: ["aggregate"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-aggregatd-values",
            languages: ["java"]
        },
        {
            titles: ["aggregate"],
            baseUrl: "/docs/query/aggregate-query",
            syntaxedAs: ["graql-keyword", "string"],
            anchor: "",
            languages: ["graql", "javascript", "python"]
        },
        {
            titles: ["answerIterator", "answer_iterator", "Iterator", "iterator"],
            syntaxedAs: ["uncategorised"],
            anchor: "#client-api-title-iterator",
            languages: ["javascript", "python"]
        },
        {
            titles: ["answers"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-retrieve-source-facts-of-inference",
            languages: ["javascript", "python"]
        },
        {
            titles: ["collectConcepts", "collect_concepts"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-consume-the-iterator-eagerly",
            languages: ["javascript", "python"]
        },
        {
            titles: ["commit"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-commit-a-write-transaction",
            languages: ["java", "javascript", "python"]
        },
        {
            titles: ["compute"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-compute-values",
            languages: ["java"]
        },
        {
            titles: ["compute"],
            baseUrl: "/docs/query/compute-query",
            syntaxedAs: ["graql-keyword", "string"],
            anchor: "",
            languages: ["graql", "javascript", "python"]
        },
        {
            titles: ["ConceptMap", "concept_map", "conceptMap"],
            syntaxedAs: ["uncategorised"],
            anchor: "#client-api-title-conceptmap",
            languages: ["java", "javascript", "python"]
        },
        {
            titles: ["define"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-manipulate-the-schema-programatically",
            languages: ["java"]
        },
        {
            titles: ["define"],
            baseUrl: "/docs/schema/concepts",
            syntaxedAs: ["graql-keyword", "string"],
            anchor: "#define",
            languages: ["graql", "javascript", "python"]
        },
        {
            titles: ["delete"],
            baseUrl: "/docs/query/delete-query",
            syntaxedAs: ["graql-keyword", "string"],
            anchor: "",
            languages: ["graql", "javascript", "python"]
        },
        {
            titles: ["explanation"],
            syntaxedAs: ["function"],
            anchor: "#client-api-title-explanation",
            languages: ["java", "javascript", "python"]
        },
        {
            titles: ["execute"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-eagerly-execute-of-a-graql-query",
            languages: ["java"]
        },
        {
            titles: ["get"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-retrieve-data-instances",
            languages: ["java"]
        },
        {
            titles: ["get"],
            baseUrl: "/docs/query/get-query",
            syntaxedAs: ["graql-keyword", "string"],
            anchor: "",
            languages: ["graql", "javascript", "python"]
        },
        {
            titles: ["Graql"],
            syntaxedAs: ["uncategorised"],
            anchor: "#client-api-title-graql",
            languages: ["java"]
        },
        {
            baseUrl: "/docs/query/delete-query",
            titles: ["delete"],
            syntaxedAs: ["graql-keyword", "string"],
            anchor: "",
            languages: ["graql", "javascript", "python"]
        },
        {
            titles: ["insert"],
            baseUrl: "/docs/query/insert-query",
            syntaxedAs: ["graql-keyword", "string"],
            anchor: "",
            languages: ["graql", "javascript", "python"]
        },
        {
            titles: ['insert'],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-insert-data-instances",
            languages: ["java"]
        },
        {
            titles: ["match"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-match-patterns-in-data",
            languages: ["java"]
        },
        {
            titles: ["match"],
            baseUrl: "/docs/query/match-clause",
            syntaxedAs: ["graql-keyword", "string"],
            anchor: "",
            languages: ["graql", "javascript", "python"]
        },
        {
            titles: ["measurement"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-retrieve-the-numeric-value-of-a-centrality-computation",
            languages: ["java", "javascript", "python"]
        },
        {
            titles: ["owner"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-retrieve-the-concept-that-is-the-group-owner",
            languages: ["java", "javascript", "python"]
        },
        {
            titles: ["putAttributeType", "put_attribute_type"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-create-or-retrieve-an-attributetype",
            languages: ["java", "javascript", "python"]
        },
        {
            titles: ["putEntityType", "put_entity_type"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-create-or-retrieve-an-entitytype",
            languages: ["javascript", "python"]
        },
        {
            titles: ["putRelationshipType", "put_relationship_type"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-create-or-retrieve-a-relationshiptype",
            languages: ["javascript", "python"]
        },
        {
            titles: ["putRole", "put_role"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-create-or-retrieve-a-role",
            languages: ["javascript", "python"]
        },
        {
            titles: ["putRule", "put_rule"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-create-or-retrieve-a-rule",
            languages: ["javascript", "python"]
        },
        {
            titles: ["query"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-lazily-execute-a-graql-query",
            languages: ["javascript", "python"]
        },
        {
            titles: ["rule"],
            baseUrl: "/docs/schema/rules",
            syntaxedAs: ["graql-keyword", "string"],
            anchor: "",
            languages: ["graql", "javascript", "python"],
        },
        {
            titles: ["session"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-create-a-session-keyspace",
            languages: ["java", "javascript", "python"]
        },
        {
            titles: ["stream"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-lazily-execute-of-a-graql-query",
            languages: ["java"]
        },
        {
            titles: ["transaction"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-create-a-transaction",
            languages: ["java", "javascript", "python"]
        },
        {
            titles: ["withTx"],
            syntaxedAs: ["function"],
            anchor: "#client-api-method-attach-transaction-to-query",
            languages: ["java"]
        },
    ]
}