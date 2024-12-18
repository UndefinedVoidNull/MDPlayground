1. 下载安装Python并添加到环境变量
2. 创建一个文件夹
3. `pip install notbook`
4. `pip install sympy`
5. `jupyter notbook`
6. File-New-Notebook
7. 
```py
import sympy as sp

x, y, z = sp.symbols('x y z')
```
8. expr
9. 
- sp.simplify
- sp.diff(expr, x) 
- sp.diff(expr, x, 2) # second derivative
- sp.integrate(expr, x) # indefinite integral
- sp.integrate(expr, (x, 0, 2)) # definite integral
- equation = sp.Eq(x**2 - 5*x + 6, 0)  # define a equation
- solutions = sp.solve(equation, x)