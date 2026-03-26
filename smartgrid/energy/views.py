from django.contrib.auth.models import User
import matplotlib
matplotlib.use('Agg')  # Required for non-interactive background rendering
import matplotlib.pyplot as plt
import io, base64
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import EnergyRecord

@login_required
def dashboard(request):
    # Fetch user data
    records = EnergyRecord.objects.filter(user=request.user).order_by('timestamp')
    
    # Generate Chart
    chart = None
    if records.exists():
        times = [r.timestamp.strftime('%H:%M') for r in records]
        usage = [r.kwh_usage for r in records]

        plt.figure(figsize=(8, 4))
        plt.plot(times, usage, marker='o', linestyle='-', color='green')
        plt.title('Energy Usage Over Time')
        plt.xlabel('Time')
        plt.ylabel('kWh')
        
        # Save plot to a buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        # Encode to base64 string
        chart = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'energy/dashboard.html', {'chart': chart})

@login_required
def add_data(request):
    if request.method == "POST":
        usage = request.POST.get('usage')
        cost = request.POST.get('cost')
        EnergyRecord.objects.create(user=request.user, kwh_usage=usage, cost=cost)
        return redirect('dashboard')
    return render(request, 'energy/add_data.html')
