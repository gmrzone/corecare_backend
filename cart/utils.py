from django.conf import Settings, settings
from django.db.models import Case, When
from redis import Redis, StrictRedis

from .models import Service
from .serializers import ServiceSerializer

if settings.DEBUG:
    r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
else:
    r = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
    )


class Recommender:
    def generate_key(self, product_id: int) -> str:
        key = f"{product_id}_purchased_with"
        return key

    def create_recommandation_for(self, services: list) -> None:
        for item in services:
            for with_item in services:
                if int(item) != int(with_item):
                    key = self.generate_key(item)
                    r.zincrby(key, 1, with_item)

    def get_basic_recommandation(self, services, max_result=5) -> list:
        if len(services) == 1:
            suggestion = r.zrange(self.generate_key(services[0]), 0, -1, desc=True)
        elif len(services) > 1:
            suggestion_keys = [self.generate_key(id) for id in services]
            temp_key = "".join(str(i) for i in services) + "union"
            r.zunionstore(temp_key, suggestion_keys, "SUM")
            r.zrem(temp_key, *services)
            suggestion = r.zrange(temp_key, 0, -1, desc=True)
        suggestion = [int(id) for id in suggestion]
        suggestion = (
            suggestion[0:max_result] if len(suggestion) >= max_result else suggestion
        )
        return suggestion

    def get_detail_recommandation(self, services, max_result=5):
        suggestion_ids = self.get_basic_recommandation(services, max_result)
        if len(suggestion_ids) > 0:
            preserve_ids = Case(
                *[When(id=id, then=index) for index, id in enumerate(suggestion_ids)]
            )
            suggestion_services = Service.objects.filter(
                id__in=suggestion_ids
            ).order_by(preserve_ids)
            serializer = ServiceSerializer(suggestion_services, many=True)
            data = serializer.data
        else:
            data = []
        return data
