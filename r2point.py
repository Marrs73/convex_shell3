from math import sqrt


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Площадь треугольника в первом квадранте
    @staticmethod
    def positive_area(new, first, last):
        zero_point = R2Point(0, 0)
        if not R2Point.is_triangle(new, first, last):
            return 0

        # находим точки пересечения с осями у трёх прямых,
        # находящиеся при этом внутри сторон треугольника.
        if (new.x == first.x):
            y1 = -1
        else:
            y1 = (first.x)/(first.x - new.x)*(new.y - first.y) + first.y
            if not R2Point(0, y1).is_inside(new, first):
                y1 = -1
        if (new.x == last.x):
            y2 = -1
        else:
            y2 = (last.x)/(last.x - new.x)*(new.y - last.y) + last.y
            if not R2Point(0, y2).is_inside(new, last):
                y2 = -1
        if (first.x == last.x):
            y3 = -1
        else:
            y3 = (last.x)/(last.x - first.x)*(first.y - last.y) + last.y
            if not R2Point(0, y3).is_inside(last, first):
                y3 = -1
        if (new.y == first.y):
            x1 = -1
        else:
            x1 = (first.y)/(first.y - new.y)*(new.x - first.x) + first.x
            if not R2Point(x1, 0).is_inside(new, first):
                x1 = -1
        if (new.y == last.y):
            x2 = -1
        else:
            x2 = (last.y)/(last.y - new.y)*(new.x - last.x) + last.x
            if not R2Point(x2, 0).is_inside(new, last):
                x2 = -1
        if (first.y == last.y):
            x3 = -1
        else:
            x3 = (last.y)/(last.y - first.y)*(first.x - last.x) + last.x
            if not R2Point(x3, 0).is_inside(last, first):
                x3 = -1

        # селекция точек треугольника, находящихся в первом квадранте
        pos_points = [R2Point(point.x, point.y) for point in [new, first, last]
                      if point.x >= 0 and point.y >= 0]
        pos_points_length = len(pos_points)

        # селекция пересечений, лежащих на положительных частях осей.
        pos_crosses = [R2Point(cross.x, cross.y) for cross in [R2Point(x1, 0),
                       R2Point(0, y1), R2Point(x2, 0), R2Point(0, y2),
                       R2Point(x3, 0), R2Point(0, y3)]
                       if cross.x >= 0 and cross.y >= 0]
        pos_crosses_length = len(pos_crosses)

        if pos_points_length == 3:
            return R2Point.area(new, first, last)

        if pos_points_length == 0 and pos_crosses_length == 0:
            return 0

        if pos_crosses_length == 2:
            if pos_points_length == 0:
                return R2Point.area(pos_crosses[0], pos_crosses[1], zero_point)

            elif pos_points_length == 1:
                return R2Point.area(pos_crosses[0], pos_crosses[1],
                                    pos_points[0])\
                    + R2Point.area(pos_crosses[0], pos_crosses[1], zero_point)

            else:  # pos_points_length == 2
                if pos_crosses[0].x == 0 and pos_crosses[1].x == 0:
                    cross1 = R2Point(0, max(pos_crosses[0].y,
                                            pos_crosses[1].y))
                    cross2 = R2Point(0, min(pos_crosses[0].y,
                                            pos_crosses[1].y))
                    point1 = pos_points[0]
                    point2 = pos_points[1]
                    if point1.y < point2.y:
                        point1, point2 = point2, point1

                    return R2Point.area(cross1, point1, point2) +\
                        R2Point.area(cross1, cross2, point2)

                elif pos_crosses[0].y == 0 and pos_crosses[1].y == 0:
                    cross1 = R2Point(min(pos_crosses[0].x,
                                         pos_crosses[1].x), 0)
                    cross2 = R2Point(max(pos_crosses[0].x,
                                         pos_crosses[1].x), 0)
                    point1 = pos_points[0]
                    point2 = pos_points[1]
                    if point1.x > point2.x:
                        point1, point2 = point2, point1

                    return R2Point.area(cross1, point1, point2) +\
                        R2Point.area(cross1, cross2, point2)

                else:
                    cross1 = R2Point(0, max(pos_crosses[0].y,
                                            pos_crosses[1].y))
                    cross2 = R2Point(max(pos_crosses[0].x,
                                         pos_crosses[1].x), 0)

                    if (pos_points[0].y > pos_points[0].x):
                        point1 = pos_points[0]
                        point2 = pos_points[1]
                    elif (pos_points[1].y < pos_points[1].x):
                        point1 = pos_points[0]
                        point2 = pos_points[1]

                    return R2Point.area(cross1, point1, point3)\
                        + R2Point.area(cross1, cross2, point2)\
                        + R2Point.area(cross1, cross2, zero_point)

        elif pos_crosses_length == 4:
            max_y = 0
            for i in pos_crosses:
                if i.y > max_y:
                    max_y = i.y
            point1 = R2Point(0, max_y)

            second_max_y = 0
            for i in pos_crosses:
                if i.y > second_max_y and i.y < max_y:
                    second_max_y = i.y
            point2 = R2Point(0, second_max_y)

            max_x = 0
            for i in pos_crosses:
                if i.x > max_x:
                    max_x = i.x
            point4 = R2Point(max_x, 0)

            second_max_x = 0
            for i in pos_crosses:
                if i.x > second_max_x and i.x < max_x:
                    second_max_x = i.x
            point3 = R2Point(second_max_x, 0)

            if pos_points_length == 1:
                return R2Point.area(point1, point2, pos_points[0])\
                    + R2Point.area(point2, point3, pos_points[0])\
                    + R2Point.area(point3, point4, pos_points[0])

            elif pos_points_length == 0:
                return R2Point.area(point1, point2, point4)\
                    + R2Point.area(point2, point3, point4)

        return "None of the cases came up"

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False


if __name__ == "__main__":
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
