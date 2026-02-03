import json
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth import login,authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

# Create your views here.




@csrf_exempt
def register_view(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        info = json.loads(request.body)

        username = info.get('username', '').strip().lower()
        email = info.get('email', '').strip().lower()
        password = info.get('password')

        # تحقق من الحقول
        if not username or not email or not password:
            return JsonResponse({"error": "All fields are required"}, status=400)

        # تحقق من username
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        # تحقق من email
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        # إنشاء المستخدم
        user=User.objects.create_user(username=username, email=email, password=password)
        login(request,user)
        return JsonResponse({"message": "Registration successful"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
