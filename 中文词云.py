# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:39:26 2021

@author: luke
"""

from wordcloud import WordCloud
import jieba
import numpy as np
from PIL import Image

with open(r"D:/桌面/2.txt", encoding='utf-8') as file:
    text = file.read()

    text = jieba.lcut(text)
    text = "  ".join(text)

    background = Image.open("D:/桌面/1.jpg")
    graph = np.array(background)

    stop_words = open("D:/桌面/cn_stopwords.txt", encoding="utf-8").read().split("\n")
    wordcloud = WordCloud(font_path="D:/桌面/simsun.ttf",
                          background_color="black", width=6000, stopwords=stop_words, mask=graph,
                          height=3000, max_words=500, scale=5).generate(text)

    image = wordcloud.to_image()
    image.show()
    image.save('人民币.png')
    process_word = WordCloud.process_text(wordcloud, text)
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    sort = str(sort[:50])  # # 获取 文本 词频 最高的 前50个词
f = open('词频.txt', 'w')
f.write(str(sort))
f.close()