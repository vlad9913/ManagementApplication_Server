from functools import wraps

import jwt
from flask import request, Response, jsonify


def auth_required_with_role(roles):
    def auth_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                roles_numbers=[el.value for el in roles]
                payload = jwt.decode(request.headers.get('Authorization'), 'super-secret-key', algorithms=['HS256'])
                if int(payload['role']) not in roles_numbers:
                    return Response('Unauthorized', 401)
            except jwt.ExpiredSignatureError as e:
                return Response('Signature expired', 401)
            except jwt.InvalidTokenError as e:
                return Response('Invalid token.', 401)
            except Exception as e:
                return Response('Unauthorized', 401)

            return func(*args, **kwargs)

        return wrapper
    return auth_required