---
pageTitle: Example page
keywords: markdown, example
longTailKeywords: makrdown example
summary: Check all main markdown syntax.
toc: false
---

# h1 Heading
## h2 Heading
### h3 Heading
#### h4 Heading
##### h5 Heading
###### h6 Heading


## Horizontal Rules

___

---

***


## Typographic replacements

Enable typographer option to see result (doesn't work).

(c) (C) (r) (R) (tm) (TM) (p) (P) +-

test.. test... test..... test?..... test!....

!!!!!! ???? ,,  -- ---

"Smartypants, double quotes" and 'single quotes'


## Emphasis

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~


## Blockquotes


> Blockquotes can also be nested...
>> ...by using additional greater-than signs right next to each other...
> > > ...or with spaces between arrows.


## Lists

Unordered

* Create a list by starting a line with `+`, `-`, or `*`
* Sub-lists are made by indenting 2 spaces (doesn't work):
  - Marker character change forces new list start:
      * Ac tristique libero volutpat at
      + Facilisis in pretium nisl aliquet
      - Nulla volutpat aliquam velit
+ Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`

Start numbering with offset (doesn't work):

57. foo
1. bar


## Code

Inline `code`

Indented code

    // Some comments
    line 1 of code
    line 2 of code
    line 3 of code


Block code "fences"

```
Sample text here...
```

Syntax highlighting

``` js
var foo = function (bar) {
  return bar++;
};

console.log(foo(5));
```

## Tables

| Option | Description |
| ------ | ----------- |
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |

Right aligned columns

| Option | Description |
| ------:| -----------:|
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |


## Links

[link text](http://dev.nodeca.com)

[link with title](http://nodeca.github.io/pica/demo/ "title text!")

Autoconverted link https://github.com/nodeca/pica (enable linkify to see) (doesn't work) 


## Images

![Minion](https://octodex.github.com/images/minion.png)
```
[caption:Minion.] (doesn't work)
```

![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")
```
[caption:Stormtroopocat.] (doesn't work)
```

With a reference later in the document defining the URL location:

![Alt text][id]

[id]: https://octodex.github.com/images/dojocat.jpg  "The Dojocat"


## Note blocks

<div class="note">
[Note]
This is a note.Feel free to study the content of `social-network-schema.tql`. The definitions have been divided into multiple sections for better understandability, with each section containing the (commented-out) query for visualisation of the corresponding section in [TypeDB Studio](../07-studio/00-overview.md).
</div>

<div class="note">
[important]
This is an important note. Feel free to study the content of `social-network-schema.tql`. The definitions have been divided into multiple sections for better understandability, with each section containing the (commented-out) query for visualisation of the corresponding section in [TypeDB Studio](../07-studio/00-overview.md).
</div>

<div class="note">
[advanced]
This is an advanced note. Feel free to study the content of `social-network-schema.tql`. The definitions have been divided into multiple sections for better understandability, with each section containing the (commented-out) query for visualisation of the corresponding section in [TypeDB Studio](../07-studio/00-overview.md).
</div>

<div class="note">
[warning]
This is a warning note. Feel free to study the content of `social-network-schema.tql`. The definitions have been divided into multiple sections for better understandability, with each section containing the (commented-out) query for visualisation of the corresponding section in [TypeDB Studio](../07-studio/00-overview.md).
</div>

## Tabs

<div class="tabs light">

[tab:Docker]

Use `docker run` to download an image `vaticle/typedb` and run a container with it. To ensure that data is preserved
even when the instance is killed or restarted, mount an external volume to your Docker container:

```
docker run --name typedb -d -v ~/typedb:/opt/typedb-all-linux/server/data/ -p 1729:1729 vaticle/typedb:latest
```

[tab:end]

[tab:Linux]

#### Using package manager, like APT

As a superuser, add the repo:
```
sudo apt install software-properties-common apt-transport-https gpg
gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 8F3DA4B5E9AEF44C 
gpg --export 8F3DA4B5E9AEF44C | sudo tee /etc/apt/trusted.gpg.d/vaticle.gpg > /dev/null
echo "deb [ arch=all ] https://repo.vaticle.com/repository/apt/ trusty main" | sudo tee /etc/apt/sources.list.d/vaticle.list > /dev/null
```

[tab:end]

[tab:MacOS]

#### Using Homebrew
```sh
brew install typedb
```

[tab:end]

[tab:Windows]

#### Manual Download
Download the [latest release](https://github.com/vaticle/typedb/releases), unzip it in a location on your machine that is easily accessible via command prompt.


[tab:end]

</div>

<div class="tabs dark">

[tab:Docker]

```
docker run --name typedb -d -v ~/typedb:/opt/typedb-all-linux/server/data/ -p 1729:1729 vaticle/typedb:latest
```

[tab:end]

[tab:Linux]

```
sudo apt install software-properties-common apt-transport-https gpg
gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 8F3DA4B5E9AEF44C 
gpg --export 8F3DA4B5E9AEF44C | sudo tee /etc/apt/trusted.gpg.d/vaticle.gpg > /dev/null
echo "deb [ arch=all ] https://repo.vaticle.com/repository/apt/ trusty main" | sudo tee /etc/apt/sources.list.d/vaticle.list > /dev/null
```

[tab:end]

[tab:MacOS]

```sh
brew install typedb
```

[tab:end]

[tab:Windows]

#### Manual Download
Download the [latest release](https://github.com/vaticle/typedb/releases), unzip it in a location on your machine that is easily accessible via command prompt.

[tab:end]

</div>

## Slideshow

(doesn't work)

<div class="slideshow">

[slide:start]
[header:start]Slide 1[header:end]
[body:start]![Alt text for image 1(../images/schema/unstructured-problems.png)[body:end]
[footer:start]Footer note for slide 1.[footer:end]
[slide:end]

[slide:start]
[header:start]Slide 2[header:end]
[body:start]![Alt text for image 2(https://octodex.github.com/images/stormtroopocat.jpg)[body:end]
[footer:start]Footer note for slide 2.[footer:end]
[slide:end]

</div>


