import numpy as np


def input_data():
    print(" Введите количество переменных в целевой функции: ")
    num_variables = int(input())

    print(" Введите количество ограничений\n При этом ограничения типа xi≥0 не учитывайте.: ")
    num_constraints = int(input())

    print("Введите коэффициенты целевой функции (через пробелы): ")
    objective_function = list(map(float, input().split()))

    constraint_matrix = []
    b_values = []
    for i in range(num_constraints):
        print(" Введите коэффициенты ограниченя ", i + 1,
              " и их значение необходимо с последующим значением (через пробелы)\n Вводить в формате x1+x2≤const: ")
        constraint = list(map(float, input().split()))
        constraint_matrix.append(constraint[:-1])
        b_values.append(constraint[-1])

    return num_variables, num_constraints, objective_function, constraint_matrix, b_values


def initialize_tableau(num_variables, num_constraints, objective_function, constraint_matrix, b_values):
    tableau = np.zeros((num_constraints + 1, num_variables + num_constraints + 1))

    for i in range(num_variables):
        tableau[-1, i] = -objective_function[i]

    for i in range(num_constraints):
        for j in range(num_variables):
            tableau[i, j] = constraint_matrix[i][j]

        tableau[i, num_variables + i] = 1
        tableau[i, -1] = b_values[i]

    return tableau


def simplex(tableau):
    while np.min(tableau[-1, :-1]) < 0:
        pivot_col_idx = np.argmin(tableau[-1, :-1])
        positive_ratios = [tableau[i][-1] / tableau[i][pivot_col_idx] if tableau[i][pivot_col_idx] > 0 else np.inf for i
                           in range(tableau.shape[0] - 1)]
        pivot_row_idx = np.argmin(positive_ratios)

        print("Индекс сводного столбца: ", pivot_col_idx)
        print("Индекс сводной строки: ", pivot_row_idx)

        pivot_value = tableau[pivot_row_idx, pivot_col_idx]
        tableau[pivot_row_idx, :] /= pivot_value

        for i in range(tableau.shape[0]):
            if i != pivot_row_idx:
                tableau[i] -= tableau[pivot_row_idx] * tableau[i, pivot_col_idx]

        print("Промежуточные таблицы:")
        print(tableau)

    return tableau


def main():
    num_variables, num_constraints, objective_function, constraint_matrix, b_values = input_data()
    tableau = initialize_tableau(num_variables, num_constraints, objective_function, constraint_matrix, b_values)
    print("Исходная таблица:")
    print(tableau)
    final_tableau = simplex(tableau)
    print("Финальная таблица:")
    print(final_tableau)
    optimal_value = final_tableau[-1, -1]
    print("Оптимальное значение максимизации функции: ", optimal_value)


if __name__ == "__main__":
    main()