from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("start/",views.Stratingpage,name="index"),
    path("",views.Landingingpage,name="index"),
    path("register/",views.Registration,name="register"),
    path("addnew/",views.Add_details,name="addnew"),
    path('generate_otp/', views.generate_otp, name='generate_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path("choices/",views.Choices ,name="choices"),
    path("detail/",views.Availdetail,name="detail"),
    path("lyrics/",views.generate_lyrics,name="lyrics"),
    path("audio/",views.generate_audio,name="audio"),
    path("play/",views.Playsong,name="play"),
    path("create_again/",views.create_again,name="create_again"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
