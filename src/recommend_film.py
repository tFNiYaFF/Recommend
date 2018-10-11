import config
import utils
import operator
from sys import argv

if __name__ == '__main__':
    user_number = 0
    try:
        user_number = int(argv[1])
    except (IndexError, TypeError):
        print("Incorrect input argument.")
        exit(1)
    grade_matrix, place_matrix, day_matrix, user_sims, u_v_days_common, u_v_places_common = [], [], [], [], [], []
    u_v_days_places_sims_mul_ratio = []
    utils.load_data(grade_matrix, config.GRADES_DATA_FILE_NAME, config.DELIMITER)
    utils.load_data(place_matrix, config.PLACES_DATA_FILE_NAME, config.DELIMITER)
    utils.load_data(day_matrix, config.DAYS_DATA_FILE_NAME, config.DELIMITER)
    utils.clean_data(grade_matrix)
    utils.clean_data(place_matrix)
    utils.clean_data(day_matrix)
    if user_number < 1 or user_number > len(grade_matrix) or user_number > len(day_matrix) or user_number > len(
            place_matrix):
        print("This user is not available")
        exit(1)
    user_number -= 1  # to simplify work with list
    utils.format_data_from_csv_to_nums(grade_matrix)
    utils.fill_sims_for_target(user_number, user_sims, grade_matrix)
    utils.common_values(user_number, u_v_days_common, day_matrix)
    utils.common_values(user_number, u_v_places_common, place_matrix)
    for i in range(0, len(u_v_places_common)):
        u_v_days_places_sims_mul_ratio.append(u_v_places_common[i] * u_v_days_common[i] * user_sims[i])
    min_grade = 3
    current_grade = min_grade
    current_movie = -1
    for i in range(0, len(u_v_days_places_sims_mul_ratio)):
        user = max(enumerate(u_v_days_places_sims_mul_ratio), key=operator.itemgetter(1))[0]
        for movie in range(0, len(day_matrix[user])):
            if (day_matrix[user][movie] == 'Sat' or day_matrix[user][movie] == 'Sun') and place_matrix[user][movie] == 'h' and grade_matrix[user][movie] >= current_grade:
                current_grade = grade_matrix[user][movie]
                current_movie = movie
        if current_movie != -1:
            break
        u_v_days_places_sims_mul_ratio[user] = 0
    if current_movie == -1:
        print("Film doesn't found")
    else:
        print("User; ", user_number + 1, ", Film: ", current_movie + 1)
else:
    print("Mode is not available")
    exit(1)
