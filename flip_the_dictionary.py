from collections import defaultdict

def invert(dct):
    res_dct = defaultdict(set)
    for key, value in dct.items():
        res_dct[value].add(key)
    res_dct = {
        key : sorted(value)
        for key , value in sorted(res_dct.items())
    }
    return res_dct

dict = {'a':42 , 'b':42, 'c':24}
print(invert(dict))