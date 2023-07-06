def convert_float_dec(num: str) -> float:
    exp = int(num[:3], 2)
    man = num[3:]
    a = int('1' + man[:exp], 2)
    b = man[exp:]
    c = 0
    j = 1

    for i in b:
        c += int(i)/(2 ** j)
        j += 1

    return a + c


print(convert_float_dec('11111111'))
    