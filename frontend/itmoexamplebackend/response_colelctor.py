import json

import requests

query_list = [
    "сигма",
    "альтушка",
    "пикмэ",
    "VIPERR",
]

your_local_backend_url = "http://127.0.0.1:5005"
your_backend_endpoint = "/api/search?query="


if __name__ == '__main__':
    result = {}

    for query in query_list:
        response = requests.get(your_local_backend_url + your_backend_endpoint + query)
        video_link = response.json()
        result[query] = video_link

    with open("result.json", "w", encoding="utf-8") as result_fp:
        json.dump(result, result_fp, ensure_ascii=False, indent=4)
