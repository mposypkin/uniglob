from lipexpr import *

e1 = const(1)
e2 = const(2)
e3 = ident([0, 1])
e4 = e3 + (e1 + e2)
print(e4)
print("Hello test")