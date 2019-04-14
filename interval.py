import math

def cos(x):
    y = [math.cos(x[0]), math.cos(x[1])]
    pi2 = 2 * math.pi
    if math.ceil(x[0]/pi2) <= math.floor(x[1]/pi2):
        b = 1
    else:
        b = max(y)

    if math.ceil((x[0] - math.pi)/pi2) <= math.floor((x[1] - math.pi)/pi2):
        a = -1
    else:
        a = min(y)
    return [a,b]

if (__name__ == '__main__'):
    print(cos([0, math.pi / 2]))
    print(cos([- math.pi / 2, math.pi / 2]))
    print(cos([- 3 * math.pi / 2, - math.pi / 2]))