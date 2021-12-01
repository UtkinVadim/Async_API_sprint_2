from typing import List, Union


async def flatten_json(obj) -> List:
    """
    "Плющит" входной объект.

    Пример работы:
    {'a': {'b': 'c'}} -> ['a', 'b', 'c']

    :param obj:
    :return:
    """
    body_list = []

    async def flatten(x):
        if isinstance(x, dict):
            for a in x:
                body_list.append(a)
                await flatten(x[a])
        elif isinstance(x, list):
            for a in x:
                await flatten(a)
        else:
            body_list.append(x)

    await flatten(obj)
    return body_list


async def key_generator(index: str, body: Union[dict, str]) -> str:
    """
    Создаёт ключ для редиса, по которому будут храниться данные.
    Структура ключа:
    <es_index>::<first_key>::<first_value>::<second_key>::<second_value>

    :param index:
    :param body:
    :return:
    """

    body_list = await flatten_json(body)
    keys_list = [index, *body_list]
    separate_symbol = "::"
    key = separate_symbol.join(keys_list)

    return key
