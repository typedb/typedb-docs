import unittest
import glob
import re
import pprint
pp = pprint.PrettyPrinter(indent=4)


class LinksTest(unittest.TestCase):

    def test_links(self):
        pattern_to_find_links = '(\[[^\]]*?\]\(\.\.\/)((\d+-[^\/\)]*(\/|))+)\)'
        pattern_to_find_anchors = '#+\s(.*)'

        links_and_anchors = {}

        for markdown_file in glob.iglob('./**/*.md'):
            markdown_file = markdown_file.replace("./", "")

            links_and_anchors[markdown_file] = {"links": [], "anchors": []}

            with open(markdown_file) as file:
                content = file.read()
                link_matches = re.findall(pattern_to_find_links, content)
                for match in link_matches:
                    links_and_anchors[markdown_file]["links"].append(match[1])

                anchor_matches = re.findall(pattern_to_find_anchors, content)
                for match in anchor_matches:
                    anchor = match.replace(r"^[^a-zA-Z]+", "").replace(r" ", "-").lower()
                    anchor = re.sub("[^a-zA-Z0-9 -]+", "", anchor)

                    links_and_anchors[markdown_file]["anchors"].append(anchor)

        errors = []

        for page_title, page_details in links_and_anchors.items():
            for link in page_details["links"]:
                page_url = link.split("#")[0]

                if page_url not in links_and_anchors:
                    errors.append("The link [" + page_url + "] found in [" + page_title + "] is broken.")

                if len(link.split("#")) > 1:
                    page_anchor = link.split("#")[1]
                    if page_url in links_and_anchors and page_anchor not in links_and_anchors[page_url]["anchors"]:
                        errors.append("The anchor [" + page_anchor + "] of the link [" + page_url + "] found in [" + page_title + "] is broken.")
        pp.pprint(errors)
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
