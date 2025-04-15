# API Extension

## Installing Django REST framework

```bash
pip install djangorestframework
```

## Add `rest_framework` to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # ...existing apps...
    'rest_framework',
    'rest_framework.authtoken',
]
```

## Create serializers for the `Route` and `RoutePoint` models

Create a file called `routes/serializers.py`.

## Add API views in `routes/views.py`

Implement `RouteViewSet` and `RoutePointViewSet` in your `views.py`.

## Add API routes

Update the `routes/urls.py` file to include API routes:

```python
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import RouteViewSet, RoutePointViewSet

router = DefaultRouter()
router.register(r'routes', RouteViewSet, basename='routes')

routes_router = NestedDefaultRouter(router, r'routes', lookup='route')
routes_router.register(r'points', RoutePointViewSet, basename='route-points')

urlpatterns = [
    # ...existing paths...
    path('api/', include(router.urls)),
    path('api/', include(routes_router.urls)),
    path('api/token-auth/', obtain_auth_token),
]
```

## Sample Endpoints

After applying the changes, the API will support the following endpoints:

-   `GET /api/routes/{route_id}/points/`: Retrieve a list of points for the given route.
-   `POST /api/routes/{route_id}/points/`: Add a new point to the given route.
-   `GET /api/routes/{route_id}/points/{point_id}/`: Retrieve details of a specific point.
-   `DELETE /api/routes/{route_id}/points/{point_id}/`: Delete a specific point.

# Tests

Run all test:

```bash
python3 manage.py test routes.tests
```

Run individual tests:

```bash
python3 manage.py test routes.tests.test_models
python3 manage.py test routes.tests.test_views
python3 manage.py test routes.tests.test_api
```
