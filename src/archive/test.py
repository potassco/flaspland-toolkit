import pickle
import sys

with open(sys.argv[1], 'rb') as f:
    env = pickle.load(f)

print(env.agents[0])
