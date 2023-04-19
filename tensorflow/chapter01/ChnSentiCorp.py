# 1、定义3个容器，对切分的字符进行存储。
labels = []  # 用户存储情感分类,形如 [1,1,1,0,0,0,0]
vocab = set()  # set类型，用以存放不重复的字符
context = []  # 存放文本列表

# 2、读取字符或者文本
with open("./ChnSentiCorp.txt", mode="r", encoding="UTF-8") as emotion_file:
    for line in emotion_file.readlines():
        line = line.strip().strip(",")
        labels.append(int(line[0]))

        text = line[1]
        context.append(text)
        for char in text: vocab.add(char)

# 3、读取字符串 并获取字符串长度
vocab_list = list(sorted(vocab))
print(len(vocab_list))
