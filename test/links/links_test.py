import unittest
import glob
import re
import pprint
pp = pprint.PrettyPrinter(indent=4)


class LinksTest(unittest.TestCase):

    def test_links(self):
        pattern_to_find_links = '(\[[^\]]*?\]\(\.\.\/)((\d+-[^\/\)]*(\/|))+)\)'
        pattern_to_find_anchors = '#+\s(.*)'

        pages = {}

        for markdown_path in glob.iglob('./**/*.md'):
            title = markdown_path.replace("./", "")

            pages[title] = {"links": [], "anchors": []}

            with open(markdown_path) as markdown_file:
                content = markdown_file.read()
                link_matches = re.findall(pattern_to_find_links, content)
                for match in link_matches:
                    link = match[1]
                    pages[title]["links"].append(link)

                anchor_matches = re.findall(pattern_to_find_anchors, content)
                for match in anchor_matches:
                    anchor = match.replace(r"^[^a-zA-Z]+", "").replace(r" ", "-").lower()
                    anchor = re.sub("[^a-zA-Z0-9 -]+", "", anchor)

                    pages[title]["anchors"].append(anchor)

        errors = []

        for title, links_and_anchors in pages.items():
            for link in links_and_anchors["links"]:
                link_page = link.split("#")[0]
                link_page = link_page.split("?")[0]  # remove params

                if link_page not in pages:
                    errors.append("The link [" + link_page + "] found in [" + title + "] is broken.")

                link_has_anchor = len(link.split("#")) > 1
                if link_has_anchor:
                    link_anchor = link.split("#")[1]
                    if link_page in pages and link_anchor not in pages[link_page]["anchors"]:
                        errors.append("The anchor [" + link_anchor + "] of the link [" + link_page + "] found in [" + title + "] is broken.")
        pp.pprint(errors)
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
