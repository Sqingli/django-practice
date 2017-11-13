from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from asset.models import HostList ,User
from django.http import HttpResponseRedirect  
import hashlib
import requests ,json
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import authenticate, login
from django.contrib import auth 
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
# Create your views here.

def decerator(func):
    def wrapper(request,*args, **kwargs):
        is_login = request.session.get('logined',None)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login')
    return wrapper


def index(request):

    form =LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password =form.cleaned_data['password']
        return HttpResponse("right")
    #return render_to_response(request, 'index.html')
    #u1 = User.objects.get(username='root')
    #p=hashlib.sha256('admin'.encode()).hexdigest()
    return render (request, 'index.html', {'form': form})
	#return HttpResponse("wrong")

def login_check(request):
    next=request.POST.get('next')
    if request.method == 'POST':  
        username = request.POST.get('username')  
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                print('right')
                login(request, user)  
        #if username == 'song' and password == '123456':  
            # 当登陆成功后记录 session  
            #request.session['logined'] = 'yes'
    if next:
        return HttpResponseRedirect(next) 
    return HttpResponseRedirect('/asset/hostlist')   
    
@login_required
def hostlist(request):
    host_list =HostList.objects.all()
    context = {
        'host_list':host_list,
    }
    return render(request, 'hostlist.html', context)


@login_required
def add(request):
	ip=request.POST['ip']
	hostname=request.POST['hostname']
	status=request.POST['status']
	remark=request.POST['remark']
	HostList.objects.create(ip=ip, hostname=hostname, status=status, remark=remark)
	return HttpResponseRedirect('/asset/hostlist')
'''	
	ip=request.POST['ip']
    hostname=request.POST['hostname']
    status=request.POST['status']
    remark=request.POST['remark']
    HostList.objects.create(ip=ip,hoatname=hostname,status=status,remark=remark)
    return render(request,'hostlist.html')
'''

@login_required
def edit(request, id):
    host=HostList.objects.filter(pk=id)
    context = {
        'host':host,
    }
    return render (request, 'edit.html', context)

def editing(request,id):
    print(id)
    ip=request.POST['ip']
    hostname=request.POST['hostname']
    status=request.POST['status']
    remark=request.POST['remark']
    HostList.objects.filter(pk=id).update(ip=ip,hostname=hostname,status=status,remark=remark)
    return HttpResponseRedirect('/asset/hostlist')

def delete(request, id):
    host=HostList.objects.filter(pk=id)
    host.delete()
    return render (request, 'index.html')

@login_required
def adduser(request):
    return render(request, 'useradd.html')

def useradd(request):
    username=request.POST['username']
    password=request.POST['password']
    password_hash=hashlib.md5(password.encode()).hexdigest()
    print(password_hash)
    User.objects.create(username=username, password=password_hash)
    return HttpResponseRedirect('/asset/adduser')

def saltcmd(request):
    return render (request, 'saltcmd.html')

def saltrun(request):
    ip=request.POST.get('ip').strip()
    port=request.POST.get('port').strip()
    tgt=request.POST.get('tgt').strip()
    fun=request.POST.get('fun').strip()
    arg=request.POST.get('arg').strip()
    url='https://'+ip+":"+port
    token="73c33eb09b5694e0ff373d2b688718387b7aeff3"
    header= {'Accept': 'application/json', 'X-Auth-Token': token}

    if arg:
        body = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
    else:
        body = {'client': 'local', 'tgt': tgt, 'fun': fun }

    print(body)
    re=requests.post(url ,data=body, headers=header, verify=False)
    if arg:
        result=json.loads(re.text)['return'][0]['hadoop1'].strip('\n')
    else:
        result=json.loads(re.text)['return']
        
    body['ip']=ip
    return render (request, 'saltcmd.html', { 'result': result , 'body': body })
    
