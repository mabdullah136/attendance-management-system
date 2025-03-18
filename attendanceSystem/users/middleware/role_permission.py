import jwt
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import re

class RolePermissionMiddleware(MiddlewareMixin):
    """
    Middleware to check user role permissions using JWT Bearer token.
    """

    def process_request(self, request):
        # Allow access to Django Admin Panel for all super admins
        if request.path.startswith("/admin/"):
            return None  

        # Skip authentication for public routes (modify as needed)
        if request.path in ["/users/login/", "/users/register/"]:
            return None

        # 🔹 Get Authorization Header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("bearer "):
            return JsonResponse({"error": "Unauthorized - No token provided"}, status=401)

        token = auth_header.split(" ")[1]  # Extract token from "Bearer <token>"

        try:
            # 🔹 Decode the token using Django's SECRET_KEY
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_role = decoded_token.get("role")  # Extract role from token
            
            if not user_role:
                return JsonResponse({"error": "Unauthorized - Invalid token"}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # 🔹 Super Admin can access everything
        if user_role == "Super Admin":
            return None

        # Define role-based access control (RBAC)
        role_permissions = {
            "Employee": ["/attendance/checkIn/", r"^/attendance/checkOut/\d+/$","/holiday/list/","/leaveRequest/"],
            "Manager": ["/attendance/checkIn/", r"^/attendance/checkOut/\d+/$","/holiday/list/","/leaveRequest/"],
            "HR": ["/attendance/checkIn/", r"^/attendance/checkOut/\d+/$","/holiday/list/","/leaveRequest/"],
        }

        # 🔹 Check if the role is allowed to access this path
        # allowed_paths = role_permissions.get(user_role, [])
        allowed_patterns = role_permissions.get(user_role, [])
        # if request.path not in allowed_paths:
        #     return JsonResponse({"error": "Forbidden: You don't have permission to access this resource"}, status=403)
        if not any(re.match(pattern, request.path) for pattern in allowed_patterns):
            return JsonResponse({"error": "Forbidden: You don't have permission to access this resource"}, status=403)

        return None
