The premise of the challenge is essentially recognizing/understanding that the popular BCrypt hashing algorithm
only makes use of the first 72 bytes. Since the hash used is a pair of the username+password, a really long username
allows for a different password to be used, with the same resulting hash.