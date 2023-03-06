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
    "commonBaseUrl": "/docs/clients/{client}",
    "keywords": [
        // order matters for functionality. keywords that need to turn into a link first. example: undefine before define
        {
            "titles": ["undefine"],
            "baseUrl": "../schema/concepts",
            "syntaxedAs": ["typeql-keyword", "string"],
            "anchor": "#undefine",
            "languages": ["typeql",  "java", "javascript", "python"]
        },
        // alphabetic order only required for readability
        {
            "titles": ["count", "sum", "min", "max", "mean", "median", "std"],
            "baseUrl": "../query/aggregate-query",
            "syntaxedAs": ["function", "typeql-keyword", "string"],
            "anchor": "",
            "languages": ["typeql", "java", "javascript", "python"]
        },
        {
            "titles": ["commit"],
            "syntaxedAs": ["function"],
            "anchor": "#commit-a-write-transaction",
            "languages": ["java", "javascript", "python"]
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
            "syntaxedAs": ["function", "typeql-keyword", "string"],
            "anchor": "#define",
            "languages": ["typeql", "java", "javascript", "python"]
        },
        {
            "titles": ["delete"],
            "baseUrl": "../query/delete-query",
            "syntaxedAs": ["function", "typeql-keyword", "string"],
            "anchor": "",
            "languages": ["typeql", "java", "javascript", "python"]
        },
        {
            "titles": ["execute"],
            "syntaxedAs": ["function"],
            "anchor": "",
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
            "syntaxedAs": ["function", "typeql-keyword", "string"],
            "anchor": "",
            "languages": ["typeql", "java", "javascript", "python"]
        },
        {
            "titles": ["TypeQL"],
            "syntaxedAs": ["uncategorised"],
            "anchor": "#typeql",
            "languages": ["java"]
        },
        {
            "titles": ["insert"],
            "baseUrl": "../query/insert-query",
            "syntaxedAs": ["function", "typeql-keyword", "string"],
            "anchor": "",
            "languages": ["typeql", "java", "javascript", "python"]
        },
        {
            "titles": ["match"],
            "baseUrl": "../query/match-clause",
            "syntaxedAs": ["function", "typeql-keyword", "string"],
            "anchor": "",
            "languages": ["typeql", "java", "javascript", "python"]
        },
        {
            "titles": ["owner"],
            "syntaxedAs": ["function"],
            "anchor": "#retrieve-the-concept-that-is-the-group-owner",
            "languages": ["java", "javascript", "python"]
        },
        {
            "titles": ["rule"],
            "baseUrl": "../schema/rules",
            "syntaxedAs": ["typeql-keyword", "string"],
            "anchor": "",
            "languages": ["typeql", "javascript", "python"],
        },
    ]
}
