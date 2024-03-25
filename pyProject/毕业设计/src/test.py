from Particle import Particle
from util import dominates


p = Particle.create(3, 10)
p.updateBest(1, 2, dominates)

print(p)