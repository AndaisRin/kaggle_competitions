'''
B. Локализация котов
Разработчица стремится автоматизировать подкармливание кошек, используя алгоритмы компьютерного зрения для локализации
и подсчета кошек на фотографиях. Она хочет определить количество кошек, посещающих миску, и обеспечить правильное насыпание
порций корма. Кроме того, она планирует создать аккаунт с фотографиями кошек для поиска их хозяев.
Задача включает в себя не только подсчет кошек, но и их разделение на фотографиях с учетом соблюдения социальной кошачьей дистанции.
Формат ввода
На вход подается результат первичной сегментации:
M строк, в каждой из них N целых чисел (0 обозначает фон, 1 - области, где Катин алгоритм нашел кошку). 1 <= N, M <=500
Формат вывода
В первой строке выведите число уникальных найденных на сегментации объектов.
Далее выведите матрицу размера NxM (как и входная матрица) с разметкой общих сегментированных областей на отдельные объекты
(у каждого объекта должен быть свой уникальный номер).
Пример 1
Ввод:
1 0 1
0 0 0
0 1 0
Вывод:
3
1 0 2
0 0 0
0 3 0
'''


import sys
sys.setrecursionlimit(10**6)

def dfs(matrix, row, col, mark):
    if row < 0 or col < 0 or row >= len(matrix) or col >= len(matrix[0]) or matrix[row][col] != 1:
        return
    matrix[row][col] = mark
    dfs(matrix, row+1, col, mark)
    dfs(matrix, row-1, col, mark)
    dfs(matrix, row, col+1, mark)
    dfs(matrix, row, col-1, mark)

def count_objects(matrix):
    mark = 2
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                dfs(matrix, i, j, mark)
                mark += 1
    return mark - 2, matrix

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

def main():
    matrix = []
    for line in sys.stdin:
        row = list(map(int, line.split()))
        matrix.append(row)

    unique_objects, labeled_matrix = count_objects(matrix)
    print(unique_objects)
    print_matrix(labeled_matrix)

if __name__ == "__main__":
    main()