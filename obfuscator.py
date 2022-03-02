with open('names.txt') as f:
    lines = f.readlines()

items = []
for i in lines:
    a = i.split()
    n = ""
    for j in a[:-1]:
        v = '*'*len(j)
        n += v + " "
    n += '*'*(len(a[-1])-3)
    n += a[-1][-3:]
    n += '\n'
    items.append(n)

with open('obfuscated.txt', 'w') as f:
    f.writelines(items)
