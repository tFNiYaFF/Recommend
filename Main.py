import csv
import math
import operator
import json

USER_NUMBER = 0  # real number minus one
KNN = 7


def load_data(matrix):
    with open('data.csv', newline='') as input_stream:
        input_data = csv.reader(input_stream, delimiter=',')
        row = 0
        for row_data in input_data:
            matrix.append([])
            for column_data in row_data:
                matrix[row].append(column_data)
            row = row + 1


def format_data(matrix):
    row = 0
    for row_data in matrix:
        temp_row_data = row_data[1:]
        i = 0
        for column_data in temp_row_data:
            temp_row_data[i] = int(column_data.replace(" ", ""))
            i = i + 1
        matrix[row] = temp_row_data
        row = row + 1


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


def r_u_i(u, i, grades, sims):
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
    while counter < KNN:
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


grade_matrix, user_sims = [], []
user_v = movie = 0
load_data(grade_matrix)
grade_matrix = grade_matrix[1:]
format_data(grade_matrix)
for user in grade_matrix:
    user_sims.append(sim_u_v(USER_NUMBER, user_v, grade_matrix))
    user_v += 1

data = {"user": USER_NUMBER}
json_counter = 0
counter_state = 1
for movie_grade in grade_matrix[USER_NUMBER]:
    if movie_grade == -1:
        if counter_state == 1:
            counter_state = 0
            json_counter += 1
            data[str(json_counter)] = {}
        data[str(json_counter)]["movie " + str(movie)] = round(r_u_i(USER_NUMBER, movie, grade_matrix, user_sims), 3)
    else:
        counter_state = 1
    movie += 1
print(json.dumps(data, indent=4))
