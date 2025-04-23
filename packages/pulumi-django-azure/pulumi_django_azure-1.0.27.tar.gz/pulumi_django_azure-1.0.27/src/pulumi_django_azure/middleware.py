import logging
import os

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.db.utils import OperationalError
from django.http import HttpResponse
from django_redis import get_redis_connection

from .azure_helper import db_token_will_expire, get_db_password, get_redis_credentials, redis_token_will_expire

logger = logging.getLogger("pulumi_django_azure.health_check")


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def _self_heal(self):
        # Send HUP signal to gunicorn main thread,
        # which will trigger new workers to start.
        os.kill(os.getppid(), 1)

    def __call__(self, request):
        if request.path == settings.HEALTH_CHECK_PATH:
            # Update the database credentials if needed
            if settings.AZURE_DB_PASSWORD:
                try:
                    if db_token_will_expire():
                        logger.debug("Database token will expire, fetching new credentials")
                        settings.DATABASES["default"]["PASSWORD"] = get_db_password()
                    else:
                        logger.debug("Database token is still valid, skipping credentials update")
                except Exception as e:
                    logger.error("Failed to update database credentials: %s", str(e))

                    self._self_heal()

                    return HttpResponse(status=503)

            # Update the Redis credentials if needed
            if settings.AZURE_REDIS_CREDENTIALS:
                try:
                    if redis_token_will_expire():
                        logger.debug("Redis token will expire, fetching new credentials")

                        redis_credentials = get_redis_credentials()

                        # Re-authenticate the Redis connection
                        redis_connection = get_redis_connection("default")
                        redis_connection.execute_command("AUTH", redis_credentials.username, redis_credentials.password)

                        settings.CACHES["default"]["OPTIONS"]["PASSWORD"] = redis_credentials.password
                    else:
                        logger.debug("Redis token is still valid, skipping credentials update")
                except Exception as e:
                    logger.error("Failed to update Redis credentials: %s", str(e))

                    self._self_heal()

                    return HttpResponse(status=503)

            try:
                # Test the database connection
                connection.ensure_connection()
                logger.debug("Database connection check passed")

                # Test the Redis connection
                cache.set("health_check", "test")
                logger.debug("Redis connection check passed")

                return HttpResponse("OK")

            except OperationalError as e:
                logger.error("Database connection failed: %s", str(e))
                return HttpResponse(status=503)
            except Exception as e:
                logger.error("Health check failed with unexpected error: %s", str(e))
                return HttpResponse(status=503)

        return self.get_response(request)
