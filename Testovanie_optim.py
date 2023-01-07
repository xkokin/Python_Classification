import time
from typing import Tuple

from Klasifikacia_Kokin import generate_point, init_map, point, classify, MAP, find_sector, classify_sup_pts, SECTORS
import matplotlib.pyplot as plt


# creating different objects of the map but with the same values (cloning)
# we have 100 sectors 100x100 points for optimization
def clone_map(mapp: MAP) -> MAP:
    map_res = []
    # un_class_res = []
    temp = []
    # here we take 1 of the sectors
    for i in mapp:
        # here we take each existing point of that sector and clone it
        for u in i:
            temp.append(point(u.get_x(), u.get_y(), u.get_clr(), u.get_area(), u.get_sector()))
        t = clone_points(temp)
        map_res.append(t.copy())
        # un_class_res += t.copy()
        temp.clear()

    return map_res


def clone_points(unclassified: list[point]) -> list[point]:
    res = []
    for i in unclassified:
        res.append(point(i.get_x(), i.get_y(), i.get_clr(), i.get_area(), i.get_sector()))

    return res


# function to supplement missing points in map
def supplement_points(k: int, blocked: list[tuple[int, int]], sectors: SECTORS, mapp: MAP, sectors_cnt: int) -> \
        Tuple[list[int], list[int], list[str]]:
    x = []
    y = []
    clr = []
    for r in range(-5000, 5000):
        for e in range(-5000, 5000):
            if (e, r) not in blocked:
                clr.append(classify_sup_pts(e, r, find_sector(e, r, sectors), k, mapp, sectors_cnt))
                x.append(e)
                y.append(r)

    return x, y, clr


def draw_graf(mapp: list[list[point]], x: list[int], y: list[int], clrs: list[str]):
    points = []
    for h in mapp:
        for j in h:
            points.append(j)

    for i in points:
        x.append(i.get_x())
        y.append(i.get_y())
        if i.get_clr() == 1:
            clrs.append("red")
        elif i.get_clr() == 2:
            clrs.append("green")
        elif i.get_clr() == 3:
            clrs.append("blue")
        elif i.get_clr() == 4:
            clrs.append("purple")

    plt.figure(figsize=(15, 15))
    plt.scatter(x, y, c=clrs, s=550, marker=".")
    plt.grid()
    plt.show()


def main():
    start_gen = time.time()
    # generate the starting map
    points_cnt = 50000
    # sectors_cnt = 100
    sectors_cnt = 50  # this gives us 50 sectors in a row and 50 rows, that makes 2500 sectors
    stats = []
    un_class1 = []
    un_class3 = []
    un_class7 = []
    un_class15 = []
    map1, blocked, sectors = init_map(sectors_cnt)
    cnt = 1
    # here we will sequentially create 40000 points switching from red through green and blue to purple
    # and from purple back to red
    for i in range(points_cnt):
        if cnt == 1:
            # generating a point
            p = generate_point(1, 3, map1, blocked)

            cnt += 1
        elif cnt == 2:
            p = generate_point(2, 3, map1, blocked)
            # map1[index].append(p)
            cnt += 1
        elif cnt == 3:
            p = generate_point(3, 3, map1, blocked)
            # map1[index].append(p)
            cnt += 1
        else:
            p = generate_point(4, 3, map1, blocked)
            # map1[index].append(p)
            cnt = 1

        # finding the index of the sector our point is in
        p.set_sector(find_sector(p.get_x(), p.get_y(), sectors))
        # adding our point to that sector and to the list of unclassified points
        un_class1.append(p)
        un_class3.append(point(p.get_x(), p.get_y(), p.get_clr(), p.get_area(), p.get_sector()))
        un_class7.append(point(p.get_x(), p.get_y(), p.get_clr(), p.get_area(), p.get_sector()))
        un_class15.append(point(p.get_x(), p.get_y(), p.get_clr(), p.get_area(), p.get_sector()))
        # map1[index].append(p)

    map3 = clone_map(map1)
    # un_class3 = clone_points(un_class1)
    map7 = clone_map(map1)
    # un_class7 = clone_points(un_class1)
    map15 = clone_map(map1)
    # un_class15 = clone_points(un_class1)

    maps = [(map1, 1, un_class1), (map3, 3, un_class3), (map7, 7, un_class7), (map15, 15, un_class15)]

    end_gen = time.time() - start_gen

    print(f"Cas inizializacii v sekundach: {end_gen}\n")

    # calling classifying function for each point for 4 possible k values (1, 3, 7, 15) separately
    for e in maps:
        start_gen = time.time()
        for j in e[2]:
            # if classify function did job right or point was created out of range then we write 1 to the list
            res = classify(j, e[1], e[0], sectors_cnt)
            if res == j.get_area() or j.get_area() == 0:
                stats.append(1)
            # else we write 0
            else:
                stats.append(0)
        end_gen = time.time() - start_gen
        # summing all the elements in stats list we will  find percentage of right classifications
        print(f"Testovanie z hodnotou k = {e[1]} bolo ukoncene,\n"
              f"Cas testovania v sekundach: {end_gen}\n"
              f"Pocet bodov vo svojom stvorce: {sum(stats)},\n"
              f"Pravidelnost vysledkov: {str(int((sum(stats)/points_cnt)*100))}%\n")
        # clearing the list for further iterations
        stats.clear()
        # supplementing the missing points
        # x, y, clrs = supplement_points(e[1], blocked, sectors, e[0], sectors_cnt)
        # drawing all the points we got from generating
        draw_graf(e[0], [], [], [])



if __name__ == "__main__":
    main()