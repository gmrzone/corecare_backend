from redis import Redis, StrictRedis
from django.conf import Settings, settings
from .serializers import ServiceSerializer
from .models import Service
if settings.DEBUG:
    r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
else:
    r = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=Settings.REDIS_D, password=settings.REDIS_PASSWORD)

class Recommender:

    def generate_key(self, product_id: int) -> str:
        key = f"{product_id}_purchased_with"
        return key

    def create_recommandation_for(self, services: list) -> None:
        for item in services:
            for with_item in services:
                if item != with_item:
                    key = self.generate_key(item)
                    r.zincrby(key, 1, with_item)


    def get_basic_recommandation(self, services, max_result=5) -> list:
        services_id = [service.id for service in services]
        if len(services_id) == 1:
            suggestion = r.zrange(self.generate_key(services_id[0]), 0, -1, desc=True)
        else:
            suggestion_keys = [self.generate_key(id) for id in services_id]
            temp_key = "".join(services_id) + "union"
            r.zunionstore(temp_key, suggestion_keys)
            r.zrem(temp_key, *services_id)
            suggestion = r.zrange(temp_key, 0, 1, desc=True)
        suggestion = [int(id) for id in suggestion]
        return suggestion[max_result]

    def get_detail_recommandation(self, services, max_result: 5):
        suggestion_ids = self.get_basic_recommandation(services, max_result)
        suggestion_services = Service.objects.filter(id__in=suggestion_ids)
        serializer = ServiceSerializer(suggestion_services, many=True)
        print(serializer.data)


