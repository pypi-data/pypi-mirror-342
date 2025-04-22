import redis
import sys
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen

@dataclass
class TimeSeriesGen(BaseGen):
    max_actions: int = 5
    max_float = sys.maxsize
    labels_dict = {
        "furniture": ["chair", "table", "desk", "mouse", "keyboard", "monitor", "printer", "scanner"],
        "fruits": ["apple", "banana", "orange", "grape", "mango"],
        "animals": ["dog", "cat", "elephant", "lion", "tiger"]
    }
    def tscreate(self, pipe: redis.client.Pipeline, key: str = None) -> None:
        # Classification: addition
        if key is None:
            key = self._rand_key()

        key = "ts-" + key
        pipe.ts().create(key)

    def tsadd(self, pipe: redis.client.Pipeline, key: str = None) -> None:
        # Classification: addition

        if key is None:
            key = self._rand_key()
        key = "ts-" + key

        timestamp = int(random.uniform(0, 1000000))  # Generate a random timestamp

        for _ in range(random.randint(2, self.max_actions)):
            value = random.uniform(1, self.max_float)  # Generate a random float value
            pipe.ts().add(key=key, timestamp=timestamp, value=value, duplicate_policy="last")

    def tsalter (self, pipe: redis.client.Pipeline, key: str = None) -> None:
        # Classification: alteration
        redis_obj = self._pipe_to_redis(pipe)

        if key is None or not redis_obj.exists(key):
            key = self._scan_rand_key(redis_obj, "TSDB-TYPE")
        if not key: return

        laebl1 = random.choice(list(self.labels_dict.keys()))
        label2 = random.choice(list(self.labels_dict.keys()))
        # Generate a random label value
        label1_value = random.choice(self.labels_dict[laebl1])
        label2_value = random.choice(self.labels_dict[label2])

        pipe.ts().alter(key, retention_msecs=random.randint(1000,100000), labels={laebl1: label1_value, label2: label2_value})

    def tsqueryindex(self, pipe: redis.client.Pipeline, key: str = None) -> None:
        # Classification: retrieval
        redis_obj = self._pipe_to_redis(pipe)

        label = random.choice(list(self.labels_dict.keys()))
        label_value = random.choice(self.labels_dict[label])

        pipe.ts().queryindex([f"{label}={label_value}"])

    def tsdel(self, pipe: redis.client.Pipeline, key: str = None) -> None:
        # Classification: removal-value
        redis_obj = self._pipe_to_redis(pipe)

        if key is None or not redis_obj.exists(key):
            key = self._scan_rand_key(redis_obj, "TSDB-TYPE")
        if not key: return

        pipe.ts().delete(key, 0, int(1e12))

    def tsdelkey(self, pipe: redis.client.Pipeline, key: str = None) -> None:
        # Classification: removal-key
        redis_obj = self._pipe_to_redis(pipe)

        if key is None or not redis_obj.exists(key):
            key = self._scan_rand_key(redis_obj, "TSDB-TYPE")
        if not key: return

        pipe.delete(key)


if __name__ == "__main__":
    ts_gen = parse(TimeSeriesGen)
    ts_gen.distributions = '{"tscreate":100, "tsadd": 100, "tsdel": 100, "tsalter":100, "tsqueryindex":100}'
    ts_gen._run()