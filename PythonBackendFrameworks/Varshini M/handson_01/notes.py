# Request lifecycle for GET /api/courses/ in Django:
# 1. Browser sends an HTTP GET request to /api/courses/.
# 2. Django's URL router matches the path to a view in urls.py.
# 3. The view handles the request, possibly calling a model to query the database.
# 4. The view returns an HttpResponse (or JSONResponse), which is sent back to the browser.

# Middleware sits between the request and the view/response pipeline.
# Example 1: SecurityMiddleware adds security headers and enforces HTTPS-related settings.
# Example 2: AuthenticationMiddleware associates a user with the request object.

# WSGI vs ASGI:
# WSGI is the synchronous request/response interface used by traditional web apps.
# ASGI is the asynchronous interface that supports long-lived connections, WebSockets, and async views.
# Django uses WSGI by default for standard deployments; switch to ASGI when you need async features.

# MVC vs Django MVT:
# MVC: Model = data layer, View = presentation layer, Controller = logic that handles input.
# Django MVT: Model = data layer, View = handles request logic (similar to MVC Controller), Template = presentation layer (similar to MVC View).
