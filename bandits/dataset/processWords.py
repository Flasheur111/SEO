count = 0
with open('words.csv', 'r') as f:
    with open('fresh_words.csv', 'w') as writer:
        for line in f:
            if len(line[:-1]) > 4:
                writer.write(line)
