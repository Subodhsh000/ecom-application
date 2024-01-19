import random, razorpay
from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import product,cart,order
from django.db.models import Q

# Create your views here.



def contact(request):
    return HttpResponse("<h1> May Contact Page Hu. </h1>")

def edit(request,rid):
    print("id to be edited:",rid)
    return HttpResponse("ID to be edited:"+ rid)

def delete(request,rid):
    print("id to be deleted:",rid)
    return HttpResponse("ID to be deleted:"+ rid)

class simpleview(View):
    def get(self,request):
        return HttpResponse("Hello From simple view")
    

def hello(request):
    context={}
    context['greet']="Good Morning"
    context['x']=10
    context['y']=20
    context['l']=[1,2,3,4,5]
    context['product']=[

        {'Id':1, 'Name':'Harry', 'Category':'Phone', 'Price': 20000},
        {'Id':2, 'Name':'Mac', 'Category':'Laptop', 'Price': 100000},
        {'Id':3, 'Name':'Subodh', 'Category':'TV', 'Price': 50000}


    ]
    return render(request,'hello.html',context)

def home(request):
    context={}
    p=product.objects.filter(is_active=True)
    context['product']=p
    # print(p)
    return render(request,'index.html',context)

def pdetails(request,pid):
    p=product.objects.filter(id=pid)
    context={}
    context['product']=p
    return render(request,'product_detail.html',context)

def register(request):
    if request.method=="POST":
       
            uname=request.POST['uname']
            upass=request.POST['upass']
            ucpass=request.POST['ucpass']
            if uname=="" or upass=="" or ucpass=="":
                context={}
                context['errmsg']="field can not be empty"
                return render(request,'register.html',context)
            
            elif upass!=ucpass:
                context={}
                context['errmsg']="password did not match"
                return render(request,'register.html',context)

            else:
                try:
                    u=User.objects.create(username=uname,password=upass,email=uname)
                    u.set_password(upass)
                    u.save()
                    context={}
                    context['success']="User Crerated successfully"
                    # return HttpResponse("data is fetch successfully") 
                    return render(request,'register.html',context)
                
                except Exception:
                    context={}
                    context['errmsg']="username already exists"
                    return render(request,'register.html',context)
    
    else:
        return render(request,'register.html')

def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="":
            context={}
            context['errmsg']="field can not be emplty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            # print(u)
           
            if u is not None:
                login(request,u)
                return redirect('/home')
        #    return HttpResponse("in else part")
            else:
                context={}
                context['errmsg']="Invalid Username and password"
                return render(request,'login.html',context)
       
        # print(uname)
    #    print(upass)
        return HttpResponse("Data is fetched")

    else:
        return render(request,'login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/home')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    context={}
    context['product']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv == '0':
        col = 'price' #asc
    else:
        col = '-price' #dec

    p=product.objects.order_by(col)
    context={}
    context['product']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1 & q2 & q3)
    context={}
    context['product']=p
    return render(request,'index.html',context)


def addtocart(request,pid):
    userid=request.user.id
    u=User.objects.filter(id=userid)
    print(u[0])
    p=product.objects.filter(id=pid)
    print(p[0])
    q1 = Q(uid=u[0])
    q2 = Q(pid=p[0])
    c=cart.objects.filter(q1 and q2)
    n=len(c)
    print(n)
    context={}
    context['product']=p
    
    if n == 1:
        context['msg']="Product already exist in cart"
    else:
        c=cart.objects.create(uid=u[0],pid=p[0])
        c.save()
        context['success']="Product Added Successfully"
    #print(pid)
    #print(userid)
    #return HttpResponse("Id is fetched")
    return render(request, 'product_detail.html', context)

def viewcart(request):
    if request.user.is_authenticated:
        c = cart.objects.filter(uid = request.user.id)
        # print(c)
        # print(c[0].uid)
        # print(c[0].pid.name)
        # print(c[1].pid.name)
        # print(c[0].uid.is_superuser)
        # print(len(c))
        np = len(c)
        s = 0
        for x in c:
            # print(x)
            # print(x.pid.price)
            s = s + (x.pid.price * x.qty)
        print(s)
        context = {}
        context['product'] = c
        context['totalprice'] = s
        context['totalitem'] = np
        return render(request, 'cart.html', context)
    else:
        return redirect('/login')

def remove(request, cid):
    c = cart.objects.filter(id = cid)
    c.delete()
    return redirect('/viewcart')


def updateqty(request, qv, cid):
    c = cart.objects.filter(id = cid)
    # print(c[0].pid)
    # print(c[0].qty)
    
    if qv == "1":
      newqty  = c[0].qty + 1
      c.update(qty = newqty)
    else:
        if c[0].qty > 1:
            newqty = c[0].qty - 1
            c.update(qty = newqty)
    return redirect('/viewcart')


def placeorder(request):
    userid = request.user.id
    #print(userid)
    c=cart.objects.filter(uid=userid)
    #print(c)
    oid = random.randrange(1000,9999)
    #print(oid)
    
    for x in c:
        print(x)
        print(x.pid)
        print(x.qty)
        o = order.objects.create(order_id=oid, pid=x.pid, uid=x.uid, qty=x.qty)
        o.save()#shit data into order
        #delete data from order
        
    orders=order.objects.filter(uid=userid)
    np=len(orders)
    s=0
    for x in c:
        # print(x)
        # print(x.pid.price)
        s = s + (x.pid.price * x.qty)
        print(s)
        context = {}
        context['product'] = c
        context['totalprice'] = s
        context['totalitem'] = np
    return render(request, 'placeorder.html', context)
    #return HttpResponse("in place order")

def makepayment(request):
    orders = order.objects.filter(uid=request.user.id)
    s = 0
    for x in orders:
        # print(x)
        # print(x.pid.price)
        s = s + (x.pid.price * x.qty)
        oid=x.order_id
    
    client = razorpay.Client(auth=("rzp_test_SeVEkCXVVp7iaO", "tFTmJVVACiD422lWMiKzZe2t"))
    
    DATA = {
    "amount": s*10,
    "currency": "INR",
    "receipt": oid,
    "notes": {
        "key1": "value3",
        "key2": "value2"
        }
    }
    payment = client.order.create(data=DATA)
    print(payment)
    uname=request.user.username
    print(uname)
    context={}
    context['orders']=payment
    context['uname']=uname
    client.order.create(data=DATA)
    return render(request, 'pay.html', context)
    #return HttpResponse("in payment section")



