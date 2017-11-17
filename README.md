# arXiv Submission API

The arXiv submission API supports programmatic submission mechanisms for
third-party applications.

The API is based on the draft specification for
[SWORDv3](http://swordapp.org/swordv3/), implemented in
[JSON-LD](https://json-ld.org).

JSON Schema for the arXiv implementation of SWORDv3 can be found in
``schema/``.

## Toy submission service

The current ``Dockerfile`` in the root of this repository provides a toy
submission API, including access token verification.

To start the API, build and run the docker image:

```
docker build ./ -t arxiv/submit-api
docker run -it -p 8000:8000 arxiv/submit-api
```

This will start the submission API service proxied by NGINX. A toy
authorization service is also started to simulate access token verification
in a typical OAuth2 scenario.

If all goes well, the submission service should be available on
http://localhost:8000.

### Authorization

The toy authorization service simulates access token verification, e.g. after
an [OAuth2 authorization code grant](https://tools.ietf.org/html/rfc6749#section-4.1)
process. The NGINX gateway expects an ``Authorization`` header with the
access token. For example:

``Authorization: Bearer footoken1234``

If the token is valid, the authorizer replaces the access with a JWT that
encodes the identity of the client, the identity of the resource owner (end
user), and an authorization scope.

Token ``as392lks0kk32`` has scope ``submission:write`` and ``submission:read``,
which should grant access to the entire submission API.

Token ``f0da9jso3l2m4`` has scope ``submission:read``, which should allow only
``GET`` requests to relevant endpoints.

See ``submit/external.py`` for all of the available endpoints.

TODO: document endpoints here.

For example:

```
$ curl -I -H "Authorization: Bearer f0da9jso3l2m4" http://localhost:8000/astro-ph/12345
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Fri, 17 Nov 2017 20:21:49 GMT
Content-Type: application/json
Content-Length: 83
Connection: keep-alive
```

But:

```
$ curl -I http://localhost:8000/astro-ph/12345
HTTP/1.1 403 Forbidden
Server: nginx/1.10.3 (Ubuntu)
Date: Fri, 17 Nov 2017 20:21:20 GMT
Content-Type: application/json
Content-Length: 32
Connection: keep-alive
```
