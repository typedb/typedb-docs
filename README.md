# Vaticle Documentation

[![CircleCI](https://circleci.com/gh/vaticle/docs/tree/master.svg?style=shield)](https://circleci.com/gh/vaticle/docs)

This repository contains all content that powers the Vaticle Documentation Portal, accessible at [docs.vaticle.com](http://docs.vaticle.com).

---

## Contribute

- Fork this repository.
- Read the [Contribution Guidelines](#contribution-guidelines) carefully.
- Make the desired changes.
- Issue pull request(s) and select the `base` branch in accordance with the [Branch Classifications](#branch-classifications).

---

## Branches

At any given time, this repository has at least 1 and at most 2 branches, i.e. `master` and `development`.

### Master Branch

The master branch contains the content for the live documentation of the current release. Unless the changes to be made in docs, are with regards to the documentation of a new feature that is yet to be released, they are all meant to be made on the _master_ branch.

If at the time of submitting changes to _master_, the _development_ is also present, then changes made on the master branch need to be made on the development branch as well. To avoid bring unwanted changes to the development branch, commits need to be cherry-picked for the PR with _development_ as its base. The steps to accomplish this are as follows.

1. `git checkout development`
2. `git pull <name of the vaticle/docs remote> development`
3. `git checkout -b <name of the branch to be the head of the upcoming PR>`
4. `git cherry-pick <SHA of the commit that represents the beginning of changes in the previous (master) PR>..<SHA of the commit that represents the end of changes in previous (master) PR>`
5. commit any other changes that are exclusive for the next release
5. `git push <name of the fork remote> <name of the current branch>`
6. issue the PR and select `development` as the _base_ branch

### Development Branch

The development branch contains the content of the documentation for the next immediate release.
PRs that have the `development` branch as their _base_, contains changes that are either:
- previously made on `master` and should also be reflected for the next release, or
- meant to introduce a new future/change that will only be available as a part of the next release

---

## Contribution Guidelines

- [Naming Conventions](#naming-conventions)
- [Using Images](#using-images)
- [Writing Style](#writing-style)
- [Writing Markdown](#writing-markdown)
- [API References](#api-references)
- [Tests](#tests)

### Naming Conventions

**Files and directories**

- Separate words with hyphens (`-`).
- Keep file and directory names compact: in most cases, one or two words that best describe the contained content. Never use more than three words unless the file is a tutorial page or a Studio screenshot.
- Choosing the same name for different files located in different directories is acceptable. (eg: `files/social-network/schema.tql` and `files/phone-calls/schema.tql`).
- For naming images, refer to the [Images Guidelines](#images).

**Headlines**

- Headlines should be phrased in a way that when read the user can determine the question that the text is meant to answer. They should describe a use-case.
- Use primitive verbs (eg: _Manage Databases_ as opposed to _Managing Databases_) or _Database Management_.

### Using Images

- The name of directories placed under `images/`, corresponds to the name of the section as displayed in the sidebar.
- Name of images, while remaining concise, should be to some level descriptive of their content (eg: `compute_path.png` and `compute_path_subgraph.png` as opposed to `compute_0.png` and `compute_1.png`).
- When an image is used across multiple pages, the **same** image file should be referenced, rather than duplicating the image.
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
  - h1 (`#`) — page title. Only one per page at the very beginning.
  - h2 (`##`)
  - h3 (`###`)
  - h4 (`####`)
- Use Title Case.
- `####` always comes after a `###` which always comes after a `##`.

**Verbs and Pronouns**

- With rare exceptions, the consistent tense used should be the present tense. (eg: _It returns_ as opposed to _It will return_).
- In most cases, the consistent pronoun is `we`. In special cases, `you` may better convey the message. Never use `I`.
- When speaking of the characteristics or capabilities of TypeDB and TypeQL or any of their components, the subject pronoun, if used, should be within the terminology, as opposed to `we`. (eg: _Graql_ has three types of statements, as opposed to _We_ have three types of statements)

**Lists (Bullet points)**
- When the list item completes the unfinished sentence before the list, end the list item with a period and start each item in lowercase.
- When the concatenation of list items construct one long sentence, end each list items with a comma with the last one ending with a period and start each item in lowercase.
- In cases other than the two described above, start the item with a capital letter and do not end the item with a full stop or a comma.
- Have an introductory sentence before the list, when possible. Always end the introductory sentence with a `:`.

**Footer Notes and Captions**
- When using a phrase, do not end the line with a period (eg: `Computation of shortest path in Workbase`).
- When using a sentence, end the line with a period. `Click on the plus icon to add a new tab.`.

**Formulations**
- Use paragraphs to provide clarity and flow.
- First sentence should describe the content of the entire paragraph at a high level.
- Avoid placing critical information in the middle or end of long paragraphs.
- Keep paragraphs short (up to 4 lines), when possible.
- Prefer short sentences to long ones. Only use complex sentence structures (multiple sentences divided by `,`, `;` or `-`), as last resort.
- Keep sentences concise. If a part of a sentence is adding no value to the point that the sentence is meant to deliver, remove it.
- Avoid the assumption that a sentence is self-explanatory. Even if explained in an earlier sentence, repeat yourself to ensure the sentence can be well-understood, without requiring reference to an earlier text.

### Cross-referencing
Most of the time, when we mention something that is explained in a previous or next page, we need to leave a reference (by turning the word or phrase into a link) to that page and sometimes to a particular heading, if need to be.

### Flow and Headings
The choice and order of headings should provide the reader with a seamless flow that offers a high-level understanding of what that page is about. By doing this, we would also make it easier for the readers to find what they are looking for, if that is why they are visiting the page.

Every heading is turned into an anchor, which in turn:
- provides visitors with a table of content, that is essentially the summary of the page.
- enables cross-referencing one or more words to a specific block of text on the same or other pages.
- allows the community to leave references to specific parts of the docs when providing answers or suggestions on different platforms.

### Keywords
All terminologies used within a page almost always need to be included as the keywords in the front matter of the markdown file.
The `keywords` attribute contains a comma-separated list of single-word keywords and/or multiple words that are expected to be searched in combination.
The `longTailKeywords` attribute contains a comma-separated list of keywords that form sensible combinations of the keyword items. They may also be any phrase that the user may search which relates to the page.

<!-- **TypeDB Terminology**

**Common Terms** -->

### Writing Markdown

**The Basics**
- Use `**` for bolding text.
- Use ` ``` ` for code blocks.
- Use `#` for headings.

**Code Blocks**

- Include the language name right after the opening ` ``` ` (eg: ` ```typeql`)
- To automatically link a code keyword to its corresponding documentation, review and maintain the [`views/autolink-keywords.js`](views/autolink-keywords.js)
- Use ` `` ` within the text, to add inline code. Language is not specified for inline code.

**Image Captions**

In the line coming immediately after the image, use the following structure for adding a caption.

```
[caption:The desired caption goes here.]
```


**Tabbed Content**
To add tabbed content, use the following structure.

```html
<div class="tabs [light|dark]">
[tab:Title 1]
...
[tab:end]

[tab:Title 2]
...
[tab:end]

[tab:Title 3]
...
[tab:end]
</div>
```
- Avoid indents inside the `div` tag, unless they appear inside a code block.
- When the tabbed content is solely a code block, use the `dark` mode (`class`).
- When the tabbed content includes text, use the `light` mode (`class`).
- In rare occasions, when the tabbed content is solely a Liquid `include` tag, add `data-no-parse` to the `div` tag.

**Slideshow**

To add slideshows, use the following structure.

```html
<div class="slideshow">

[slide:start]
[header:start]Slide 1[header:end]
[body:start]![Alt text for image 1(path/to/image-1.png)[body:end]
[footer:start]Footer note for slide 1.[footer:end]
[slide:end]

[slide:start]
[header:start]Slide 2[header:end]
[body:start]![Alt text for image 2(path/to/image-2.png)[body:end]
[footer:start]Footer note for slide 2.[footer:end]
[slide:end]

</div>
```

- `header` and `footer` are not required, but encouraged.

**Colored Panels**

To add a coloured panel, use the following structure.

```html
 <div class="note">
      [predefined-title]
      body of the note ...
 </div>
```

For the above html/markdown to be presented as a coloured panel, `predefined-title` must map to an object contained within `coloredPanels` accessible in [`views/colored-panels.js`](views/colored-panels.js).

**Colored Labels**

To add an inline coloured label, use the following structure.

```
[Label Title]
```

For the above to be presented as a coloured label, the `Label Title` must be included in the `labelsList` accessible in [`views/colored-labels.js`](views/colored-labels.js).

### Sidebar

To add sections/pages to the sidebar, modify the [`sidebar.yml`](views/sidebar.yml).

### Compatibility Tables

The documentation of each interface to TypeDB (i.e. clients, Studio, Console, etc), contains a compatibility table that needs to be updated upon every release of the interface itself, TypeDB or TypeDB Cluster. The convention in constructing these tables is as follows:

- The first column is dedicated to the versions of the interface, where each cell contains one single version number, except for the last row(s) (to avoid lengthy tables).
- Second and third columns are dedicated to TypeDB and TypeDB Cluster, respectively, where each cell may contain one or more version numbers.
  -  If there need to be 2 version numbers, they are to be separated by a `, ` (e.g. `1.5.2, 1.5.3`).
  -  If there need to be more than 2 version numbers, a range is provided (e.g. `1.5.4 to 1.5.7`).

### API References

API references are written and maintained in `.yml` files. To work, with these files, you need to have a solid understanding of YAML anchors and references.

Client API reference files are accessible via [`03-client-api/references`](03-client-api/references) and Concept API references via [`04-concept-api/references`](04-client-api/references).

### Tests

- A code block of `java` that is not preceded by any test flags, will be tested as a _Query_. Such code blocks are expected to contain an instantiation of a TypeQL query.
- A code block of `typeql` that is not preceded by any test flags, will be tested either as a _pattern_ or a _query_. It will be tested as a query if it contains any query keywords (`match`, `define`, `insert`). Otherwise, it will be tested as a pattern.
- A code block that follows the `<!-- test-example file-name.extension -->` flag, will be tested as an _example_. Such code blocks are expected to contain a self-contained piece of code with its only requirements being:
  - a running TypeDB Server
  - the schema loaded into the target database
- Code blocks that have no language name, will not be tested.
- Code blocks whose language is not `java`, `javascript` or `python` will not be tested.
- Code blocks that follow the `<!-- test-ignore -->` flag, will not be tested.
- Code blocks that follow the `<!-- test-delay -->` flag, will not be tested. The flag is expected to be removed in the next major or minor release.
