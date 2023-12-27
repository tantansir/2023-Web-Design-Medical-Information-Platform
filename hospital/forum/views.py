from django import forms
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
import datetime
import math
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from forum.models import *
from forum import positon_to_distance


def homepage(request):
    return render(request, "home_page.html")


def loginpage(request):
    error_msg = None
    if request.method == "GET":
        return render(request, "login_page.html")
    else:
        username = request.POST.get("user")
        password = request.POST.get("pwd")

        filter_result = User.objects.filter(username__exact=username)
        if len(filter_result) == 0:
            error_msg = "用户名不存在。"
            return render(request, 'login_page.html', {'error_msg': error_msg})

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/../")
        else:
            error_msg = '密码错误，请重新输入！'

            return render(request, 'login_page.html', {'error_msg': error_msg})


def registerpage(request):
    error_msg = None
    user0 = request.GET.get('user0')
    if request.method == "GET":
        return render(request, "register_page.html",)
    else:

        username = request.POST.get("user")
        password = request.POST.get("pwd")

        if username.strip() and password:

            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                error_msg = "您的用户名已被注册过。"

            if password.isnumeric() or password.isalpha():
                error_msg = '密码需同时包含英文字符和数字字符。'

            if error_msg is None:
                user = User.objects.create_user(username=username, password=password)
                success_msg = "恭喜你，注册成功！"
                return render(request, "login_page.html", {'success_msg': success_msg})
            else:
                return render(request, "register_page.html", {'error_msg': error_msg})

        else:
            error_msg = "用户名密码不能为空。"
            return render(request, "register_page.html", {'error_msg': error_msg})


@login_required
def logout(request):
    auth.logout(request)
    return render(request, "home_page.html")


@login_required
def userpage(request):
    user = request.user
    profile = Profile.objects.filter(user_id__exact=user.id)

    return render(request, "user_page.html",
                  {
                      'profile': profile,
                  })


@login_required
def usermyblogpage(request):
    user = request.user
    blogs = Blog.objects.filter(user_id__exact=user.id).order_by('-modified_time')
    comments = Comment.objects.filter(user_id__exact=user.id).order_by('-created_time')
    return render(request, "user_myblog.html",
                  {
                      'blogs': blogs,
                      'comments': comments,
                  })


@login_required
def usermycollectionpage(request):
    user: User = request.user
    collection_blogs = Collection_Blog.objects.filter(user_id__exact=user.id).order_by('-blog__collect_amount')
    collection_hospitals = Collection_Hospital.objects.filter(user_id__exact=user.id)
    return render(request, "user_mycollection.html",
                  {
                      'collection_hospitals': collection_hospitals,
                      'collection_blogs': collection_blogs,
                  })


@login_required
def usermodifypage(request):
    if request.method == "GET":
        return render(request, "user_modify.html")
    else:
        user = request.user

        profile = Profile.objects.filter(user_id__exact=user.id)
        if profile:
            profile.delete()

        name = request.POST.get("Name")
        email = request.POST.get("Email")
        telephone = request.POST.get("Telephone")
        gender = request.POST.get("Sex")
        district = request.POST.get("District")
        address = request.POST.get("Address")
        info = request.POST.get("Information")

        new_profile = Profile(user=user, name=name, email=email, telephone=telephone, gender=gender, district=district, address=address, info=info)
        new_profile.save()

        if name or email or telephone or gender or district or address or info:
            return render(request, "user_page.html")

#信息公开页面
@login_required
def infopage(request):
    hospitals = Hospital.objects.all()
    search_query = request.GET.get('search_query')

    if not search_query:
        # 获取所有医院信息
        hospitals = Hospital.objects.all()
        # 将医院信息传递给模板
        context = {
            'hospitals': hospitals,
        }
    else:
        hospitals1 = hospitals.filter(district__iexact=search_query)
        if hospitals1:
            context = {'hospitals': hospitals1}
        else:
            hospitals = hospitals.filter(name__icontains=search_query)
            context = {'hospitals': hospitals}
    return render(request, 'info_page.html', context)

