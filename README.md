threes
======

Model of threes game

```Python
g = threes.Grid()
g = g.up
g = g.left

while g.up:
  g = g.up

def measure():
    gs = []
    for i in range(10):
        g = threes.Grid()
        while not g.ended():
            l = map(lambda x: g.direction(x), range(4))
            l = [0 if x == None else x.score() for x in l]
            idx = l.index(max(l))
            g = g.direction(idx)
        gs.append(g)
    return gs

gs = measure()
