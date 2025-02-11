from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest
from .forms import ServiceRequestForm, ServiceRequestUpdateForm

@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            return redirect('track_requests')
    else:
        form = ServiceRequestForm()
    return render(request, 'customer_service/submit_request.html', {'form': form})

@login_required
def track_requests(request):
    requests = ServiceRequest.objects.filter(customer=request.user)
    return render(request, 'customer_service/track_requests.html', {'requests': requests})

@login_required
def manage_requests(request):
    if not request.user.is_staff:
        return redirect('track_requests')
    requests = ServiceRequest.objects.all()
    return render(request, 'customer_service/manage_requests.html', {'requests': requests})

@login_required
def update_request(request, request_id):
    if not request.user.is_staff:
        return redirect('track_requests')
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    if request.method == 'POST':
        form = ServiceRequestUpdateForm(request.POST, instance=service_request)
        if form.is_valid():
            form.save()
            return redirect('manage_requests')
    else:
        form = ServiceRequestUpdateForm(instance=service_request)
    return render(request, 'customer_service/update_request.html', {'form': form})