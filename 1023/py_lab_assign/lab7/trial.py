a=10

def addnum(list): 
    list.append(1)

def add():
    global a
    a+=1
    print(a)

def re(list):
    if len(list)==3:
        return
    addnum(list)
    re(list)
    print(list)

    addnum(list)

re([0])