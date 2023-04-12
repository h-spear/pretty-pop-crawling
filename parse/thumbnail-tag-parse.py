from html.parser import HTMLParser
import pandas as pd

results = {"goodsno": [], "thumbnail_url": []}

THUMBNAIL_LINK_TXT = "source/thumbnail-tag.txt"


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attr = None
            url = None
            for attr, val in attrs:
                if attr == "alt":
                    goodsno = val
                elif attr == "src":
                    url = val

            if attr and url:
                results["goodsno"].append(goodsno)
                results["thumbnail_url"].append(url)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass


parser = MyHTMLParser()
f = open(THUMBNAIL_LINK_TXT, "r")

for line in f.readlines():
    parser.feed(line)

f.close()

df = pd.DataFrame(results)
df.to_excel("thumbnails" + ".xlsx")
