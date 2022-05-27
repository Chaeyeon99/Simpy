import itertools
import random
import simpy

RANDOM_SEED = 42
MIN_PATIENCE = 1
MAX_PATIENCE = 3
SIMULATE_TIME = 1000

def source(env, counter):
        for i in itertools.count():
            yield env.timeout(random.randint(0,20))
            c = customer(env, "Customer%02d" %i, counter, time_in_bank=20.0)
            env.process(c)


def customer(env, name, counter, time_in_bank):
    arrive = env.now
    print('%7.4f %s : Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            print('%7.4f %s : Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%7.4f %s : Finished' % (env.now, name))

        else:  # 1-d
            print('%7.4f %s : RENEGED after %6.3f' % (env.now, name, wait))


print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

counter = simpy.Resource(env, capacity=2)
env.process(source(env, counter))
env.run(until = SIMULATE_TIME)
