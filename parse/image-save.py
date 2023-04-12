import pandas as pd

results = {"goodsno": [], "image_url": []}

IMAGE_LINK_TXT = "source/image-url.txt"


f = open(IMAGE_LINK_TXT, "r")

for line in f.readlines():
    last = line.split("/")[-1]
    file_name_end = last.index(".")
    goodsno = last[:file_name_end]
    results["goodsno"].append(goodsno)
    results["image_url"].append(line)

f.close()

df = pd.DataFrame(results)
df.to_excel("images" + ".xlsx")
