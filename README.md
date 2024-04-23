# College-exam-django


Регистрация пользователей в Django включает в себя несколько ключевых шагов на стороне бэкенда и фронтенда. Вот примерный процесс создания системы регистрации:

1. Создание формы регистрации:

   - Сначала создадим форму, используя класс UserCreationForm, который Django предоставляет по умолчанию, или можно создать свой класс формы, расширяющий UserCreationForm, если необходимо добавить дополнительные поля.

2. Создание представления (view) для обработки регистрации:

   - Создадим представление, которое будет обрабатывать GET и POST запросы: отображать форму регистрации при GET-запросе и обрабатывать данные формы при POST-запросе.

3. Добавление маршрута URL:

   - Добавим маршрут URL в urls.py, чтобы пользователь мог перейти на страницу с формой регистрации.

4. Создание шаблона HTML для отображения формы регистрации:

   - Разработаем шаблон HTML, в котором будет использоваться наша форма регистрации.

Вот как можно реализовать эти шаги:

### Шаг 1: Создание формы регистрации

Создайте файл forms.py в вашем приложении и определите форму регистрации:

# forms.py
~~~
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
~~~


### Шаг 2: Создание представления

Создайте представление для регистрации в файле views.py:

# views.py
~~~
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
~~~


### Шаг 3: Добавление маршрута URL

Обновите файл urls.py вашего приложения, чтобы добавить новый маршрут:

# urls.py
~~~
from django.urls import path
from .views import register

urlpatterns = [
    # ... другие URL-адреса ...
    path('register/', register, name='register'),
]
~~~

### Шаг 4: Создание шаблона HTML

Создайте шаблон register.html в директории шаблонов вашего приложения:

~~~
<!-- register.html -->
{% extends 'base.html' %} <!-- Унаследуйте базовый шаблон, если таковой имеется -->

{% block content %}
<h2>Register</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Register</button>
</form>
{% endblock %}
~~~

 Применить миграции:
   Вам нужно убедиться, что все миграции были применены. Для этого выполните команду:

# sh
~~~
python manage.py migrate
~~~
   



Включите {% csrf_token %} в вашу форму для защиты от атак межсайтовой подделки запроса.

Теперь, когда вы посетите /register/ на вашем сайте Django, вы увидите форму регистрации. После успешного заполнения и отправки формы пользователь будет зарегистрирован и автоматически войдет в систему. Redirect('homepage') перенаправит пользователя на главную страницу (замените 'homepage' на нужное имя маршрута вашего проекта).

Это базовая регистрация. Вы можете настроить её, добавив дополнительные поля, валидацию, сообщения об ошибках и логику аутентификации, в зависимости от вашего проекта.
Любая регистрационная система должна обеспечивать безопасность данных пользователя и гладкий процесс взаимодействия. Используйте UserCreationForm в качестве отправной точки и настройте его под свои нужды, чтобы обеспечить, что ваша система соответствует требованиям и ожиданиям пользователей. Помните, что после того, как пользователь зарегистрирован, вам также может потребоваться предоставить функционал входа в систему (login) и выхода из системы (logout), чтобы завершить процесс управления учетными записями.




### Авторизация пользователя и создание профиля

Для создания системы авторизации на Django необходимо выполнить несколько шагов, используя встроенные средства Django для управления пользователями. Вот основные шаги для создания простой системы авторизации:

1. Использование встроенных моделей и форм
   Django предоставляет встроенную модель пользователя (User) и систему авторизации, а также формы для аутентификации, такие как AuthenticationForm.

2. Настройка URL
   Вам нужно настроить URL-адреса для входа, выхода и, если нужно, для регистрации пользователей. В urls.py вашего приложения добавьте следующие пути:
~~~
   from django.contrib.auth import views as auth_views
   from django.urls import path
   from . import views

   urlpatterns = [
       path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
       path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
       # Если вы хотите создать страницу регистрации:
       path('register/', views.register, name='register'),
   ]
~~~
   

