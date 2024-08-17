from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import UserProfile, ClientRecipient
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from io import BytesIO

def home_view(req):
    return render(req,'home.html')

def monitor_view(request):
    if request.user.is_authenticated:
        return render(request, 'monitor.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            return redirect('home')
            
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')
    
    return render(request, 'login.html')




def get_watched_clients(request):
    if request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        watched_clients = user_profile.watched_clients.all()

        data = [{
            'client_email': client.client_email,
            'recipient_email': client.recipient_email
        } for client in watched_clients]

        return JsonResponse({'clients': data})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
@require_POST
def add_client_recipient(request):
    import json
    data = json.loads(request.body)
    client_email = data.get('client_email')
    recipient_email = data.get('recipient_email')
    region = data.get('region')
    try:
        client_recipient, created = ClientRecipient.objects.get_or_create(
            client_email=client_email,
            recipient_email=recipient_email,
            region = region 
        )

        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.watched_clients.add(client_recipient)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@login_required
@require_POST
def delete_client_recipient(request):
    import json
    data = json.loads(request.body)
    client_email = data.get('client_email')
    recipient_email = data.get('recipient_email')

    try:
        client_recipient = ClientRecipient.objects.get(
            client_email=client_email,
            recipient_email=recipient_email
        )
        client_recipient.delete()

        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.watched_clients.remove(client_recipient)

        return JsonResponse({'success': True})

    except ClientRecipient.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Client-recipient pair does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def export_excel(request):
    user = UserProfile.objects.get(user=request.user) 
    data = {'client_email': [], 'recipient_email': []}
    for client in user.watched_clients.all():
        data['client_email'].append(client.client_email)
        data['recipient_email'].append(client.recipient_email)
    
    df = pd.DataFrame(data)
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, 'Sheet1', index=False)
    
    output.seek(0)  # Rewind the buffer
    
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=email_maps.xlsx'
    
    return response
