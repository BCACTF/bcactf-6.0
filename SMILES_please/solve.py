from hashlib import sha256
hashed_SMILES = open("compound.txt").readline().split()[-1]
with open("example.smi") as f:
    for line in f:
        SMILES = line.strip()
        if (sha256(SMILES.encode()).hexdigest() == hashed_SMILES):
            print(SMILES)

        