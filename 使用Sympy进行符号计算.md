# Sympy
1. 下载安装Python并添加到环境变量
2. 创建一个文件夹
3. `pip install notbook`
4. `pip install sympy`
5. `jupyter notbook`
6. File->New->Notebook
7. 
a. 
```py
from sympy import *

x = Symbol('x')
y, z = symbols('y z')
```
b.

 `expr = (x**2 + 2*x + 1) / (x + 1)`

c.
- `simplify(expr)`
- `diff(expr, x) `
- `diff(expr, x, 2)` # second derivative
- `integrate(expr, x)` # indefinite integral
- `integrate(expr, (x, 0, 2))` # definite integral
- `equation = Eq(x**2 - 5*x + 6, 0)`  # define a equation
- `solutions = solve(equation, x)`