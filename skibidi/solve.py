spec = {
    "skibidi": ">",
    "rizz": "<",
    "sigma": "+",
    "gyatt": "-",
    "ohio": ".",
    "blud": ",",
    "grimaceshake": "[",
    "fanumtax": "]"
}

with open('brainrot.skibidi','r') as file:
    text = file.read().strip()
    for word in spec.keys():
        text = text.replace(word, spec[word])
    text.replace(" ","")
print(text)

# just use https://tio.run/#brainfuck after that