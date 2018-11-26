import sparql_works
import recommend_film
import utils
import config
from sys import argv

user_number = 0
try:
    user_number = int(argv[1])
except (IndexError, TypeError):
    print("Incorrect input argument.")
    exit(1)
film_id = recommend_film.get_film(user_number)
if film_id == -1:
    print("Film did not found for recomendation.")
    exit(1)
data = []
utils.load_data(data, config.MOVIE_NAMES, config.DELIMITER)
result = sparql_works.get_sparql_result_by_film_name(data[film_id-1][1])
if result == -1:
    print("Film did not found on wikidata.")
    exit(1)
print(result)