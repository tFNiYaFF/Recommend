import csv
import operator
import math


def load_data(matrix, name, delimiter):
    with open(name, newline='') as input_stream:
        input_data = csv.reader(input_stream, delimiter=delimiter)
        row = 0
        for row_data in input_data:
            matrix.append([])
            for column_data in row_data:
                matrix[row].append(column_data)
            row = row + 1


def clean_data(matrix):
    del (matrix[0])
    row = 0
    for row_data in matrix:
        temp_row_data = row_data[1:]
        i = 0
        for column_data in temp_row_data:
            temp_row_data[i] = column_data.replace(" ", "")
            i = i + 1
        matrix[row] = temp_row_data
        row = row + 1


def format_data_from_csv_to_nums(matrix):
    for row_data in matrix:
        i = 0
        for column_data in row_data:
            row_data[i] = int(column_data)
            i = i + 1


def sim_u_v(u, v, grades):
    if u == v:
        return 0
    films_total = len(grades[0])
    u_v_mul_sum = u_sqr_sum = v_sqr_sum = sim = 0
    for film in range(0, films_total):
        if grades[v][film] != -1 and grades[u][film] != -1:
            u_v_mul_sum += grades[v][film] * grades[u][film]
            u_sqr_sum += grades[u][film] ** 2
            v_sqr_sum += grades[v][film] ** 2
    if u_v_mul_sum != 0:
        sim = u_v_mul_sum / (math.sqrt(u_sqr_sum) * math.sqrt(v_sqr_sum))
    return sim


def r_u_i(u, i, grades, sims, knn):
    u_avg_sum = count = 0
    for grade in grades[u]:
        if grade != -1:
            u_avg_sum += grade
            count += 1
    u_avg_sum /= count
    sims_copy = []
    for s in sims:
        sims_copy.append(s)
    counter = 0
    vs = []
    while counter < knn:
        index, value = max(enumerate(sims_copy), key=operator.itemgetter(1))
        if value == 0:
            if len(vs) == 0:
                return -1  # if we cannot find any users to approximating grade
            break
        sims_copy[index] = 0
        if grades[index][i] != -1:
            vs.append(index)
            counter += 1
    sum_up = sum_down = 0
    for v in vs:
        v_avg_sum = count = 0
        for grade in grades[v]:
            if grade != -1:
                v_avg_sum += grade
                count += 1
        v_avg_sum /= count
        sum_up += sims[v] * (grades[v][i] - v_avg_sum)
        sum_down += sims[v]
    if sum_down == 0:
        return -1  # if we cannot find any users to approximating grade
    return u_avg_sum + (sum_up / abs(sum_down))


def fill_sims_for_target(target_user, sims, grades):
    users_total = len(grades)
    for v in range(0, users_total):
        sims.append(sim_u_v(target_user, v, grades))
