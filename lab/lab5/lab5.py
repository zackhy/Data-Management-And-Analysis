import matplotlib.pyplot as plt

with open ('ngrams-output.txt', 'r') as f:
    dict = {}
    for line in f:
        line = line.strip().replace('(', '').replace(')', '').replace(' ', '').split(',')
        dict[line[0]] = line[1]

    tup = sorted(dict.items(), key= lambda x:x)
    year, word_len = zip(*tup)

    plt.plot(year, word_len)
    plt.show()