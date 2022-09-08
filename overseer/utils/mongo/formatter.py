from typing import List


def format_collection(query_results) -> List[dict]:
    formatted = []
    for result in query_results:
        if '_id' in result:
            result['_id'] = str(result['_id'])
        formatted.append(result)

    return formatted


def format_single_element(element) -> dict:
    if '_id' in element:
        element['_id'] = str(element['_id'])

    return element


