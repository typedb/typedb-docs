# Vaticle Documentation

[![Netlify Status](https://api.netlify.com/api/v1/badges/e8d3d72a-dcb6-4e31-bfc5-deb4e665d083/deploy-status)](https://app.netlify.com/sites/typedb-docs/deploys)
[![Discord](https://img.shields.io/discord/665254494820368395?color=7389D8&label=chat&logo=discord&logoColor=ffffff)](https://typedb.com/discord)
[![Discussion Forum](https://img.shields.io/discourse/https/forum.typedb.com/topics.svg)](https://forum.typedb.com/)
[![Stack Overflow](https://img.shields.io/badge/stackoverflow-typedb-796de3.svg)](https://stackoverflow.com/questions/tagged/typedb)
[![Stack Overflow](https://img.shields.io/badge/stackoverflow-typeql-3dce8c.svg)](https://stackoverflow.com/questions/tagged/typeql)

This repository contains all content that powers the Vaticle Documentation Portal, accessible at [https://typedb.com/docs](https://typedb.com/docs).

---

## Contribute

- Read the [Contribution Guidelines](#contribution-guidelines) carefully.
- Fork this repository.
- Make the desired changes.
- Issue pull request(s) and select the `base` branch in accordance with the [Branches](#branches) section.

---

## Branches

At any given time, this repository has at least two branches, i.e. `master` and `development`.

The `master` branch contains the content for the published documentation, available at the
[Documentation portal](https://typedb.com/docs).

The `development` branch contains the content of the documentation to be published soon, 
available at the [staging environment](https://development.typedb.com/docs).

Main workflow is to merge changes to the `development` branch, test them in the staging environment, 
and publish to production by cherry-picking the changes to the `master` branch.

Hot fixes can be merged directly to the `master` branch, and then cherry-picked into the `development` branch.

---

## Contribution Guidelines

Use Asciidoc syntax with Antora to write content.

- [Naming Conventions](#naming-conventions)
- [Using Images](#using-images)
- [Writing Style](#writing-style)

### Naming Conventions

**Files and directories**

- Separate words with hyphens (`-`).
- Keep file and directory names compact: in most cases, one or two words that best describe the contained content. 
  Never use more than three words unless the file is a tutorial page or a Studio screenshot.
- Choosing the same name for different files located in different directories is acceptable. 
  For example: `files/social-network/schema.tql` and `files/phone-calls/schema.tql`.
- For naming images, refer to the [Images Guidelines](#using-images).

**Headlines**

- Headlines should be phrased in a way that when read the user can determine the question that the text is meant to 
  answer. They should describe a use-case.
- Use primitive verbs (eg: _Manage Databases_ as opposed to _Managing Databases_) or _Database Management_.

### Using Images

- The name of directories placed under `images/`, corresponds to the name of the section as displayed in the sidebar.
- Name of images, while remaining concise, should be to some level descriptive of their content.
  For example: `compute_path.png` and `compute_path_subgraph.png` as opposed to `compute_0.png` and `compute_1.png`.
- When an image is used across multiple pages, the **same** image file should be referenced, rather than duplicating 
  the image.
- The source file used to generate an image is to be located under `images/source/<section-name>`.
- The source file must always contain the latest changes present in its corresponding image.
- Screenshots of Studio should be:
  - named after the UI/UX components of the software itself. (eg: `typeql-editor_clear-query.png`).
  - taken at the screen resolution of 1280 x 720 pixels.
  - of size, 1147 x 671 pixels.
  - consistent in their paddings (position of Studio's layout within the screenshot).

### Writing Style

**Spelling**

Use American.

**Headings**
- There are multiple levels of headings used across all markdown files:
  - h1 (`=`) — page title. Only one per page at the very beginning.
  - h2 (`==`)
  - h3 (`===`)
  - h4 (`====`)
- Use sentence case.
- `====` always comes after a `===` which always comes after a `==`.

**Verbs and Pronouns**

- With rare exceptions, the consistent tense used should be the present tense. 
  For example: _It returns_ as opposed to _It will return_.
- In most cases, the consistent pronoun is `we`. In special cases, `you` may better convey the message. Never use `I`.
- When speaking of the characteristics or capabilities of TypeDB and TypeQL or any of their components, the subject 
  pronoun, if used, should be within the terminology, as opposed to `we`. (eg: _TypeQL_ has three types of statements, 
  as opposed to _We_ have three types of statements)

**Lists (Bullet points)**

- Have an introductory sentence before the list, when possible. End the introductory sentence with a colon (`:`).
- List elements should be similar to each other as much as possible. That includes using same words, word order, 
  punctuation, elements format, etc.
- When the list item completes the unfinished sentence before the list, end the list item with a period and start each
  item in lowercase.
- When the concatenation of list items construct one long sentence, end each list items with a comma or a semicolon 
  with the last one ending with a period and start each item in lowercase.
- If the item consists of a single word, don't add end punctuation.
- If the item is a short phrase that doesn't include a verb, don't add end punctuation.
- If the item is entirely in code font, don't add end punctuation.
- If the item is entirely link text or a document title, don't add end punctuation.
- In cases other than the two described above, start the item with a capital letter and end the item with a full 
  stop.

**Serial comma**

- Use serial (aka Oxford) comma.

**Footer Notes and Captions**
- When using a phrase, do not end the line with a period (eg: `Computation of shortest path in Studio`).
- When using a sentence, end the line with a period. `Click on the plus icon to add a new tab.`.

**Formulations**
- Use paragraphs to provide clarity and flow.
- First sentence should describe the content of the entire paragraph at a high level.
- Avoid placing critical information in the middle or end of long paragraphs.
- Keep paragraphs short (up to 4 lines), when possible.
- Prefer short sentences to long ones. Only use complex sentence structures (multiple sentences divided by `,`, `;` 
  or `-`), as last resort.
- Keep sentences concise. If a part of a sentence is adding no value to the point that the sentence is meant to deliver, 
  remove it.
- Avoid the assumption that a sentence is self-explanatory. Even if explained in an earlier sentence, repeat yourself 
  to ensure the sentence can be well-understood, without requiring reference to an earlier text.

### Cross-referencing
Most of the time, when we mention something that is explained in a previous or next page, we need to leave a reference 
(by turning the word or phrase into a link) to that page and sometimes to a particular heading.

### Flow and Headings
The choice and order of headings should provide the reader with a seamless flow that offers a high-level understanding 
of what that page is about. By doing this, we would also make it easier for the readers to find what they are looking 
for, if that is why they are visiting the page.

Every heading is turned into an anchor, which in turn:
- provides visitors with a table of content, that is essentially the summary of the page.
- enables cross-referencing one or more words to a specific block of text on the same or other pages.
- allows the community to leave references to specific parts of the docs when providing answers or suggestions on 
  different platforms.

### Keywords
All terminologies used within a page almost always need to be included as the keywords in the front matter of the 
markdown file.
The `keywords` attribute contains a comma-separated list of single-word keywords and/or multiple words that are 
expected to be searched in combination.
The `longTailKeywords` attribute contains a comma-separated list of keywords that form sensible combinations of the 
keyword items. They may also be any phrase that the user may search which relates to the page.

<!-- **TypeDB Terminology**

**Common Terms** -->
