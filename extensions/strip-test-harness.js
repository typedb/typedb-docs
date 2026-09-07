'use strict'

// Keep MARKERS synced with test/code/parser/parser.py and typedb-docs-web hidden-code.js.
const MARKERS = {
  typeql: {
    testStart: /^\s*#!test(?:\[.*?\])?\s*$/,
    hiddenStart: /^\s*#{{/,
    hiddenEnd: /^\s*#}}/,
    segmentSep: /^\s*#!---\s*$/,
  },
  python: {
    testStart: /^\s*#!test(?:\[.*?\])?\s*$/,
    hiddenStart: /^\s*#{{/,
    hiddenEnd: /^\s*#}}/,
    segmentSep: /^\s*#!---\s*$/,
  },
  console: {
    testStart: /^\s*#!test(?:\[.*?\])?\s*$/,
    hiddenStart: /^\s*#{{/,
    hiddenEnd: /^\s*#}}/,
    segmentSep: /^\s*#!---\s*$/,
  },
  rust: {
    testStart: /^\s*\/\/!test(?:\[.*?\])?\s*$/,
    hiddenStart: /^\s*\/\/{{/,
    hiddenEnd: /^\s*\/\/}}/,
    segmentSep: /^\s*\/\/---\s*$/,
  },
}

const HARNESS_PROBE = /#!test|#{{|\/\/!test|\/\/{{/

function resolveMarkers (language, lines) {
  if (language && MARKERS[language]) return MARKERS[language]
  const joined = lines.join('\n')
  if (/\/\/!test|\/\/{{/.test(joined)) return MARKERS.rust
  if (/#!test|#{{/.test(joined)) return MARKERS.typeql
  return null
}

function stripHarnessLines (lines, markers) {
  const visible = []
  let inHidden = false

  for (const line of lines) {
    if (markers.testStart.test(line)) continue
    if (markers.hiddenStart.test(line)) {
      inHidden = true
      continue
    }
    if (inHidden) {
      if (markers.hiddenEnd.test(line)) inHidden = false
      continue
    }
    if (markers.segmentSep.test(line)) continue
    visible.push(line)
  }

  while (visible.length && visible[0].trim() === '') visible.shift()
  while (visible.length && visible[visible.length - 1].trim() === '') visible.pop()

  return visible
}

function removeBlock (block) {
  const parent = block.getParent()
  if (!parent) return
  const blocks = parent.getBlocks()
  const idx = blocks.indexOf(block)
  if (idx >= 0) blocks.splice(idx, 1)
}

module.exports = function registerStripTestHarness () {
  this.treeProcessor(function () {
    this.process(function (doc) {
      doc.findBy({ context: 'listing' }).forEach((block) => {
        const lines = block.getLines ? block.getLines() : block.lines
        if (!lines || !lines.length) return
        if (!HARNESS_PROBE.test(lines.join('\n'))) return

        const language = block.getAttribute('language') || block.getAttribute('style')
        const markers = resolveMarkers(language, lines)
        if (!markers) return

        const stripped = stripHarnessLines(lines, markers)
        if (!stripped.length) {
          removeBlock(block)
          return
        }
        block.lines = stripped
      })
    })
  })
}

module.exports.stripHarnessLines = stripHarnessLines
module.exports.MARKERS = MARKERS
