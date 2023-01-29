from django.shortcuts import render, get_object_or_404, redirect
from .models import Courses, Topics, Order, Comment
from django.http import JsonResponse
import stripe
from django.views import View
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse,HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .forms import CommentForm
from django.urls import reverse_lazy, reverse, resolve
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView


stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'

# Create your views here.

def home(request):
    courses = Courses.objects.all()
    context = {"courses":courses}
    return render(request, 'app/index.html', context)

#success view
def success(request):
    session_id = request.GET.get('session_id')
    print(session_id)

    if session_id is None:
        return HttpResponseNotFound()

    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    session = stripe.checkout.Session.retrieve(session_id)

    order = get_object_or_404(Order, stripe_payment_intent=session_id)
    order.paid = True
    order.save()
    
    return render(request,'app/success.html')

class SuccessView(TemplateView):
    template_name="app/success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(Order, stripe_payment_intent=session.payment.intent)
        order.paid = True
        order.save()
        return render(request, self.template_name)

    
#cancel view
def cancel(request):
    return render(request,'app/cancel.html')

@login_required
def course(request, pk):
    course_id = pk
    c = Courses.objects.get(id=pk)
    lessons = Topics.objects.filter(course__id=course_id)
    
    try:
        order = Order.objects.get(course__id=course_id, paid=True, user = request.user)
    except Order.DoesNotExist:
        order = None

    context = {
        'course': get_object_or_404(Courses, id=pk),
        'lessons': lessons,
        'order': order,
        
    }
    return render(request, 'app/course.html', context)

def topic(request, id):
    topic_id = id
    t = Topics.objects.get(id=topic_id)
    comment = Comment.objects.filter(topic__id = topic_id)

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(topic=t, user=request.user, body=content)
            comment.save()
            return redirect(t.get_absolute_url())
    else:
        form = CommentForm()

    context={
        't':t,
        'comment': comment,
        'form': form
    }

    return render(request, 'app/topic.html', context)


def courses(request):

    courses = Courses.objects.all()
    order = Order.objects.filter(user=request.user)

    context = {"courses":courses, 'order':order}
    return render(request, 'app/courses.html', context)

class CourseCreate(CreateView):
    model = Courses
    fields = ["name", "desc", "price"]

    def get_success_url(self):
        return reverse_lazy('home')


class TopicCreate(CreateView):
    model = Topics
    fields = ["name", "course", "video", "description"]

    def get_success_url(self):
        return reverse_lazy('home')

class OrderCreate(CreateView):
    model = Order
    fields = ['user', 'course', 'email', 'paid', 'amount', 'description']


@csrf_exempt
@login_required
def create_checkout_session(request):

    path = request.META.get('HTTP_REFERER')
    id=path.split('/')[-2]
    course = Courses.objects.get(id=id)
    
    print(course.name)
    print(request.user)

    session = stripe.checkout.Session.create(
        client_reference_id=request.user.id if request.user.is_authenticated else None,
        payment_method_types=['card'],
        line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
            'name': course.name,
            },
            'unit_amount': int(course.price * 100),
        },
        'quantity': 1,
        }],

        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=YOUR_DOMAIN + '/cancel',
    )

    order=Order(course=course, user = request.user, stripe_payment_intent=session.id, email=request.user.email,paid=False, amount=0,description=" ")
    order.save()

    print(session)
    
    return JsonResponse({'id': session.id})

@csrf_exempt
def webhook(request):
    print("Webhook")
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        price = session["amount_total"] /100
        sessionID = session["id"]
        ID=session["metadata"]["order_id"]
        print(ID)
        
        Order.objects.filter(id=ID).update(email=customer_email, amount=price,paid=True,description=sessionID)

    return HttpResponse(status=200)