3. Создание шаблонов
   Создайте шаблоны HTML для страниц входа, выхода и регистрации. Для входа вы можете создать шаблон login.html, который будет использовать AuthenticationForm.
   ~~~
      <!-- users/login.html -->
   <form method="post">
       {% csrf_token %}
       {{ form.as_p }}
       <button type="submit">Войти</button>
   </form>
   ~~~
   

   Аналогично, для регистрации создайте свою форму или используйте UserCreationForm.

5. Обработка представлений (views)
   Если вы создаёте собственную страницу регистрации, вам следует создать представление для обработки данных формы:
~~~
   from django.contrib.auth.forms import UserCreationForm
   from django.shortcuts import render, redirect

   def register(request):
       if request.method == 'POST':
           form = UserCreationForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect('login')
       else:
           form = UserCreationForm()
       return render(request, 'users/register.html', {'form': form})
~~~
   

5. Подключение системы аутентификации
   Убедитесь, что 'django.contrib.auth' включен в INSTALLED_APPS вашего файла settings.py. Также убедитесь, что у вас есть соответствующие настройки для управления сессиями пользователей:
~~~
      INSTALLED_APPS = [
       ...
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       ...
   ]

   MIDDLEWARE = [
       ...
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       ...
   ]
~~~
   

7. Настройка перенаправления
   В settings.py установите переменные для контроля перенаправления при входе и выходе:
~~~
   LOGIN_REDIRECT_URL = 'home'  # Перенаправление после входа
   LOGOUT_REDIRECT_URL = 'login'  # Перенаправление после выхода
~~~

   Здесь 'home' и 'login' — это имена URL-адресов, которые вы определяете в urls.py.

8. Миграции базы данных
   Проведите миграции, чтобы убедиться, что созданы все необходимые таблицы для аутентификации:
~~~
      python manage.py migrate
~~~
   

Это базовая настройка системы аутентификации. Вы можете расширять и настраивать её, создавая собственные формы, модели и представления, в зависимости от требований вашего проекта.


Отправка пользователем записи 
Понял тебя, короче говоря, тебе нужна система модерации постов. Чтобы пользователь мог создавать посты, которые затем поступают на утверждение администратору. Вот базовые шаги, которые тебе предстоит сделать в Django:

1. Настрой модель Post в models.py, добавь туда булево поле, например is_approved, с дефолтным значением False. Это поле будет указывать на то, одобрен пост или нет.
~~~
   from django.db import models
   from django.contrib.auth.models import User

    class Post(models.Model):
        title = models.CharField(max_length=200)
        content = models.TextField()
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        is_approved = models.BooleanField(default=False)
        # Другие поля, например дата создания
        created_at = models.DateTimeField(auto_now_add=True)
~~~
    

2. В admin.py зарегистрируй модель Post с кастомным ModelAdmin, в котором укажи, что отображать в админ-панели.
~~~
   from django.contrib import admin
   from .models import Post

    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_display = ('title', 'author', 'is_approved', 'created_at')
        list_filter = ('is_approved', 'created_at')
        search_fields = ('title', 'content')
~~~

3. Настрой views, чтобы пользователи могли через форму на сайте создавать посты. Не забудь проверить, что пользователь авторизован.
~~~
   from django.shortcuts import render, redirect
   from .forms import PostForm
   from .models import Post
   from django.contrib.auth.decorators import login_required

    @login_required
    def create_post(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('view_where_to_go_after_save')
        else:
            form = PostForm()
        return render(request, 'create_post.html', {'form': form})
~~~
    

4. В формах у тебя появится форма создания поста PostForm, которую ты напишешь в forms.py.
~~~
   from django import forms
   from .models import Post

    class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ['title', 'content']
   ~~~ 

5. Также тебе потребуется в шаблоне create_post.html отобразить форму для создания поста.
~~~
   <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Отправить на модерацию</button>
    </form>
~~~
    

6. Настрой URL, чтобы пользователи могли переходить на страницу создания поста.
~~~   
    from django.urls import path
    from . import views

    urlpatterns = [
        path('create/', views.create_post, name='create_post'),
        # Остальные пути.
    ]
~~~    

Теперь, когда пользователь создает пост, он сохраняется с is_approved = False. Администратор в админ-панели может видеть все посты и изменять их статус на одобренный. Только одобренные посты стоит отображать на сайте.
