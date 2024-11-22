from dramatiq import set_broker
from dramatiq.brokers.redis import RedisBroker
from django.conf import settings

broker = RedisBroker(url=settings.DRAMATIQ_BROKER['REDIS_URL'])
set_broker(broker)
