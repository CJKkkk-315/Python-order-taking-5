import requests
import json
from bilibili_api import video, sync, Credential
import csv

res = []

credential = Credential(sessdata="c4d85b58%2C1725189373%2C4968d%2A32CjAwg3RYSBlAsdV9pi2knUyDpLM3d48JtfrjUe9rbhPp43bovlWPsKyhf5-ns6puCE0SVkZybDU1Ym5Id3pBWHRFUHdnc2pPT3B0dHc4dUJMWklQR2YyZWl6WGtFX0o5RUpnaDNiSmc0YkJBemluc3dEdHRmZUJCdTVMcnJtX05oaHhLaThnYU1nIIEC", bili_jct="448dcc3d4976743cadb686be576b6d6b", buvid3="67A33030-120E-0B12-196D-396AC4B2E6FF10757infoc", dedeuserid="250171188")
iid = 0
v = video.Video(bvid='BV1Bz421R7E9', credential=credential)
dms = sync(v.get_danmakus())
for dm in dms:
    res.append([iid, dm.text])
    print(dm.text)

