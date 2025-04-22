import functools
import json
from collections.abc import (
    Iterable,
)
from uuid import (
    UUID,
)
from django.conf import (
    settings,
)
from m3_gar.models import (
    AddrCacheResult,
)
from m3_gar.models.hierarchy import (
    Hierarchy,
)
from rest_framework.response import (
    Response,
)


# Пример административного деления
# 33634065 - д 54
# 210826 - ул Заречная
# 210984 - с Кунгуртуг
# 213492 - р-н Тере-Хольский
# 206101 - Респ Тыва

# Пример муниципального деления
# 33634065 - д 54
# 210826 - ул Заречная
# 210984 - с Кунгуртуг
# 95235279 - с.п. Шынаанский
# 95235278 - м.р-н Тере-Хольский
# 206101 - Респ Тыва


def get_hierarchy_models(hierarchy):
    """Возвращает список моделей иерархии по заданному коду (или нескольким кодам).

    Args:
        hierarchy: Код или список кодов иерархии.
            Примеры: 'adm', 'mun', 'any', ['adm', 'mun']

    Returns:
        Список классов моделей иерархии

    Raises:
        ValueError: неверный код иерархии
    """

    hierarchy_model_map = Hierarchy.get_shortname_map()

    if hierarchy == 'any':
        hierarchy = hierarchy_model_map.keys()
    elif isinstance(hierarchy, str):
        hierarchy = [hierarchy]
    elif isinstance(hierarchy, Iterable):
        pass
    else:
        raise ValueError(f'Invalid hierarchy value: {hierarchy}')

    try:
        hierarchy_models = [hierarchy_model_map[h] for h in hierarchy]
    except KeyError as e:
        raise ValueError(f'Invalid hierarchy value: {e}')

    return hierarchy_models


def is_objectguid(value):
    try:
        UUID(value)
    except ValueError:
        result = False
    else:
        result = True

    return result


def get_cached_addr_results(fn):
    """
    Возвращает, сохранённые в БД, результаты запроса по конкретному адресу при
    включённой настройке USE_CACHED_ADDR_RESULTS

    Args:
        fn: AddrObjViewSet.list
    """
    @functools.wraps(fn)
    def wrapper(view_self, request, *args, **kwargs):
        response = None

        if settings.USE_CACHED_ADDR_RESULTS and not request.query_params.get('parent'):
            page = request.query_params['page']
            name = request.query_params['name_with_parents'].lower()
            name = name.replace('mun:', '').strip()
            name = name.replace('город ', '').replace('г.', '').replace('г ', '').strip()

            cache_result = AddrCacheResult.objects.filter(name=name, page=page).first()
            if cache_result:
                data = json.loads(cache_result.data)
                response = Response({'results': data, 'next': None})

        if not response:
            response = fn(view_self, request, *args, **kwargs)

        return response

    return wrapper