#医院详情
@login_required
def hospitalinfo(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    user: User = request.user

    if user.collection_hospital_set.filter(hospital_id__exact=hospital.id).count() == 0:
        is_collected = False
    else:
        is_collected = True

    if request.method == 'POST':
        collect_hospital = request.POST.get('collect_hospital')
        if not (collect_hospital is None):
            collection = Collection_Hospital.objects.filter(user_id__exact=user.id, hospital_id__exact=hospital.id)
            if len(collection) == 0:
                new_collection = Collection_Hospital(user=user, hospital=hospital)
                hospital.save()
                new_collection.save()
                is_collected = True
            else:
                collection.delete()
                is_collected = False
    return render(request, 'hospital_info.html', {'hospital': hospital, 'is_collected': is_collected})


# 创建/修改帖子的表单
class ModifyForm(forms.Form):
    title = forms.CharField(label='标题', max_length=200,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-user mb-5'}))
    content = forms.CharField(label='帖子内容',
                              widget=forms.Textarea(attrs={'class': 'form-control form-control-user mb-5'}))


# 帖子详情
@login_required
def blogindexpage(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comment_set.all().order_by('created_time')
    user: User = request.user

    if user.collection_blog_set.filter(blog_id__exact=blog.pk).count() == 0:
        is_collected = False
    else:
        is_collected = True

    if request.method == 'POST':
        create_comment = request.POST.get('create_comment')
        collect_blog = request.POST.get('collect_blog')

        if not (collect_blog is None):
            collection = Collection_Blog.objects.filter(user_id__exact=user.id, blog_id__exact=blog.id)
            if len(collection) == 0:
                new_collection = Collection_Blog(user=user, blog=blog)
                blog.collect_amount += 1
                blog.save()
                new_collection.save()
                is_collected = True
            else:
                collection.delete()
                is_collected = False

        if not (create_comment is None):
            new_comment = Comment(user=user, blog=blog, content=create_comment)
            new_comment.save()

    else:
        blog.pageview += 1
        blog.save()

    return render(request, 'blog_index.html',
                  {'blog': blog, 'comments': comments, 'user': user, 'is_collected': is_collected})


@login_required
def blogcreatepage(request):
    user = request.user

    if request.method == "POST":
        form = ModifyForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            blog = Blog(user=user, title=title, content=content)
            blog.save()
            return HttpResponseRedirect(reverse('forum:blog_page', args=(blog.id,)))
    else:
        form = ModifyForm()

    return render(request, 'blog_create.html', {'form': form})


@login_required
def blogmodifypage(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.user != request.user:
        return HttpResponseForbidden

    if request.method == "POST":
        form = ModifyForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            blog.title = title
            blog.content = content
            blog.save()
            return HttpResponseRedirect(reverse('forum:blog_page', args=(blog.id,)))
    else:
        form = ModifyForm(initial={'title': blog.title, 'content': blog.content})

    return render(request, 'blog_modify.html', {'form': form})


@login_required
def blogdelete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.user != request.user:
        return HttpResponseForbidden
    blog.delete()
    return HttpResponseRedirect(reverse("forum:my_blog"))


@login_required
def commentdelete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
        return HttpResponseForbidden
    comment.delete()
    return HttpResponseRedirect(reverse("forum:my_blog"))


@login_required
def bloghomepage(request, pg):
    search_query = request.GET.get('search_query')
    if not search_query:
        blogs = Blog.objects.filter(
            Q(user__blog__pageview__gte=10, modified_time__gte=timezone.now() - datetime.timedelta(days=10)) |
            Q(modified_time__gte=timezone.now() - datetime.timedelta(days=10))).distinct().order_by('-modified_time')
        page_num = math.ceil(len(blogs) / 5)

    else:
        blogs = Blog.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query),
            Q(user__blog__pageview__gte=10, modified_time__gte=timezone.now() - datetime.timedelta(days=10)) |
            Q(modified_time__gte=timezone.now() - datetime.timedelta(days=10))).distinct().order_by('-modified_time')
        page_num = math.ceil(len(blogs) / 5)
    if page_num == 0:
        page_num = 1

    if pg < 1:
        return render(request, 'blog_page.html',
                        {
                            'blogs': blogs,
                            'page_num': page_num,
                            'current_page': 1,
                        })

    if pg > page_num:
        return render(request, 'blog_page.html',
                        {
                            'blogs': blogs,
                            'page_num': page_num,
                            'current_page': page_num,
                        })

    if pg * 5 > len(blogs):
        number = len(blogs)
    else:
        number = pg * 5

    blogs = blogs[(pg - 1) * 5: number]
    return render(request, 'blog_page.html',
                    {
                        'blogs': blogs,
                        'page_num': page_num,
                        'current_page': pg,
                    })



@login_required
def recommendpage(request):

        user = request.user
        search_query = request.GET.get('search_query')
        button_text = request.GET.get('button_text')
        address = request.GET.get('address')
        illnesses = Illness.objects.values("name").distinct()
        hospitals = request.user
        distance_dict_sorted = {}

        if not address:
            if not search_query:
                is_result = False
            if search_query == 'A~E':
                illnesses = Illness.objects.values("name").distinct().filter(alphabet__in=["a", "b", "c", "d", "e"]).order_by('alphabet')
                is_result = False
            elif search_query == 'F~J':
                illnesses = Illness.objects.values("name").distinct().filter(alphabet__in=['f', 'g', 'h', 'i', 'j']).order_by('alphabet')
                is_result = False
            elif search_query == 'K~O':
                illnesses = Illness.objects.values("name").distinct().filter(alphabet__in=['k', 'l', 'm', 'n', 'o']).order_by('alphabet')
                is_result = False
            elif search_query == 'P~T':
                illnesses = Illness.objects.values("name").distinct().filter(alphabet__in=['p', 'q', 'r', 's', 't']).order_by('alphabet')
                is_result = False
            elif search_query == 'U~Z或其他':
                illnesses = Illness.objects.values("name").distinct().filter(alphabet__in=['u', 'v', 'w', 'x', 'y', 'z', '#']).order_by('alphabet')
                is_result = False
            elif search_query:
                illnesses = Illness.objects.values("name").distinct().filter(name__icontains=search_query)
                is_result = False
        else:
            #返回搜索结果
            is_result = True
            departments = list(Illness.objects.values_list("department", flat=True).filter(name__exact=button_text))
            hospitals = Hospital.objects.filter(Q(advantage_1__in=departments) | Q(advantage_2__in=departments) | Q(advantage_3__in=departments))
            hospital_list = []
            distance_dict = {}

            for hospital in hospitals:
                hospital_list.append(hospital.name)

            for hospital in hospitals:
                address1 = address
                lon_lat1 = positon_to_distance.stt(positon_to_distance.geocode(address1))
                address2 = hospital.address
                lon_lat2 = positon_to_distance.stt(positon_to_distance.geocode(address2))
                distance = positon_to_distance.geodesic(lon_lat1, lon_lat2)
                distance_dict[hospital] = distance

            distance_dict_sorted = dict(sorted(distance_dict.items(), key=lambda x: x[1], reverse=False))



        return render(request, "recommend_page.html",
        {
            'illnesses': illnesses,
            'is_result': is_result,
            'user': user,
            'hospitals': hospitals,
            'address': address,
            'distance_dict_sorted': distance_dict_sorted,
        })