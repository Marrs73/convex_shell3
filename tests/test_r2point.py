from pytest import approx
from math import sqrt
from r2point import R2Point

# python -B -m pytest -p no:cacheprovider


class TestR2Point:

    # Расстояние от точки до самой себя равно нулю
    def test_dist1(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(1.0, 1.0)) == approx(0.0)

    # Расстояние между двумя различными точками положительно
    def test_dist2(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(1.0, 0.0)) == approx(1.0)

    def test_dist3(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(0.0, 0.0)) == approx(sqrt(2.0))

    # Площадь треугольника равна нулю, если все вершины совпадают
    def test_area1(self):
        a = R2Point(1.0, 1.0)
        assert R2Point.area(a, a, a) == approx(0.0)

    # Площадь треугольника равна нулю, если все вершины лежат на одной прямой
    def test_area2(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 1.0), R2Point(2.0, 2.0)
        assert R2Point.area(a, b, c) == approx(0.0)

    # Площадь треугольника положительна при обходе вершин против часовой
    # стрелки
    def test_area3(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
        assert R2Point.area(a, b, c) > 0.0

    # Площадь треугольника отрицательна при обходе вершин по часовой стрелке
    def test_area4(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
        assert R2Point.area(a, c, b) < 0.0

    # Точки могут лежать внутри и вне "стандартного" прямоугольника с
    # противопложными вершинами (0,0) и (2,1)
    def test_is_inside1(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 0.5).is_inside(a, b) is True

    def test_is_inside2(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 0.5).is_inside(b, a) is True

    def test_is_inside3(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 1.5).is_inside(a, b) is False

    # Ребро [(0,0), (1,0)] может быть освещено или нет из определённой точки
    def test_is_light1(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, 0.0).is_light(a, b) is False

    def test_is_light2(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(2.0, 0.0).is_light(a, b) is True

    def test_is_light3(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, 0.5).is_light(a, b) is False

    def test_is_light4(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, -0.5).is_light(a, b) is True

    ######################################
    # Тесты нового метода positive_area():
    ######################################

    # Треугольник вырождается в точку
    def test_point_case(self):
        a, b, c = R2Point(1, 1), R2Point(1, 1), R2Point(1, 1)
        assert R2Point.positive_area(a, b, c) == 0

    def test_point_case(self):
        a, b, c = R2Point(0, 0), R2Point(0, 0), R2Point(0, 0)
        assert R2Point.positive_area(a, b, c) == 0

    # Треугольник вырождается в прямую
    def test_line_case(self):
        a, b, c = R2Point(0, 0), R2Point(5, 5), R2Point(3, 3)
        assert R2Point.positive_area(a, b, c) == 0

    # Треугольник полностью в первом квадранте
    def test_full_area(self):
        a, b, c = R2Point(3, 5), R2Point(5, 3), R2Point(8, 8)
        assert R2Point.positive_area(a, b, c) == approx(R2Point.area(a, b, c))

    # Треугольник полносью вне первого квадранта
    def test_null_area(self):
        a, b, c = R2Point(0, 0), R2Point(-4, -4), R2Point(-4, 0)
        assert R2Point.positive_area(a, b, c) == approx(0)

    # Треугольник имеет 2 пересечения и 0 точек в первом квадранте
    def test_null_area(self):
        a, b, c = R2Point(-2, 4), R2Point(4, -2), R2Point(-2, -2)
        assert R2Point.positive_area(a, b, c) == approx(2)

    # Треугольник имеет 2 пересечения и 1 точку в первом квадранте,
    # не включая начало координат
    def test_null_area(self):
        a, b, c = R2Point(-4, 6), R2Point(-2, 2), R2Point(4, 4)
        assert R2Point.positive_area(a, b, c) == approx(4.7)

    # Треугольник имеет 2 пересечения и 1 точку в первом квадранте,
    # включая начало координат
    def test_null_area(self):
        a, b, c = R2Point(-4, 2), R2Point(-2, -4), R2Point(4, 4)
        assert R2Point.positive_area(a, b, c) == approx(8)

    # Треугольник имеет 2 пересечения и 2 точки в первом квадранте
    # на оси Oy
    def test_null_area(self):
        a, b, c = R2Point(-4, 6), R2Point(4, 8), R2Point(4, 2)
        assert R2Point.positive_area(a, b, c) == approx(18.1)

    # Треугольник имеет 2 пересечения и 2 точки в первом квадранте
    # на оси Ox
    def test_null_area(self):
        a, b, c = R2Point(1, 1), R2Point(2, -3), R2Point(5, 3)
        assert R2Point.positive_area(a, b, c) == approx(5.6)

    # Треугольник имеет 2 пересечения и 2 точки в первом квадранте
    # на разных осях
    def test_null_area(self):
        a, b, c = R2Point(-2, -2), R2Point(3, 5), R2Point(6, 3)
        assert R2Point.positive_area(a, b, c) == approx(13.5)

    # Треугольник имеет 4 пересечния и 1 точку в первом квадранте
    def test_null_area(self):
        a, b, c = R2Point(-4, -4), R2Point(6, 3), R2Point(6, -2)
        assert R2Point.positive_area(a, b, c) == approx(17.7)

    # Треугольник имеет 4 пересечения и 0 точек в первом квадранте
    def test_null_area(self):
        a, b, c = R2Point(-4, 2), R2Point(-1, 5), R2Point(8, -2)
        assert R2Point.positive_area(a, b, c) == approx(10.79365)
