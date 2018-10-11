import json
import config
import utils
from sys import argv

if __name__ == '__main__':
    user_number = 0
    knn = 7
    try:
        user_number = int(argv[1])
    except (IndexError, TypeError):
        print("Incorrect input argument.")
        exit(1)
    grade_matrix, user_sims, data = [], [], {"user": user_number, "1" : {}}
    utils.load_data(grade_matrix, config.GRADES_DATA_FILE_NAME, config.DELIMITER)
    utils.clean_data(grade_matrix)
    utils.format_data_from_csv_to_nums(grade_matrix)
    if user_number < 1 or user_number > len(grade_matrix):
        print("This user is not available")
        exit(1)
    user_number -= 1  # to simplify work with list
    utils.fill_sims_for_target(user_number, user_sims, grade_matrix)
    movie = 0
    for movie_grade in grade_matrix[user_number]:
        if movie_grade == -1:
            data["1"]["movie " + str(movie + 1)] = round(utils.r_u_i(user_number, movie, grade_matrix, user_sims, knn), 3)
        movie += 1
    print(json.dumps(data, indent=4))
else:
    print("Mode is not available")
    exit(1)
