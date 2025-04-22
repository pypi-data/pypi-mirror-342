import redis_command_generator as cg
import redis

gen_runner = cg.GenRunner(hosts=("3.253.21.167:6380",), max_cmd_cnt=10000, pipe_every_x=100, logfile="/tmp/bla.txt", verbose=True, maxmemory_bytes=100000000000, flush=True)
gen_runner.start()
print(gen_runner.join())

# base_gen = cg.BaseGen(hosts=("3.253.21.167:6380",), verbose=True, pipe_every_x=1, distributions = '{"expire": 100, "persist": 100}')
# base_gen._run()

# r = redis.Redis(host="3.253.21.167", port="6380")
# r.set("test_key", "Hello Redis Cluster!")
# value = r.get("test_key")
# print(f"Retrieved value: {value}")