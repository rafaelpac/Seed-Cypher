import hashlib, binascii, sys

goal = "a"
while goal not in "dDeE" or len(goal) != 1:
    print()
    goal = input("Do you want to ENCRYPT (E) or DECRYPT (D) a seed phrase? (Q) to QUIT. ")
    if goal in "qQ":
        sys.exit()
    if goal in "dD":
        operator = -1
        verb = "decrypted"
    if goal in "eE":
        operator = 1
        verb = "encrypted"

while True:
    try:
        size = int(input("\nHow many words does the seed have? "))
        break
    except ValueError:
        print("Oops! That was no valid number. Try again.")

original_seed = [""] * size
original_seed_numbered = [0] * size
new_seed = [""] * size
new_seed_numbered = [0] * size

for i in range(size):
    numeral = "th"
    if i == 0 or (i%10 == 0 and i > 19):
        numeral = "st"
    if i == 1 or (i%10 == 1 and i > 19):
        numeral = "nd"
    if i == 2 or (i%10 == 2 and i > 19):
        numeral = "rd"
    while original_seed_numbered[i] == 0:
        print()
        original_seed[i] = input(str(i+1) + numeral + " word of the seed: ")
        f = open("english.txt", "r")
        line = 1
        for x in f:
            if x == original_seed[i] + "\n":
                original_seed_numbered[i] = line
            line += 1
        if original_seed_numbered[i] == 0:
            print("                      This word is not part of the BIP-39 english words list.")
            print("                      Please enter it again.")
        f.close()
print()

password = input("\nEnter a password: ")
hashed_seed = hashlib.sha512(binascii.a2b_qp(password)).hexdigest()
print("Password SHA-512 hash: " + hashed_seed)
print()
      
for i in range(size):
    result = original_seed_numbered[i] + operator*int(hashed_seed[i*3:i*3+3],16)
    new_seed_numbered[i] = result
    while result > 2048:
        new_seed_numbered[i] = result - 2048
        result -= 2048
    while result < 1:
        new_seed_numbered[i] = result + 2048
        result += 2048
    
    f = open("english.txt", "r")
    line = 1
    for x in f:
        if line == new_seed_numbered[i]:
            new_seed[i] = x[:-1]
        line += 1
    f.close()

print("The seed")
print("---> ", end ="")
print(original_seed)
print("was " + verb + " with password \'" + password + "\' into")
print("---> ", end ="")
print(new_seed)
