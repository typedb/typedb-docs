# GRAKN.AI Documentation

This repository contains all content that powers the Grakn Documentation Portal, accessible at [dev.grakn.ai](http://dev.grakn.ai).


## Contribute
- Fork this repository
- Read the [Contribution Guidelines]() carefully
- Make the desired changes.
- Issue pull request(s) and select the `base` branch in accordance with the Branch Classifications.

## Branch Classifications
The classification of the branches and the purpose of each is as follows:

### Master
The master branch contains the content for the live documentation for the current release.
PRs that have the `master` branch as their _base_, contain one or more of the following changes:
- fixing a linguistic mistake,
- reflecting a change in the terminology,
- rephrasing textual content,
- adding complementary content to an existing feature,
- updating images,
- and other changes of the same nature

Given a PR made on `master` that can and should be reflected in the next release as well, a second identical (or slightly different) PR needs to be made on one of the `development` branches.

### Development
The development branch contains the content of the documentation for the next immediate release.
PRs that have the `development` branch as their _base_, contain changes that are either:
- previously made on `master` and should also be reflected for the next release, or
- meant to introduce a new future/change that will only be available as a part of the next release

**Grakn Core** and clients **Java**, **Node.js** and **Python** are all separate repositories that have their independent release cycles. To ensure that the development state of the documentation remains in sync with the latest changes made in each of these repositories, `docs` has a different `development` branch for each of them. Therefore, when submitting a PR to update the development state of docs, the correct corresponding `development` branch needs to be selected as `base`. The file changes expected to be seen in a development PR are as follows:
- `development-java`: `03-client-api/references/*.md`, `03-client-api/01-java.md` and changes made in `java` code blocks
- `development-nodejs`: `03-client-api/references/*.md`, `03-client-api/01-nodejs.md` and changes made in `nodejs` code blocks
- `development-python`: `03-client-api/references/*.md`, `03-client-api/01-python.md` and changes made in `python` code blocks
- `development-grakn`: any other files and changes made in `graql` code blocks

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
- Keep file and directory names compact: in most cases, one or two words that best describe the contained content. Never use more than three words.
- Choosing the same name for different files located in different directories is acceptable. (eg: `files/social-network/schema.gql` and `files/phone-calls/schema.gql`).
- For naming images, refer to the [Images Guidelines](#images).


**Headlines**

- Headlines should be phrased in a way that when read the user can determine the question that the text is meant to answer. They should describe a use-case.
- Use primitive verbs (eg: _Manage Keyspaces_ as opposed to _Managing Keyspaces_).

### Using Images

- The name of directories placed under `images/`, corresponds to the name of the section as displayed in the sidebar.
- Name of images, while remaining concise, should be to some level descriptive of their content (eg: `compute_path.png` and `compute_path_subgraph.png` as opposed to `compute_0.png` and `compute_1.png`).
- When an image is used across multiple pages, the **same** image file should be referenced, rather than duplicating the image.
- Screenshots of Workbase should be:
  - named after the UI/UX components of the software itself. (eg: `graql-editor_clear-query.png`).
  - taken at the screen resolution of 1280 x 720.
  - image size of 1147 x 671.
  - consistent in their paddings (position of Workbase's layout within the screenshot).

### Writing Style

**Spelling**

Use American.git st

**Headings**
- There are only two levels of headings used across all markdown files:
  - h2 (`##`)
  - h3 (`###`)
- Use Title Case.
- `###` always comes after a `##`.

**Verbs and Pronouns**

- With rare exceptions, the consistent tense used should be the present tense. (ex: _It returns_ as opposed to _It will return_).
- In most cases, the consistent pronoun is `we`. In individual cases, `you` may better convey the message. Never use `I`.

**Lists (Bullet points)**
- When the list item completes the unfinished sentence before the list, end the list item with a period.
- When the concatenation of list items construct one long sentence, end each list items with a comma with the last one ending with a period.
- Have an introductory sentence prior to the list, when possible.

**Footer Notes and Captions**
- When using a phrase, do not end the line with a period (eg: `Computation of shortest path in Workbase`).
- When using a sentence, end the line with a period. `Click on the plus icon to add a new tab.`.

**Formulations**
- Use paragraphs to provide clarity and flow.
- Fist sentence should describe the content of the entire paragraph at a high level.
- Avoid placing critical information in the middle or end of long paragraphs.
- Keep paragraphs short (up to 4 lines), when possible.
- Prefer short sentences to long ones. Only use complex sentence structures (multiple sentences divided by `,`, `;` or `-`), as last resort.
- Keep sentences concise. If a part of a sentence is adding no value to the point that the sentence is meant to deliver, remove it.
- Avoid the assumption that a sentence is self-explanatory. Even if explained in an earlier sentence, repeat yourself to ensure the sentence can be well-understood, without requiring reference to an earlier text.

<!-- **Grakn Terminology**

**Common Terms** -->

### Writing Markdown

**The Basics**
- Use `**` for bolding text.
- Use ` ``` ` for code blocks.
- Use `#` for headings.

**Code Blocks**

- Include the language name right after the opening ` ``` ` (eg: ` ```graql `)
- To automatically link a code keyword to its corresponding documentation, review and maintain the [`views/autolink-keywords.js`](views/autolink-keywords.js)
- Use ` `` ` within the text, to add inline code. Language is not specified for inline code.

**Tabbed Content**
To add tabbed content, use the following structure.

```html
<div class="tabs light">
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
- Avoid indents inside the `div` tag.
- When the tabbed content is solely a code block, use the `dark` mode (`class`).
- When the tabbed content includes text, use the `light` mode (`class`).
- In rare occasions, when the tabbed content is solely a Liquid `include` tag, add `data-no-parse` to the `div`.

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

- `header` and `footer` is not required, but encouraged.

**Colored Panels**

To add a coloured panel, use the following structure.

```html
 <div class="note">
      [predefined-title]
      body of the note ...
 </div>
```

In order for the above html/markdown to be presented as a coloured panel, `predefined-title` must map to an object contained within `coloredPanels` accessible in [`views/colored-panels.js`](views/colored-panels.js).

**Colored Labels**

To add an inline coloured label, use the following structure.

```
[Label Title]
```

In order for the above to be presented as a coloured label, the `Label Title` must be included in the `labelsList` accessible in [`views/colored-labels.js`](views/colored-labels.js).

### API References

API references are written and maintained in `.yml` files. In order to work, with these files, you need to have a solid understanding of yaml anchors and references.

Client API reference files are accessible via [`03-client-api/references`](03-client-api/references) and Concept API references via [`04-concept-api/references`](04-client-api/references).

### Tests

- Code blocks that have no language name, will not be tested.
- Code blocks whose language is not `java`, `javascript` or `python` will not be tested.
- Code blocks that follow the `<!-- test-ignore --> flag, will not be tested.
- Code blocks that follow the `<!-- test-delay --> flag, with the flag expected to be removed in the next major or minor release.
- Code blocks of `java`, `javascript` or `python` that are not preceded by any test flags, will be tested as snippets. Learn more about [Snippet Tests](test/snippet/README.md).
- Code blocks that follow the `<!-- test-standalone file-name.extension --> flag, will be tested as standalones. Learn more about [Standalone Tests](test/standalone/README.md).