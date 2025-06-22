import random

# 1) Set your new flag here:
flag_str = "bcactf{5011d11y_r3v3r53_3n61n33r3d_600d_j08}"
flag = flag_str.encode("utf-8")
assert len(flag) == 44, "Flag length must be 44 bytes"

# 2) Split into three groups
g1 = flag[0:16]   # bytes[0..15]
g2 = flag[16:32]  # bytes[16..31]
g3 = flag[32:44]  # bytes[32..43]

# 3) Generate random keys (16 bytes for G1, 16 bytes for G2, 12 bytes for G3)
#    (Here we fix the seed so you get the same constants every time; remove or change seed for fresh randomness.)
random.seed(0)
K1 = bytes([random.randrange(0, 256) for _ in range(len(g1))])  # 16 bytes
K2 = bytes([random.randrange(0, 256) for _ in range(len(g2))])  # 16 bytes
K3 = bytes([random.randrange(0, 256) for _ in range(len(g3))])  # 12 bytes

# 4) Compute OB1, OB2, OB3
OB1 = bytes([ ((b ^ k) + 1) & 0xFF for (b, k) in zip(g1, K1) ])  # 16 bytes
OB2 = bytes([ (b + k) & 0xFF for (b, k) in zip(g2, K2) ])         # 16 bytes
OB3 = bytes([ (b ^ k)      for (b, k) in zip(g3, K3) ])            # 12 bytes

# 5) Compute the extra sum‐check (positions 4, 10, 15 of the full 44‐byte flag)
SUM_CHECK = flag[4] + flag[10] + flag[15]

# 6) Print everything in hex for direct copy‐paste into Solidity
print("=== CONSTANTS FOR Solidity ===\n")

print("bytes16 public constant K1 = hex\"" + K1.hex() + "\";")
print("bytes16 public constant OB1 = hex\"" + OB1.hex() + "\";\n")

print("bytes16 public constant K2 = hex\"" + K2.hex() + "\";")
print("bytes16 public constant OB2 = hex\"" + OB2.hex() + "\";\n")

print("bytes12 public constant K3 = hex\"" + K3.hex() + "\";")
print("bytes12 public constant OB3 = hex\"" + OB3.hex() + "\";\n")

print("uint16 public constant SUM_CHECK = " + str(SUM_CHECK) + ";")
