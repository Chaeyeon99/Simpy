import random
import simpy

RANDOM_SEED = 42
NEW_CUSTOMERS = 30
INTERVAL_CUSTOMERS = 2.0
MIN_PATIENCE = 1
MAX_PATIENCE = 3
PT_MEAN = 10.0
PT_SIGMA = 2.0


def source(env, number, interval, counter):
    for i in range(number):
        c = customer(env, "Customer%02d" % i, counter, time_in_bank=random.normalvariate(PT_MEAN, PT_SIGMA))
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


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
            print('%7.4f %s : Finished, time_in_bank: %.2f' % (env.now, name, time_in_bank))

        else:  # 1-d
            print('%7.4f %s : RENEGED after %6.3f' % (env.now, name, wait))


print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

counter = simpy.Resource(env, capacity=3)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()
