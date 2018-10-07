import config
import utils

USER_NUMBER = 0
KNN = 7

grade_matrix, place_matrix, day_matrix, user_sims = [], [], [], []
utils.load_data(grade_matrix, config.GRADES_DATA_FILE_NAME, config.DELIMITER)
utils.load_data(place_matrix, config.PLACES_DATA_FILE_NAME, config.DELIMITER)
utils.load_data(day_matrix, config.DAYS_DATA_FILE_NAME, config.DELIMITER)
utils.clean_data(grade_matrix)
utils.clean_data(place_matrix)
utils.clean_data(day_matrix)
utils.format_data_from_csv_to_nums(grade_matrix)
utils.fill_sims_for_target(USER_NUMBER, user_sims, grade_matrix) # похожие вкусы