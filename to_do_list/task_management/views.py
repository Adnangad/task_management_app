from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.cache import cache
from uuid import uuid4

# Create your views here.
def index(request):
    return HttpResponse('Hello World')

@csrf_exempt
def createUser(request):
    """endoint that creates a user and adds them to the db"""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        userwithmail = Users.objects.filter(email=email)
        userwithname = Users.objects.filter(username=username)
        if userwithname:
            return JsonResponse({'error': 'A user with the username already exists'}, status=409)
        if userwithmail:
            return JsonResponse({'error': f'A user with the email {email} already exists'}, status=409)
        try:
            user = Users.objects.create(username=username, email=email, password=make_password(password))
            user.save()
            token = uuid4()
            cache.set(f'auth_{token}', email, 86400)
            return JsonResponse({'message': 'Success', 'token': token}, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status=409)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def login(request):
    """Authenticates a users credentials"""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        try:
            user = Users.objects.filter(username=username).first()
            if not user:
                return JsonResponse({'error': 'No user with such credentials exists'}, status=409)
            if check_password(password, user.password):
                token = uuid4()
                cache.set(f'auth_{token}', user.email, 86400)
                return JsonResponse({'message': 'Successfully Logged in', 'token': token}, status=200, safe=False)
            else:
                return JsonResponse({'error': 'Invalid Password'}, status=401)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status=409)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def create_task(request):
    """Creates a task"""
    if request.method == 'POST':
        token = request.headers['X-Token']
        email = cache.get(f'auth_{token}')
        if email:
            data = json.loads(request.body.decode('utf-8'))
            task = data.get('task')
            try:
                user = Users.objects.filter(email=email).first()
                tasks = [model_to_dict(obj) for obj in Tasks.objects.all().filter(user=user)]
                names = []
                for el in tasks:
                    names.append(el['task'])
                if task in names:
                    return JsonResponse({'error': 'Task already exists',}, status=409, safe=False)               
                to_do = Tasks.objects.create(task=task, user=user, status=False)
                return JsonResponse({'message': 'Success',}, status=200, safe=False)
            except Exception as e:
                return JsonResponse({'error': f'{e}'}, status=409)
        else:
            return JsonResponse({'error': 'Session expired, please log in to continue'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_tasks(request):
    """Retreives tasks associated with the user"""
    if request.method == 'GET':
        token = request.headers['X-Token']
        email = cache.get(f'auth_{token}')
        if email:
            try:
                user = Users.objects.filter(email=email).first()
                tasks = [model_to_dict(obj) for obj in Tasks.objects.all().filter(user=user)]
                return JsonResponse({'tasks': tasks,}, status=200, safe=False)
            except Exception as e:
                return JsonResponse({'error': f'{e}'}, status=409)
        else:
            return JsonResponse({'error': 'Session expired, please log in to continue'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def update_tasks(request):
    """Updates a users task"""
    if request.method == 'PUT':
        token = request.headers['X-Token']
        email = cache.get(f'auth_{token}')
        if email:
            data = json.loads(request.body.decode('utf-8'))
            task_id = data.get('task_id')
            try:
                user = Users.objects.filter(email=email).first()
                task = Tasks.objects.get(user=user, id=task_id)
                if task.status == True:
                    task.status = False
                    task.save()
                else:
                    task.status = True
                    task.save()
                return JsonResponse({'message': 'Success',}, status=200, safe=False)
            except Exception as e:
                print(f'Error is {e}')
                return JsonResponse({'error': f'{e}'}, status=409)
        else:
            return JsonResponse({'error': 'Session expired, please log in to continue'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_task(request):
    """Deletes a users task"""
    if request.method == 'DELETE':
        token = request.headers['X-Token']
        email = cache.get(f'auth_{token}')
        if email:
            data = json.loads(request.body.decode('utf-8'))
            task_id = data.get('task_id')
            try:
                user = Users.objects.filter(email=email).first()
                task = Tasks.objects.get(user=user, id=task_id)
                task.delete()
                return JsonResponse({'message': 'Success',}, status=200, safe=False)
            except Exception as e:
                print(f'Error is {e}')
                return JsonResponse({'error': f'{e}'}, status=409)
        else:
            return JsonResponse({'error': 'Session expired, please log in to continue'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def updateAccount(request):
    """Updates a users account"""
    if request.method == 'PUT':
        token = request.headers['X-Token']
        mail = cache.get(f'auth_{token}')
        if mail:
            try:
                data = json.loads(request.body.decode('utf-8'))
                username = data.get('username')
                user = Users.objects.get(email=mail)
                if len(username) > 1:
                    user.username = username
                    user.save()
                return JsonResponse({'message': 'Success'}, status=200)
            except Exception as e:
                print(f'Error is {e}')
                return JsonResponse({'error': f'{e}'}, status=409)
        return JsonResponse({'error': 'Session expired, please log in to continue'}, status=401)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def getUser(request):
    """Gets user details"""
    if request.method == 'GET':
        token = request.headers['X-Token']
        email = cache.get(f'auth_{token}')
        if email:
            try:
                user = Users.objects.filter(email=email).first()
                user = model_to_dict(user)
                return JsonResponse({'user': user}, status=200, safe=False)
            except Exception as e:
                return JsonResponse({'error': f'{e}'}, status=409)
        else:
            return JsonResponse({'error': 'Session expired, please log in to continue'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)