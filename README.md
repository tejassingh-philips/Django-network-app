# Django-network-app

## Django Tailwind Integration

This guide will help you integrate Tailwind CSS into your Django project using the `django-tailwind` package.

## Step-by-Step Instructions

### 1. Install the `django-tailwind` Package

Install the package via pip:

```bash
python -m pip install django-tailwind
```

If you want to use automatic page reloads during development, use the `[reload]` extras, which also installs the `django-browser-reload` package:

```bash
python -m pip install 'django-tailwind[reload]'
```

Alternatively, you can install the latest development version:

```bash
python -m pip install git+https://github.com/timonweb/django-tailwind.git
```

### 2. Add `tailwind` to `INSTALLED_APPS`

In your `settings.py` file, add `tailwind` to the `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
  # other Django apps
  'tailwind',
]
```

### 3. Create a Tailwind CSS Compatible Django App

Create a new Django app called `theme` (or a name of your choice) for Tailwind CSS:

```bash
python manage.py tailwind init
```

### 4. Add the `theme` App to `INSTALLED_APPS`

Add your newly created `theme` app to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
  # other Django apps
  'tailwind',
  'theme',
]
```

### 5. Register the `theme` App

Add the following line to your `settings.py` file:

```python
TAILWIND_APP_NAME = 'theme'
```

### 6. Ensure `INTERNAL_IPS` is Set

Make sure that the `INTERNAL_IPS` list is present in the `settings.py` file and contains the `127.0.0.1` IP address:

```python
INTERNAL_IPS = [
    "127.0.0.1",
]
```

### 7. Install Tailwind CSS Dependencies

Run the following command to install the Tailwind CSS dependencies:

```bash
python manage.py tailwind install
```

### 8. Use the `base.html` Template

The `django-tailwind` package comes with a simple `base.html` template located at `your_tailwind_app_name/templates/base.html`. You can extend or delete it if you already have a layout.

### 9. Add `{% tailwind_css %}` to Your Template

If you are not using the `base.html` template that comes with Django Tailwind, add `{% tailwind_css %}` to the `base.html` template:

```html
{% load static tailwind_tags %}
...
<head>
   ...
   {% tailwind_css %}
   ...
</head>
```

The `{% tailwind_css %}` tag includes Tailwind’s stylesheet.

### 10. Configure `django_browser_reload` for Automatic Page Reloads

Add `django_browser_reload` to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
  # other Django apps
  'tailwind',
  'theme',
  'django_browser_reload',
]
```

### 11. Add the `BrowserReloadMiddleware`

In `settings.py`, add the middleware:

```python
MIDDLEWARE = [
  # ...
  "django_browser_reload.middleware.BrowserReloadMiddleware",
  # ...
]
```

**Note:** The middleware should be listed after any that encode the response, such as Django’s `GZipMiddleware`. The middleware automatically inserts the required script tag on HTML responses before `</body>` when `DEBUG` is `True`.

### 12. Include `django_browser_reload` URL

Include `django_browser_reload` URL in your root `urls.py`:

```python
from django.urls import include, path

urlpatterns = [
    ...,
    path("__reload__/", include("django_browser_reload.urls")),
]
```

### 13. Start the Development Server

You should now be able to use Tailwind CSS classes in your HTML. Start the development server by running:

```bash
python manage.py tailwind start
```



