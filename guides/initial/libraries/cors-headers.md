# cors headers

## installation

```bash
pip install django-cors-headers
```

## and then add it to your installed apps

```bash
INSTALLED_APPS = [
    ...,
    "corsheaders",
    ...,
]
```

## You will also need to add a middleware class to listen in on responses

```bash
MIDDLEWARE = [
    ...,
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...,
]
```
