print("Enter a emoji in each line and finally press Ctrl+d for get its unicode :)")
print("Blank enter for end :)")

emojies = []
while True:
    i = input()
    if not i or i == "":
        break
    emojies.append(i)
print("Unicodes in respectively")
for e in emojies:
    print(f'U+{ord(e):X}')
