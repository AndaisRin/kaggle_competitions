'''
C. Эволюция полиномов
Ваша задача помочь Васе найти наименьший вещественный корень уравнения det(B+Az+Iz^2)=0,
где матрицы A и B - вещественные симметричные матрицы. Гарантируется, что такой корень существует.

Формат ввода
Первая строка содержит число n 1≤n≤100 - размер матриц A и B. В следующих n строчках содержится n чисел - элементов матрицы A.
В следующих n строчках содержится n чисел - элементов матрицы B.

Формат вывода
Выведите одно число - ответ на задачу с точностью четыре знака после запятой. Округление выполняется по стандартным правилам.
Рекомендуем использовать np.round(data, 4) или аналоги.

Пример
Ввод
3
1 0 0
0 1 0
0 0 1
-1 0 0
0 -1 0
0 0 -1
Вывод
-1.618
'''


import numpy as np

def f(z, A, B):
    n = A.shape[0]
    return np.linalg.det(B + np.dot(A, z) + np.eye(n) * z**2)

def find_root(f, x0, A, B, maxiter):
    def newton_method(f, x0, A, B, maxiter):
        tol = 1e-8
        for i in range(maxiter):
            fval = f(x0, A, B)
            fder = (f(x0 + tol, A, B) - f(x0, A, B)) / tol
            newton_step = fval / fder
            if abs(newton_step) < tol:
                return x0 - newton_step
            x0 = x0 - newton_step
        return x0
    root = newton_method(f, x0, A, B, maxiter)
    return round(root, 4)

def read_input():
    n = int(input())
    A = np.array([list(map(float, input().split())) for _ in range(n)])
    B = np.array([list(map(float, input().split())) for _ in range(n)])
    return A, B

if __name__ == "__main__":
    A, B = read_input()
    root = find_root(f, -1, A, B, 80)
    print(root)