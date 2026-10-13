import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rehabvision.settings")
django.setup()

from exercises.models import Exercise


video_links = {
    "Bodyweight Squat": "https://www.youtube.com/watch?v=X1NI4VFCuDI",
    "Reverse Lunge": "https://www.youtube.com/watch?v=MvVQO0Zasjs",
    "Glute Bridge": "https://www.youtube.com/watch?v=TXBtTmNpW00",
    "Calf Raise": "https://www.youtube.com/watch?v=-M4-G8p8fmc",
    "Wall Sit": "https://www.youtube.com/watch?v=cWTZ8Am1Ee0",
    "Push Up": "https://www.youtube.com/watch?v=gwPJw_p3h6g",
    
    "Dumbbell Shoulder Press": "https://www.youtube.com/watch?v=aI2hGzsAMXs",
    "Dumbbell Bicep Curl": "https://www.youtube.com/watch?v=w7hl4IbHMtY",
    "Dumbbell Row": "https://www.youtube.com/watch?v=ufhQhwyrx-4",
    "Plank": "https://www.youtube.com/watch?v=mwlp75MS6Rg",
    "Bird Dog": "https://www.youtube.com/watch?v=ZdAHe9_HeEw",
    "Dead Bug": "https://www.youtube.com/watch?v=g_BYB0R-4Ws",
    "Mountain Climber": "https://www.youtube.com/watch?v=hq_0YlyfqGM",
    "Jumping Jack": "https://www.youtube.com/watch?v=UpH7rm0cYbM",
    "High Knees": "https://www.youtube.com/watch?v=sTvekaq6vOU",
    "Glute Kickback": "https://www.youtube.com/watch?v=GQLi7oxp8tE",
    "Standing Hip Abduction": "https://www.youtube.com/watch?v=xUxWsvWj3Go",
    "Cat Cow": "https://www.youtube.com/watch?v=kqnua4rHVVA",
    "Arm Circles": "https://www.youtube.com/watch?v=PulZUNcnwuI",
    "Hamstring Stretch": "https://www.youtube.com/watch?v=9ESpoUPqpFw",
    "Quadriceps Stretch": "https://www.youtube.com/watch?v=XBLIiQS5RQI",
    "Child's Pose": "https://www.youtube.com/watch?v=8MGZRJjVDM4",
    "Standing Single Leg Balance": "https://www.youtube.com/watch?v=FJ5ToYR-OuA",
    "Wall Push Up": "https://www.youtube.com/watch?v=QpMTk21EmaM",
}


updated = 0

for exercise_name, video_url in video_links.items():

    count = Exercise.objects.filter(
        exercise_name=exercise_name
    ).update(
        demonstration_url=video_url
    )

    if count:
        print(f"✓ Updated: {exercise_name}")
        updated += count
    else:
        print(f"✗ NOT FOUND: {exercise_name}")


print()
print(f"Total exercises updated: {updated}")
print("Video links added successfully!")