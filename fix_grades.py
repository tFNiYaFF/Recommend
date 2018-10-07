import json
import utils

USER_NUMBER = 0  # real number minus one
KNN = 7
GRADES_DATA_FILE_NAME = "data.csv"
DELIMITER = ","

grade_matrix, user_sims, data = [], [], {"user": USER_NUMBER}
utils.load_data(grade_matrix, GRADES_DATA_FILE_NAME, DELIMITER)
utils.format_data_from_csv_to_nums(grade_matrix)
utils.fill_sims_for_target(USER_NUMBER, user_sims, grade_matrix)
json_counter = movie = 0
counter_state = 1
for movie_grade in grade_matrix[USER_NUMBER]:
    if movie_grade == -1:
        if counter_state == 1:
            counter_state = 0
            json_counter += 1
            data[str(json_counter)] = {}
        data[str(json_counter)]["movie " + str(movie)] = round(utils.r_u_i(USER_NUMBER, movie, grade_matrix, user_sims, KNN), 3)
    else:
        counter_state = 1
    movie += 1
print(json.dumps(data, indent=4))
