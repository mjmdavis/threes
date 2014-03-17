"""threes! this is a selection of classes for playing with the game 
of the same name.
"""
import random
import copy

Up = 0
Down = 1
Left = 2
Right = 3


class Grid:
    """A threes game grid.
    This encapsulates the model and the actions associated with the board
    """

    def __init__(self, startPosition=None, randSeed=None):
        """startPosition: optional lol (list of rows) in row notation
        generator: optionally provide a generator for nextTile
        """
        self.tileGen = random.Random()
        self.tileInsertionGen = random.Random()
        self.directions = dict()
        self.moves = 0
        self.tileQ = []
        self.empty = False
        if randSeed:
            self.randGen.seed(randSeed)
            self.randInsertionGen.seed(self.randGen.random())

        if startPosition:
            sp = tuple(map(tuple, startPosition))
            self.grid = Grid.saneCheck(sp)
            if self.grid == tuple([tuple([None]*4)]*4):
                self.empty = True
        else:
            self.grid = tuple([tuple([None]*4)]*4)
            self.empty = True

    def __repr__(self):
        decStrs = list()
        decStrs.append('threesGrid score: ' + str(int(self.score())) + ' moves: ' + str(self.moves))
        for row in self.grid:
            s = [str(i) if i!=None else '' for i in row]
            s = '[{:>2},{:>2},{:>2},{:>2}]'.format(*s)
            decStrs.append(s)
        return ',\n'.join(decStrs)

    @classmethod
    def saneCheck(cls, grid):
        assert type(grid) == tuple
        assert False not in [ type(i) == tuple for i in grid]
        assert len(grid) == 4
        assert map(len, grid) == [4,4,4,4]
        assert False not in [i in range(-2,12) for l in grid for i in l if i != None]
        return grid


    def ended(self):
        if not (self.up or self.down or self.left or self.right):
            return self.score()
        else:
            return False

    def score(self):
        return sum([pow(3,i+1) for r in self.grid for i in r if i >= 0])

    @property
    def up(self):
        return self._direction(Up)
    
    @property
    def down(self):
        return self._direction(Down)

    @property
    def left(self):
        return self._direction(Left)
    
    @property
    def right(self):
        return self._direction(Right)

    def direction(self, direction):
        return self._direction(direction)
            
    def _direction(self, direction):
        if direction in self.directions.keys():
            return self.directions[direction]
        else:
            movedGrid = self._moveGrid(direction)
            if movedGrid:
                newDirection = self._createDirection(movedGrid, direction)
                self.directions[direction] = newDirection
            else:
                self.directions[direction] = None
        return self.directions[direction]

    def _createDirection(self, newGrid, direction):
        new = copy.deepcopy(self)
        new.grid = newGrid
        new.moves += 1
        new.directions = dict()
        new._insertTile(direction)
        return new

    """
    def __copy__(self):
    """


    def _insertTile(self, direction):
        g = self._flip(self.grid, direction)
        insertable = [x for x in g if x[-1] == None]
        if len(insertable) > 0:
            newTile = self._nextTile()
        insertable[self.tileInsertionGen.randrange(len(insertable))][-1] = newTile
        self.grid = self._unflip(g, direction)
        if self.empty:
            self.empty = False
    
    def _nextTile(self):
        if self.tileQ == []:
            self.tileQ = [-1]*4 + [-2]*4 + [0]*4
            self.tileGen.shuffle(self.tileQ)
        return self.tileQ.pop()

    def _flip(self, grid, direction):
        g = [list(x) for x in grid]
        
        #transpose if vertical
        if direction == Up or direction == Down:
            g = _transpose(g)
        #reverse if lower right
        if direction == Down or direction == Right:
            g = _reverse(g)
        return g

    def _unflip(self, grid, direction):
        #reverse if lower right
        if direction == Down or direction == Right:
            grid = _reverse(grid)
        #transpose if vertical
        if direction == Up or direction == Down:
            grid = _transpose(grid)

        g = tuple([tuple(x) for x in grid])
        return g

    def _moveGrid(self, direction, nextTile=None, nextTileIdx=None):
        """Swipe the grid in a certain direction.
        direction: Up, Down, Left or Right, 1,2,3,4 resp.
        nextTile: optionally provide a nextTile for the grid.
        """
        moved = []
        g = self._flip(self.grid, direction)

        #for each row/column
        for x in range(len(g)):
            l = g[x]
            moved.append(0)
            for i in range(3):
                if l[i] == None:
                    if max(l[i:]) > None:
                        del l[i]
                        l.append(None)
                        moved[x] += 1
                        break
                elif -1 in l[i:i+2] and -2 in l[i:i+2]:
                    l[i] = 0
                    del l[i+1]
                    l.append(None)
                    moved[x] += 1
                    break
                elif l[i] >= 0 and l[i] == l[i+1]:
                    l[i] += 1
                    del l[i+1]
                    l.append(None)
                    moved[x] += 1
                    break
        #    if moved[x] == 0:
        #        moved[x] = None == l[-1]
        #print 'moved: ' + str(moved)
        if sum(moved) == 0 and not self.empty:
            return None

        return self._unflip(g, direction)

"""
class tileStack:
    def __init__(self):
        self.randomo

    def 
"""


def _transpose(lol):
    return map(list, zip(*lol))

def _reverse(lol):
    map(lambda x: x.reverse(), lol)
    return lol

