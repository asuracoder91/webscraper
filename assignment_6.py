# BLUEPRINT | DONT EDIT

import requests

movie_ids = [238, 680, 550, 185, 641, 515042, 152532, 120467, 872585, 906126, 840430]

# /BLUEPRINT

# 👇🏻 YOUR CODE 👇🏻:
API_URL = "https://nomad-movies.nomadcoders.workers.dev/movies/"

for i, movie_id in enumerate(movie_ids, start=1):
    response = requests.get(f"{API_URL}{movie_id}")
    data = response.json()
    print(f"{i}. {data['title']}")
    print(f"   - Overview : {data['overview']}")
    print(f"   - Rating   : {data['vote_average']:.1f}\n")

# /YOUR CODE
