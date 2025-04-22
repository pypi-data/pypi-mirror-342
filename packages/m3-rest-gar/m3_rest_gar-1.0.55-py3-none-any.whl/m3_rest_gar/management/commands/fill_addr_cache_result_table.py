import json
import logging
from collections import (
    defaultdict,
)

from django.core.management import (
    BaseCommand,
)
from m3_gar.models.addrobj import (
    AddrCacheResult,
    AddrObj,
)
from m3_rest_gar.views import (
    AddrObjViewSet,
)
from rest_framework.test import (
    APIRequestFactory,
)


# Уровни адресных объектов
LEVELS = ('1', '2', '5', '6')
OBJECTS_TO_CREATE_BATCH = 350


class Command(BaseCommand):
    """
    Команда заполняет данными таблицу m3_gar_addrcacheresult
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--page_num',
            '-pn',
            default=2,
            type=int,
            help='Кол-во страниц по конкретному запросу адреса',
        )
        parser.add_argument(
            '--truncate_table',
            '-tt',
            default=False,
            type=bool,
            help='Полностью очищает таблицу перед заполнением',
        )

    def handle(self, **options):
        logging.basicConfig(level=logging.INFO)
        factory = APIRequestFactory()
        page_num = options['page_num']

        if options['truncate_table']:
            AddrCacheResult.objects.all().delete()

        # Кол-во загруженных записей на уровне
        log_counter_dict = defaultdict(int)
        for level in LEVELS:
            names = AddrObj.objects.filter(
                level=level,
                typename='г',
                isactive=True,
                isactual=True,
            ).values_list('name', flat=True)

            to_create = []
            for name in names:
                name = name.lower()
                for page in range(1, page_num + 1):
                    page = str(page)
                    request = factory.get(
                        '/gar/v1/addrobj/',
                        {'name_with_parents': f'mun:город {name}', 'page': page},
                        format='json'
                    )

                    view = AddrObjViewSet.as_view({'get': 'list'})
                    response = view(request)

                    try:
                        result_json = json.dumps(response.data['results'])
                    except KeyError:
                        continue

                    to_create.append(AddrCacheResult(
                        name=name,
                        page=page,
                        data=result_json,
                    ))
                    log_counter_dict[level] += 1

                    if len(to_create) == OBJECTS_TO_CREATE_BATCH:
                        AddrCacheResult.objects.bulk_create(to_create)
                        logging.info(f'Загружено {log_counter_dict[level]} записей на уровне {level}')
                        to_create.clear()

            AddrCacheResult.objects.bulk_create(to_create)
            logging.info(f'Загружено {log_counter_dict[level]} записей на уровне {level}')
