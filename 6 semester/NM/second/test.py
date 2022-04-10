from sympy import *
from sympy.parsing.sympy_parser import parse_expr
x = symbols('x')
y2 = symbols('y2')
z, z1 = symbols('z z1')
#
f = "y2+y1-x"
parse = parse_expr(f, local_dict={"y2": z1, "y1": z})
print(parse)
# try:
#     f = S(f)
#     print(f)
#     print(Derivative(x, x))
# except ValueError:
#     print("aza")




