def convert_float(num: float):
    num_str = str(num)

    if '.' not in num_str:
        return False

    a, b = num_str.split('.')
    a = bin(int(a))
    c = int(b)/(10 ** len(b))
    b = ''

    iter = 1
    while (True):
        if iter > (5 - (len(a) - 3)):
            print('error')
            return

        q = c * 2
        b += str(int(q))

        if int(q) == q:
            break

        c: int = int(str(q).split('.')[-1])
        c: float = c/(10 ** len(str(c)))
        iter += 1

    exp = format(len(a)-3, '03b')
    ans: str = exp + a[3:] + b
    
    if len(ans) < 8:
        ans += (8-len(ans))*'0'

    print(ans)

convert_float(1.59375)
