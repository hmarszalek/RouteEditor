from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from routes.models import BackgroundImage, Route, RoutePoint


class ModelCreationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.background = BackgroundImage.objects.create(name="BG", image="backgrounds/bg.jpg")

    def test_create_route(self):
        route = Route.objects.create(name="My Route", user=self.user, background=self.background)
        self.assertEqual(route.name, "My Route")
        self.assertEqual(route.user, self.user)
        self.assertEqual(route.background, self.background)

    def test_create_route_point(self):
        route = Route.objects.create(name="Route A", user=self.user, background=self.background)
        point = RoutePoint.objects.create(name="Point A", x=100, y=200, route=route, user=self.user)
        self.assertEqual(point.route, route)
        self.assertEqual(point.user, self.user)
        self.assertEqual(point.x, 100)
        self.assertEqual(point.y, 200)


class ModelRelationsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.background = BackgroundImage.objects.create(name="BG", image="backgrounds/bg.jpg")
        self.route = Route.objects.create(name="Main Route", user=self.user, background=self.background)
        self.point = RoutePoint.objects.create(name="P1", x=50, y=60, route=self.route, user=self.user)

    def test_route_has_points(self):
        points = self.route.points.all()
        self.assertIn(self.point, points)

    def test_point_belongs_to_route_and_user(self):
        self.assertEqual(self.point.route, self.route)
        self.assertEqual(self.point.user, self.user)


class ValidationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.background = BackgroundImage.objects.create(name="BG", image="backgrounds/bg.jpg")
        self.route = Route.objects.create(user=self.user, name="Valid Route", background=self.background)

    def test_missing_route_name(self):
        route = Route(user=self.user, background=self.background)
        with self.assertRaises(ValidationError):
            route.full_clean()

    def test_negative_coordinates_should_fail(self):
        point = RoutePoint(user=self.user, route=self.route, name="Bad Point", x=-10, y=-20)
        with self.assertRaises(ValidationError):
            point.full_clean()

    def test_missing_point_name(self):
        point = RoutePoint(user=self.user, route=self.route, x=100, y=100)
        with self.assertRaises(ValidationError):
            point.full_clean()