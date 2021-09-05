import numpy as np
import matplotlib.pyplot as plt
import math

#Global Variables
X_MIN = 0
X_MAX = 100
Y_MIN = 0
Y_MAX = 100

THETA = 0.5

G = 6.67408 * 10**(-11)


class Point_2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + "," + str(self.y)

    def calc_distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y + other.y)**2)



class Body():
    def __init__(self, point, mass):
        self.position = point
        self.mass = mass

    def __str__(self):
        return "{ position : " + str(self.position) + "   " + "mass : " + str(self.mass) + "}"

    def calc_force(self, other):
        return G * (self.mass * other.mass) / self.position.calc_distance(other.position)


class Area():
    def __init__(self, point, length):
        self.position = point
        self.length = length

    def __str__(self):
        return "{position : " + str(self.position) + "  " + "length : " + str(self.length) + "}"



class Node():
    def __init__(self, area):
        self.status = -1
        self.depth = None
        self.body = None
        self.area = area
        self.children = None
        self.center_of_mass = Body(None, 0)

    def __str__(self):
        return "node : " + "{area : " + str(self.area) + " body : " + str(self.body) + "}"

    '''
    way of devision
     -> x
    |
    y
    ------------------------------------------------------
    |                          |                          |
    |                          |                          |
    |            0             |            1             |
    |                          |                          |
    |                          |                          |
   -------------------------------------------------------
    |                          |                          |
    |                          |                          |
    |            2             |            3             |
    |                          |                          |
    |                          |                          |
   -------------------------------------------------------

    '''

    def calcPartition(self, inserted_body):
        center = Point_2D(self.area.position.x + self.area.length/2, self.area.position.y + self.area.length/2)
        print(center.x, center.y)
        print(inserted_body.position.x > center.x)
        print(inserted_body.position.y > center.y)
        return int(inserted_body.position.x > center.x) + (int(inserted_body.position.y > center.y) << 1)

    def updatecenter_of_mass(self):
        total_mass = 0
        total_mass_times_position_x = 0
        total_mass_times_position_y = 0


        for child in self.children:
            if child.status != -1:
                total_mass += child.center_of_mass.mass
                total_mass_times_position_x += child.center_of_mass.position.x * child.center_of_mass.mass
                total_mass_times_position_y += child.center_of_mass.position.y * child.center_of_mass.mass

        res = Point_2D(total_mass_times_position_x / total_mass, total_mass_times_position_y / total_mass)

        return [res, total_mass]

    def insert(self, inserted_body):
        partition_idx = self.calcPartition(inserted_body)

        next_node = self.children[partition_idx]
        next_node.depth = self.depth + 1

        if next_node.status == -1:
            print("in -1")
            next_node.status = 0
            next_node.body = inserted_body
            next_node.center_of_mass.position = inserted_body.position
            next_node.center_of_mass.mass = inserted_body.mass


        elif next_node.status == 0:
            print("in 0")
            next_node.status = 1
            next_node.children = [Node(None) , Node(None), Node(None) , Node(None)]
            half = next_node.area.length / 2
            next_node.children[0].area = Area(Point_2D(next_node.area.position.x, next_node.area.position.y), half)
            next_node.children[1].area = Area(Point_2D(next_node.area.position.x + half, next_node.area.position.y), half)
            next_node.children[2].area = Area(Point_2D(next_node.area.position.x, next_node.area.position.y + half), half)
            next_node.children[3].area = Area(Point_2D(next_node.area.position.x + half, next_node.area.position.y + half), half)

            next_node.insert(next_node.body)
            next_node.insert(inserted_body)
            next_node.body = None

        else:
            print("in 1")
            next_node.insert(inserted_body)

        self.center_of_mass.position = self.updatecenter_of_mass()[0]
        self.center_of_mass.mass = self.updatecenter_of_mass()[1]

    def calc_gravity(self, base_body):
        if self.status == -1:
            return 0
        elif self.status == 0:
            return self.center_of_mass.calc_force(base_body)
        else:
            print("l/d : ", self.area.length / self.center_of_mass.position.calc_distance(base_body.position))
            if (self.area.length / self.center_of_mass.position.calc_distance(base_body.position)) < THETA:
                return self.center_of_mass.calc_force(base_body)
            else:
                gravitation = 0
                for child in self.children:
                    gravitation = gravitation + child.calc_gravity(base_body)
                    print(gravitation)
                return gravitation

    def update(self):
        pass
        #update all points according to runge-kutta

    def space_plot(self):

        if self.status == 1:
            for child in self.children:
                child.space_plot()

        plt.plot([self.area.position.x, self.area.position.x + self.area.length],
                      [self.area.position.y, self.area.position.y], color = "cyan")

        plt.plot([self.area.position.x, self.area.position.x],
                      [self.area.position.y, self.area.position.y + self.area.length], color = "cyan")

        plt.plot([self.area.position.x + self.area.length, self.area.position.x + self.area.length] ,
                      [self.area.position.y, self.area.position.y + self.area.length], color = "cyan")

        plt.plot([self.area.position.x, self.area.position.x  + self.area.length] ,
                      [self.area.position.y + self.area.length, self.area.position.y  + self.area.length], color = 'cyan')

        if self.status != -1:
            marker = str(self.depth % 4 + 1)
            plt.plot(self.center_of_mass.position.x, self.center_of_mass.position.y,
                marker = marker, color = 'yellow', label = str(self.area.length))



if __name__ == '__main__':
    bodies = []
    with open('input.dat', 'r') as fin:
        for line in fin:
            tmp = list(map(float, line.split()))
            body = Body(Point_2D(tmp[0], tmp[1]), tmp[2])
            bodies.append(body)

    root = Node(area = Area(Point_2D(X_MIN, Y_MIN) , X_MAX - X_MIN))
    root.status = 1
    root.depth = 0
    root.children = [Node(None) , Node(None), Node(None) , Node(None)]

    half = root.area.length / 2
    root.children[0].area = Area(Point_2D(root.area.position.x, root.area.position.y),  half)
    root.children[1].area = Area(Point_2D(root.area.position.x + half, root.area.position.y), half)
    root.children[2].area = Area(Point_2D(root.area.position.x, root.area.position.y + half), half)
    root.children[3].area = Area(Point_2D(root.area.position.x + half, root.area.position.y + half), half)

    for b in bodies:
        print("insert" + str(b))
        root.insert(b)

    fig = plt.figure()
    plt.grid()
    plt.xlim(X_MIN, X_MAX)
    plt.ylim(Y_MIN, Y_MAX)

    for b in bodies:
        plt.plot(b.position.x, b.position.y, marker = '*', color = 'blue', markersize = b.mass / 10**5)

    root.space_plot()

    res = root.calc_gravity(bodies[0])
    print("answer", res)



    plt.savefig('output.png')
