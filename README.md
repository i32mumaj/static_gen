# static_gen

A small static site generator written in Python. It takes Markdown content, drops it into an HTML template, and spits out a set of static pages ready to serve.

Built while working through the [Static Site Generator course on Boot.dev](https://www.boot.dev/courses/build-static-site-generator-python).

## How it works

Pages live as Markdown files under `content/`, mirroring the folder structure you want in the final site. Each file needs an H1 (`# Title`) at the top, which is used both as the page title and for extracting the `<title>` tag.

`template.html` is a single HTML shell with two placeholders:

- `{{ Title }}` — replaced with the page's H1
- `{{ Content }}` — replaced with the rendered HTML body

Anything in `static/` (CSS, images, etc.) gets copied over as-is.

Running the generator:

1. Wipes and recreates `public/`
2. Copies everything from `static/` into `public/`
3. Walks `content/` recursively, converts each `.md` file to HTML using `template.html`, and writes the result into the matching path under `public/`

## Markdown support

The parser handles the block and inline elements needed for a basic blog/site:

- Headings (`#` through `######`)
- Paragraphs
- Blockquotes (`>`)
- Unordered and ordered lists
- Fenced code blocks (` ``` `)
- Inline bold (`**`), italic (`_`), code (`` ` ``), links (`[text](url)`), and images (`![alt](url)`)

Everything is parsed into an intermediate node tree (`TextNode` → `HTMLNode`/`LeafNode`/`ParentNode`) before being rendered to HTML strings.

## Usage

Build the site and serve it locally:

```
./main.sh
```

This runs `src/main.py` to regenerate `public/`, then starts a local server at `http://localhost:8888`.

Run the test suite:

```
./test.sh
```

## Project layout

```
content/     Markdown source pages
static/      Static assets copied verbatim into public/
public/      Generated output (not committed)
template.html
src/
  main.py            entry point
  generate_page.py   page generation + recursive directory walk
  block.py           Markdown block parsing -> HTML nodes
  textnode.py        inline Markdown parsing (bold/italic/code/links/images)
  htmlnode.py, leafnode.py, parentnode.py   HTML node tree
  regex.py           Markdown extraction helpers
  test_*.py          unit tests
```

## Sample content

The `content/` folder includes a small demo site (a Tolkien fan page with a few blog posts) used to exercise the generator during development.
