def call():
    with open("a.txt"   , "r",encoding='UTF-8') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i]=lines[i].strip()
    return lines 

if __name__ == '__main__':
    a= call()
    print(a)
    