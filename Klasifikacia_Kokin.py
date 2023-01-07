import random
from math import sqrt
from typing import Tuple


# creating class that stands for point with x, y coordinates and variable for group,
# where 1 - red, 2 - green, 3 - blue, 4 - purple
class point:
    x: int
    y: int
    clr: int
    # if clr keeps value that classify function has given it
    # area variable keeps value of the area where it has been generated (one of the four possible)
    # where 1 - area for reds, 2 - greens, 3 - blues, 4 - purples
    area: int
    # sct variable keeps the value representing the number of sector that point is a part of
    sct: int

    def __init__(self, x, y, clr, area, sct):
        self.x = x
        self.y = y
        self.clr = clr
        self.area = area
        self.sct = sct

    def set_sector(self, sct):
        self.sct = sct

    def get_sector(self):
        return self.sct

    def set_clr(self, clr):
        self.clr = clr

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_clr(self):
        return self.clr

    def get_area(self):
        return self.area


# this is the implementation of the optimization
# class represents a sector 100x100 with the center point
class sector:
    x: int
    y: int
    num: int

    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

    def get_num(self):
        return self.num

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


# type of variable that represents our map with 10 000 x 10 000 points
MAP = list[list[point]]
BLOCKED = list[Tuple[int, int]]
SECTORS = list[sector]


# finding the sector selected point is in
def find_sector(x: int, y: int, sectors: SECTORS) -> int:
    # sorting our sectors so the first one on the list is the one our point in
    s_sectors = sorted(
        sectors,
        key=lambda j: calculate_distance(x, y, j.get_x(), j.get_y()),
        reverse=False
    )

    return s_sectors[0].get_num()


def init_map(sectors_cnt: int) -> Tuple[MAP, BLOCKED, SECTORS]:
    # amount of points in one row in one sector
    points_cnt = 10000/sectors_cnt
    # first - we initialize the sectors
    sectors = []
    # the middle point of the first sector will be -4950, 4950
    s_x = -5000 + points_cnt/2
    s_y = 5000 - points_cnt/2
    for i in range(sectors_cnt):
        for u in range(sectors_cnt):
            sectors.append(sector(s_x, s_y, (u+(i*sectors_cnt))))
            s_x += points_cnt
        s_x = -5000 + points_cnt/2
        s_y -= points_cnt
    # in the result we will have n sectors in one row that makes n*n sectors whole map
    # for example we have 100 sectors in a row, map will be 10000 sectors
    # list of the points that already has been classified
    starters = []
    blocked = []
    # setting the starter points from the conditions of the task
    starters += [point(-4500, -4400, 1, 1, 0), point(-4100, -3000, 1, 1, 0), point(-1800, -2400, 1, 1, 0),
                 point(-2500, -3400, 1, 1, 0), point(-2000, -1400, 1, 1, 0)]
    starters += [point(4500, -4400, 2, 2, 0), point(4100, -3000, 2, 2, 0), point(1800, -2400, 2, 2, 0),
                 point(2500, -3400, 2, 2, 0), point(2000, -1400, 2, 2, 0)]
    starters += [point(-4500, 4400, 3, 3, 0), point(-4100, 3000, 3, 3, 0), point(-1800, 2400, 3, 3, 0),
                 point(-2500, 3400, 3, 3, 0), point(-2000, 1400, 3, 3, 0)]
    starters += [point(4500, 4400, 4, 4, 0), point(4100, 3000, 4, 4, 0), point(1800, 2400, 4, 4, 0),
                 point(2500, 3400, 4, 4, 0), point(2000, 1400, 4, 4, 0)]

    # creating the list of the sectors with actual points
    mapp: MAP = []
    for h in range(sectors_cnt**2):
        mapp.append([])

    # adding the starter points to their sectors
    for t in starters:
        index = find_sector(t.get_x(), t.get_y(), sectors)
        # get the sector and append there a point
        mapp[index].append(t)

    blocked += [[-4500, -4400], [-4100, -3000], [-1800, -2400], [-2500, -3400], [-2000, -1400]]
    blocked += [[4500, -4400], [4100, -3000], [1800, -2400], [2500, -3400], [2000, -1400]]
    blocked += [[-4500, 4400], [-4100, 3000], [-1800, 2400], [-2500, 3400], [-2000, 1400]]
    blocked += [[4500, 4400], [4100, 3000], [1800, 2400], [2500, 3400], [2000, 1400]]

    return mapp, blocked, sectors


