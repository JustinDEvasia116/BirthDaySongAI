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
from django.views.decorators.cache import never_cache, cache_control


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

@never_cache
@cache_control(no_cache=True, max_age=0, must_revalidate=True, no_store=True)
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
@never_cache
def Choices(request):
    user = request.user
    try:
        profile = Profiles.objects.filter(user=user).latest("id")
    except Profiles.DoesNotExist:
        return redirect('addnew')
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

openai.api_key = settings.GPT3_SECRET_API
@login_required(login_url='register')
@never_cache
def Availdetail(request):
    user = request.user
    try:
        profile = Profiles.objects.filter(user=user).latest("id")
    except Profiles.DoesNotExist:
        # Profile does not exist for this user, so redirect to "addnew"
        return redirect('addnew')  # Replace 'addnew' with the actual URL name for your "addnew" view
    
    if request.method == "POST":
        if profile.generated_lyrics is None:
            # If generated_lyrics is None, fetch values from request.POST
            petname = request.POST.get("petname")
            angry = request.POST.get("angry")
            funny = request.POST.get("funny")
            movie = request.POST.get("movie")
            sport = request.POST.get("sport")
            smile = request.POST.get("smile")
            
            # Update the profile object with the new values
            profile.petname = petname
            profile.angry = angry
            profile.funny = funny
            profile.movie = movie
            profile.sport = sport
            profile.smile = smile
            
            # Save the updated profile
            profile.save()
        else:
            # Use values from the profile object
            petname = profile.petname
            angry = profile.angry
            funny = profile.funny
            movie = profile.movie
            sport = profile.sport
            smile = profile.smile

        # Assuming you have access to the user making the request
        user = request.user  # Replace with how you get the user making the request

        # Fetch user-specific profile data
        try:
            profile = Profiles.objects.filter(user=user).latest("id")
            full_name = profile.full_name
            print(full_name)
            age = profile.age
            gender = profile.gender
            mood = profile.mood
            genre = profile.genre
        except Profiles.DoesNotExist:
            # Handle the case where the user's profile does not exist
            return redirect(request, "addnew")
        
        gender_pronouns = {
             "Male": ("He", "him", "His"),
             "Female": ("She", "her", "Her"),
    }
        subject_pronoun, object_pronoun, possessive_pronoun = gender_pronouns[gender]

        # Dynamically create the input script with the requirement for at least two "Happy birthday" lines
        input_script = f"""

Generate one Happy Birthday song without verse for {full_name} who is turning {age}.
Include the following details:
- we call {object_pronoun} {petname}.
- {angry} makes {object_pronoun} angry.
- {funny} makes {object_pronoun} funniest.
- {smile} makes {object_pronoun} special.
- {movie} movie {subject_pronoun} likes the most.
- {sport} sports {subject_pronoun} likes the most.
- do not categorize the song into verse and chorus.

The song should have at least two instances of "Happy birthday" and should rhyme.
Lyrics should be simple, short, and easy to sing.

Using the above information about {full_name}, please create a heartfelt Happy Birthday song.
Each line can have a maximum of 8 words or 40 characters.


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
        # Return the generated lyrics as a JSON response
        return JsonResponse({'success': True})
    else:
        return render(request, "frame4.html")

@login_required(login_url='register')
@never_cache
def generate_lyrics(request):
    user = request.user
    try:
        profile = Profiles.objects.filter(user=user).latest("id")
        
    except Profiles.DoesNotExist:
        return redirect('addnew')
    if request.method == "GET":
        # Assuming you have access to the user making the request
        user = request.user  # Replace with how you get the user making the request

        # Fetch user-specific profile data
        try:
            profile = Profiles.objects.filter(user=user).latest("id")
            generated_lyrics = profile.generated_lyrics

            # Render the HTML page with the retrieved lyrics
            return render(request, "frame5.html", {'generated_lyrics': generated_lyrics})
        except Profiles.DoesNotExist:
            # Handle the case where the user's profile does not exist
            return redirect("addnew")  # Redirect to the "addnew" page or the appropriate URL

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def generate_audio(request):
    user = request.user
    try:
        profile = Profiles.objects.filter(user=user).latest("id")
        generated_lyrics = profile.generated_lyrics
        full_name = profile.full_name
    except Profiles.DoesNotExist:
        return redirect('addnew')

    directory_path = os.path.join(settings.MEDIA_ROOT, 'assets', 'audiofiles')
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    # Convert the lyrics to audio using gTTS and specify the content type as MP3
    tts = gTTS(text=generated_lyrics, lang='en', lang_check=False, slow=False)

    # Generate the audio file name using the user's full name
    audio_file_name = f"{full_name.replace(' ', '_')}.mp3"
    audio_file_path = os.path.join(directory_path, audio_file_name)
    tts.save(audio_file_path)

    # Save the audio file to the audio_file field in the Profiles model
    with open(audio_file_path, 'rb') as audio_file:
        profile.audio_file.save(audio_file_name, File(audio_file))
    os.remove(audio_file_path)
    return redirect('play')

@never_cache
def Playsong(request):
    user = request.user
    try:
        profile = Profiles.objects.filter(user=user).latest("id")
        audio_file_url = profile.audio_file.url
    except Profiles.DoesNotExist:
        return redirect('addnew')

    return render(request, 'frame6.html', {'audio_file_url': audio_file_url})

def generate_otp(request):
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        username = name.replace(" ", "")
        
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
                user = auth.authenticate(request, username=username, password="")
                if user is not None and user.is_active and not user.is_superuser:
                    auth.login(request, user)
                    print("login successfull")
                    
                # OTPs match, return a success response
                return JsonResponse({'success': True})
            else:
                # OTPs do not match, return an error response
                return JsonResponse({'success': False, 'message': 'Invalid OTP'})
        else:
            # If no account with the provided phone number is found, return an error response
            return JsonResponse({'success': False, 'message': 'Account not found'})
@never_cache
def create_again(request):
    user = request.user
    try:
        profile = Profiles.objects.filter(user=user).latest("id")
    except Profiles.DoesNotExist:
        return render(request,"frame2.html")
    if request.user.is_authenticated:
        # Delete profiles associated with the authenticated user
        
        Profiles.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})