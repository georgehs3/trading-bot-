import json
import logging

import redis


class RedisCache:
    """Implements Redis caching to store frequently accessed stock and news data."""

    def __init__(self, host="localhost", port=6379, db=0, expiration_time=3600):
        self.logger = logging.getLogger(__name__)
        try:
            self.redis_client = redis.Redis(
                host=host, port=port, db=db, decode_responses=True
            )
            self.expiration_time = expiration_time  # Default cache expiration: 1 hour
            self.logger.info("Connected to Redis cache successfully.")
        except Exception as e:
            self.logger.error(f"Redis connection failed: {e}")
            self.redis_client = None

    def set_cache(self, key, data):
        """Stores data in Redis cache with an expiration time."""
        if self.redis_client:
            try:
                self.redis_client.setex(key, self.expiration_time, json.dumps(data))
                self.logger.info(f"Cached data for {key}")
            except Exception as e:
                self.logger.error(f"Failed to cache data for {key}: {e}")

    def get_cache(self, key):
        """Retrieves data from Redis cache."""
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                self.logger.error(f"Failed to retrieve cache for {key}: {e}")
        return None

    def delete_cache(self, key):
        """Removes a specific cache entry."""
        if self.redis_client:
            try:
                self.redis_client.delete(key)
                self.logger.info(f"Deleted cache for {key}")
            except Exception as e:
                self.logger.error(f"Failed to delete cache for {key}: {e}")

    def clear_all_cache(self):
        """Clears all cached data."""
        if self.redis_client:
            try:
                self.redis_client.flushdb()
                self.logger.info("Cleared all Redis cache.")
            except Exception as e:
                self.logger.error(f"Failed to clear Redis cache: {e}")


# Usage Example:
if __name__ == "__main__":
    cache = RedisCache(expiration_time=600)  # Cache expires after 10 minutes
    cache.set_cache("AAPL_stock_price", {"price": 150.25, "volume": 5000000})
    cached_data = cache.get_cache("AAPL_stock_price")
    print(f"Retrieved Cache: {cached_data}")