# function that finds distance between two points byy Pythagorean theorem
def calculate_distance(start_x: int, start_y: int, finish_x: int, finish_y) -> float:
    # we can't take to the calculations points without color
    """if finish.get_clr() == 0:
        return 1000000.0"""

    cat1 = abs(finish_x - start_x)
    cat2 = abs(finish_y - start_y)

    dist = abs(sqrt(cat1**2 + cat2**2))

    return dist


def expand_sectors(cur: int, n_range: int, sectors_id: list, sectors_cnt: int) -> list[int]:

    stop_left = False
    stop_right = False

    if cur % sectors_cnt == 0:
        stop_left = True
    if (cur+1) % sectors_cnt == 0:
        stop_right = True

    # we begin with adding all the upper and down neighbours
    for w in range(1, n_range+1):
        # when we get to the left corner of the map, which is every 100 index,
        # we stop going to the left and remains only right side
        if (cur - w) % sectors_cnt == 0 and w != n_range:
            sectors_id.append(cur - (sectors_cnt * n_range) - w)
            sectors_id.append(cur + (sectors_cnt * n_range) - w)
            stop_left = True
        if (cur + 1 + w) % sectors_cnt == 0 and w != n_range:
            sectors_id.append(cur - (sectors_cnt * n_range) + w)
            sectors_id.append(cur + (sectors_cnt * n_range) + w)
            stop_right = True
        # if we didn't get to the border yet - we add sectors to the list
        if stop_left is False:
            sectors_id.append(cur - (sectors_cnt * n_range) - w)
            sectors_id.append(cur + (sectors_cnt * n_range) - w)
        if stop_right is False:
            sectors_id.append(cur - (sectors_cnt * n_range) + w)
            sectors_id.append(cur + (sectors_cnt * n_range) + w)

    # if we didn't get to the border - we add all the sectors in range from the left
    if stop_left is False:
        for hl in range(n_range):
            if hl == 0:
                sectors_id.append(cur - (sectors_cnt * hl) - n_range)
            else:
                sectors_id.append(cur - (sectors_cnt * hl) - n_range)
                sectors_id.append(cur + (sectors_cnt * hl) - n_range)

    # the same thing for the right side:
    if stop_right is False:
        for hr in range(n_range):
            if hr == 0:
                sectors_id.append(cur - (sectors_cnt * hr) + n_range)
            else:
                sectors_id.append(cur - (sectors_cnt * hr) + n_range)
                sectors_id.append(cur + (sectors_cnt * hr) + n_range)

    return sectors_id


# function to collect all the points of the neighbour sectors to one list
# n_range will decide how many layers neighbours to skip to get the points,
# for example n_range = 0 will get the points of the closest neighbours
def get_sectors(cur: int, mapp: MAP, n_range: int, sectors_cnt: int) -> list[point]:
    points_cnt = int(10000/sectors_cnt)
    res = []
    sectors_id = []
    # cur - sector of our point
    if n_range == 0:
        sectors_id += [cur]
    else:
        # first things first we are getting sectors that are right above and below
        sectors_id += [cur + sectors_cnt * n_range, cur - sectors_cnt * n_range]
        # then we move from those we just got to the left and right and then down, so it makes a square
        expand_sectors(cur, n_range, sectors_id, sectors_cnt)

    # deleting every element that is out of range
    sectors_new = sectors_id.copy()
    for j in sectors_id:
        if j < 0 or j > ((sectors_cnt*sectors_cnt)-1):
            sectors_new.remove(j)

    # then we take every sector we found
    for s in sectors_new:
        # check points for classified ones
        if len(mapp[s]) != 0:
            for dot in mapp[s]:
                # and if it is classified we add it to the list of neighbours
                res.append(dot)

    return res


