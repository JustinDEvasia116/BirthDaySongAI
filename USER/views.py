from django.shortcuts import render,redirect
import random
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
import openai
from gtts import gTTS
import os
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings


from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from USER.models import *
from django.contrib import messages

# Create your views here.
def Stratingpage(request):
    return render(request,'start.html')

def Landingingpage(request):
    return render(request,'index.html')

def Registration(request):
    return render(request,'frame1.html')

@login_required(login_url='register')
def Add_details(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        
        # Validate the form data (e.g., check for required fields)
        if not name or not age or not gender:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'frame2.html')
        else:
            # Create a new Profiles instance and save it to the database
            try:
                profile = Profiles(user=user, full_name=name, age=age, gender=gender)
                profile.save()
                print("profile created")
            except Exception as e:
                messages.error(request, 'An error occurred while saving the profile.')
            return redirect('choices')
    else:    
        return render(request, 'frame2.html')

@login_required(login_url='register')
def Choices(request):
    if request.method == 'POST':
        selected_mood = request.POST.get('mood')
        selected_genre = request.POST.get('genre')

        # Assuming you have a user object, you can access it like this:
        user = request.user

        # Save the selected mood and genre to the Profiles model
        profile = Profiles.objects.filter(user=user).latest('id')
        profile.mood = selected_mood
        profile.genre = selected_genre
        profile.save()

        # Return a success response
        return JsonResponse({'success': True})
    # Handle other cases (e.g., GET requests) if needed
    return render(request, 'frame3.html')


def Availdetail(request):
    user = request.user
    try:
        profile = Profiles.objects.filter(user=user).latest("id")
    except Profiles.DoesNotExist:
        return redirect('addnew')  
    
    if request.method == "POST":
        profile.petname = request.POST.get("petname")
        profile.angry = request.POST.get("angry")
        profile.funny = request.POST.get("funny")
        profile.movie = request.POST.get("movie")
        profile.sport = request.POST.get("sport")
        profile.smile = request.POST.get("smile")
        profile.save()
        return JsonResponse({'success': True})
    return render(request,'frame4.html')
 
openai.api_key = settings.GPT3_SECRET_API
def generate_lyrics(request):
    user = request.user
    try:
        profile = Profiles.objects.filter(user=user).latest("id")
    except Profiles.DoesNotExist:
        # Handle the case where the user's profile does not exist
        return redirect("addnew") 
    
    if request.method == "GET":
        full_name = profile.full_name
        age = profile.age
        gender = profile.gender
        mood = profile.mood
        genre = profile.genre
        petname = profile.petname
        angry = profile.angry
        funny = profile.funny
        movie = profile.movie
        sport = profile.sport
        smile = profile.smile   
        
        # Dynamically create the input script with the requirement for at least two "Happy birthday" lines
        input_script = f"""
        Wish a happy birthday  to {full_name}.


        """

        # Generate lyrics using the input script
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_script,
            max_tokens=200,  # Adjust as needed
            n=1,  # Number of completions
            stop=None,
            temperature=0.7,  # Adjust for creativity
            )

            # Extract the generated lyrics from the response
        gpt_response = response.choices[0].text.strip()
        generated_lyrics =(str(gpt_response))
        print("gpt worked")
        print(generated_lyrics)
        profile.generated_lyrics = generated_lyrics
        profile.save()
        return render(request, "frame5.html", {'generated_lyrics': generated_lyrics})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def generate_audio(request):
    user = request.user
    try:
        profile = Profiles.objects.filter(user=user).latest("id")
        generated_lyrics = profile.generated_lyrics
        full_name = profile.full_name
    except Profiles.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User profile not found'})

    # Convert the lyrics to audio using gTTS and specify the content type as MP3
    tts = gTTS(text=generated_lyrics, lang='en', lang_check=False, slow=False)

    # Generate the audio file name using the user's full name
    audio_file_name = f"{full_name.replace(' ', '_')}.mp3"
    audio_file_path = os.path.join("media", "assets", "audiofiles", audio_file_name)
    tts.save(audio_file_path)

    # Save the audio file to the audio_file field in the Profiles model
    with open(audio_file_path, 'rb') as audio_file:
        profile.audio_file.save(audio_file_name, File(audio_file))
    
    return redirect('play')


def Playsong(request):
    user = request.user
    try:
        profile = Profiles.objects.filter(user=user).latest("id")
        audio_file_url = profile.audio_file.url
    except Profiles.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User profile not found'})

    return render(request, 'frame6.html', {'audio_file_url': audio_file_url})

def generate_otp(request):
        username = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        
        # Generate a 4-digit OTP (you can customize the length as needed)
        otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        
        existing_account = Accounts.objects.filter(phone=phone).first()
        
        if request.method == 'POST':
            if existing_account:
            # An account with the same phone number already exists
            # Update the OTP field with a newly generated OTP                
                existing_account.otp = otp
                existing_account.save()
                print("OTP updated for existing account")
            else:        
                user = User.objects.create_user(username=username,email=email,password="")
                user.save_base
                user_id = User.objects.get(username=username)
                account = Accounts.objects.create(user=user_id,phone=phone,otp=otp)
                account.save()
                print("user created")   

            # Here, you can send the OTP to the user via email, SMS, or any other method

        # Return a JSON response indicating success and the generated OTP
        return JsonResponse({'success': True, 'otp': otp})

def verify_otp(request):
    if request.method == 'POST':
        # Get the received OTP from the request
        received_otp = request.POST.get('otpValue')
        
        # Get the phone number from the request
        phone = request.POST.get('phone')
        print(received_otp,phone)
        
        # Fetch the corresponding account from the database based on the phone number
        account = Accounts.objects.filter(phone=phone).first()
        validate_user = account.user
        username = validate_user.username
        
        if account:
            # If an account with the provided phone number exists, fetch the OTP from the account
            generated_otp = account.otp

            if received_otp == generated_otp:
                # user = auth.authenticate(request, username=username, password="")
                # if user is not None and user.is_active and not user.is_superuser:
                #     auth.login(request, user)
                #     print("login successfull")
                    
                # OTPs match, return a success response
                return JsonResponse({'success': True})
            else:
                # OTPs do not match, return an error response
                return JsonResponse({'success': False, 'message': 'Invalid OTP'})
        else:
            # If no account with the provided phone number is found, return an error response
            return JsonResponse({'success': False, 'message': 'Account not found'})