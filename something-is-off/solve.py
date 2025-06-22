# in case we exit, we can resave the script with our last progress
cache = {'wosld': 'world', 'whese': 'where', 'counsless': 'countless', 'individtals': 'individuals', 'rhse': 'rise', 'famf,': 'fame,', 'omly': 'only', 'raqe': 'rare', 'ffw': 'few', 'traoscend': 'transcend', 'boundaqies': 'boundaries', 'besween': 'between', 'intelkect': 'intellect', 'aod': 'and', 'autractiveness': 'attractiveness', 'becole': 'become', 'spmething': 'something', 'mose—a': 'more—a', 'symaol,': 'symbol,', 'culturzl': 'cultural', 'pgenomenon.': 'phenomenon.', 'Tienyion': 'Tienxion', 'represdnts': 'represents', 'ooe': 'one', 'svch': 'such', 'indivhdual.': 'individual.', 'Describimg': 'Describing', 'hhm': 'him', 'meremy': 'merely', 'legdnd,': 'legend,', '"hpt"': '"hot"', 'amd': 'and', '"smbrt"': '"smart"', 'wpuld': 'would', 'conttitute': 'constitute'}


current_byte = '0'
flag = ''

try:
    with open('somethingsoff.txt','r') as file:
        text = [a for a in file.read().split() if len(a)>2]
        for word in text:
            if word in cache.keys():
                real = cache[word]
            else:
                real = input(word)

                # we can skip if the word is spelled right (short words)
                if real.strip() == '' or real.strip() == word:
                    continue
                if len(real) != len(word):
                    print(f"error: didnt handle correct spelling of {word}")
                    continue

                cache[word] = real

            for i in range(len(real)):
                if real[i] == word[i]:
                    continue
                else:
                    # little hack to handle wrapping around the alphabet
                    new_bit = int(real[i] < word[i] and real[i] != 'a')
                    print(f'\t{word}-->{new_bit}')
                    if len(current_byte) == 8:
                        print(current_byte + "..." + f'{int(current_byte, 2)}'+'...'+chr(int(current_byte, 2)))
                        flag += chr(int(current_byte, 2))
                        current_byte = ''
                    current_byte += str(new_bit)
                    break
    print(flag)
except KeyboardInterrupt:
    print(cache)
    print(flag)