# function for classifying the point to some group
def classify(p: point, k: int, mapp: MAP, sectors_cnt: int) -> int:
    if p.get_clr() != 0:
        return p.get_clr()

    # found points to observe
    found = 0
    n_range = 0
    neighbours = []
    # until we find enough points from our neighbours we will continue
    while found < k:
        neighbours += get_sectors(p.get_sector(), mapp, n_range, sectors_cnt)
        found = len(neighbours)
        # if we still didn't find enough neighbours then we simply increase our range and check further ones
        n_range += 1

    # sorting our lists of the all points in the neighbour sectors so on the first places will be the closest
    # ones to our selected point to classify
    closest = sorted(
        neighbours,
        key=lambda l: calculate_distance(p.get_x(), p.get_y(), l.get_x(), l.get_y()),
        reverse=False
    )

    # in cycle for k iterations we are counting what group of points we meet most often
    red = green = blue = purple = 0
    for i in range(k):
        if closest[i].get_clr() == 1:
            red += 1
        elif closest[i].get_clr() == 2:
            green += 1
        elif closest[i].get_clr() == 3:
            blue += 1
        elif closest[i].get_clr() == 4:
            purple += 1

    group = [red, green, blue, purple]

    # adding our point to the list of classified points
    mapp[p.get_sector()].append(p)

    # find the group that happens to be closest to the point
    # and add our point to this group
    group = sorted(
        group,
        reverse=True
    )

    if group[0] == red:
        # setting the color of the point red
        p.set_clr(1)
        return 1
    elif group[0] == green:
        p.set_clr(2)
        return 2
    elif group[0] == blue:
        p.set_clr(3)
        return 3
    else:  # group.index(max(group)) == 4:
        p.set_clr(4)
        return 4


def classify_sup_pts(x: int, y: int, sec: int, k: int, mapp: MAP, sectors_cnt: int) -> str:
    # found points to observe
    found = 0
    n_range = 0
    neighbours = []
    # until we find enough points from our neighbours we will continue
    while found < k:
        neighbours += get_sectors(sec, mapp, n_range, sectors_cnt)
        found = len(neighbours)
        # if we still didn't find enough neighbours then we simply increase our range and check further ones
        n_range += 1

    # sorting our lists of the all points in the neighbour sectors so on the first places will be the closest
    # ones to our selected point to classify
    closest = sorted(
        neighbours,
        key=lambda l: calculate_distance(x, y, l.get_x(), l.get_y()),
        reverse=False
    )

    # in cycle for k iterations we are counting what group of points we meet most often
    red = green = blue = purple = 0
    for i in range(k):
        if closest[i].get_clr() == 1:
            red += 1
        elif closest[i].get_clr() == 2:
            green += 1
        elif closest[i].get_clr() == 3:
            blue += 1
        elif closest[i].get_clr() == 4:
            purple += 1

    group = [red, green, blue, purple]

    group = sorted(
        group,
        reverse=True
    )

    if group[0] == red:
        return "red"
    elif group[0] == green:
        return "green"
    elif group[0] == blue:
        return "blue"
    else:  # group.index(max(group)) == 4:
        return "purple"


# function that generates point from certain range due to the parameter clr
# 1% of probability that point will be randomly chosen from the whole range
def generate_point(clr: int, k: int, mapp: MAP, blocked: BLOCKED, probability: float = 0.98) -> point:
    x = 0
    y = 0
    area = 0
    # 99% that we choose our point from the certain range
    if random.random() < probability:
        if clr == 1:
            # if next colour in the queue is 1 (red) then we and choose
            # point from -5000 to 500 for x and for y
            x = random.randint(-5000, 500)
            y = random.randint(-5000, 500)
            area = 1
            # as long as it is the same with the point we already classified
            # we randomly pick another one point form the range
            while [x, y] in blocked:
                x = random.randint(-5000, 500)
                y = random.randint(-5000, 500)
        elif clr == 2:
            x = random.randint(-500, 5000)
            y = random.randint(-5000, 500)
            area = 2
            while [x, y] in blocked:
                x = random.randint(-500, 5000)
                y = random.randint(-5000, 500)
        elif clr == 3:
            x = random.randint(-5000, 500)
            y = random.randint(-500, 5000)
            area = 3
            while [x, y] in blocked:
                x = random.randint(-5000, 500)
                y = random.randint(-500, 5000)
        elif clr == 4:
            x = random.randint(-500, 5000)
            y = random.randint(-500, 5000)
            area = 4
            while [x, y] in blocked:
                x = random.randint(-500, 5000)
                y = random.randint(-500, 5000)
    else:
        x = random.randint(-5000, 5000)
        y = random.randint(-5000, 5000)
        while [x, y] in blocked:
            x = random.randint(-5000, 5000)
            y = random.randint(-5000, 5000)

    blocked.append((x, y))
    res = point(x, y, 0, area, 0)

    return res







