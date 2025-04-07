def f_string(s):
    s = f"{s:,.3f}"
    s = s.replace(',', ' ')
    s = f"{s:*^30}"
    return s

print(f_string(3.14159265))
