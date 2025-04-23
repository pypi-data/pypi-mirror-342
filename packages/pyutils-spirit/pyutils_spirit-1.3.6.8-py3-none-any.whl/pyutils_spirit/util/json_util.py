import json

import datetime


class JsonUtil:

    @staticmethod
    def json_handle_iterable(iterable: [list | tuple | set]) -> list | tuple | set:
        container_type = type(iterable)
        if not isinstance(iterable, (list, tuple, set)):
            raise TypeError('the argument must be a list or tuple or set')

        processed = []
        for item in iterable:
            if isinstance(item, (list, tuple, set)):
                processed.append(JsonUtil.json_handle_iterable(item))
            elif isinstance(item, dict):
                processed.append(JsonUtil.json_handle_dict(item))
            elif isinstance(item, str):
                try:
                    parsed = json.loads(item)
                    if isinstance(parsed, dict):
                        processed.append(JsonUtil.json_handle_dict(parsed))
                    elif isinstance(parsed, (list, tuple, set)):
                        processed.append(JsonUtil.json_handle_iterable(parsed))
                except json.JSONDecodeError:
                    processed.append(item)
            elif isinstance(item, datetime.datetime):
                processed.append(item.isoformat())
            else:
                processed.append(item)

        return container_type(processed)

    @staticmethod
    def json_handle_dict(data: dict) -> dict:
        if not isinstance(data, dict):
            raise TypeError('the argument must be a dict')

        for key in list(data.keys()):
            value = data[key]
            if isinstance(value, str):
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, dict):
                        data[key] = JsonUtil.json_handle_dict(parsed)
                    elif isinstance(parsed, (list, tuple, set)):
                        data[key] = JsonUtil.json_handle_iterable(parsed)
                except json.JSONDecodeError:
                    pass
            elif isinstance(value, (list, tuple, set)):
                data[key] = JsonUtil.json_handle_iterable(value)
            elif isinstance(value, dict):
                data[key] = JsonUtil.json_handle_dict(value)
            elif isinstance(value, datetime.datetime):
                data[key] = value.isoformat()
        return data
