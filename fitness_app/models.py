from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    user_id = models.AutoField(
        primary_key=True, db_column="user_id", db_index=True)
    user_name = models.CharField(unique=True, max_length=100)
    email = models.EmailField()
    age = models.IntegerField(
        validators=([MinValueValidator(0)], [MaxValueValidator(120)])
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Weight in kg and with max 2 decimal places",
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Height in meters and with max 2 decimal places",
    )
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default="M")
    ACTIVITY_CHOICES = [
        ("sedentary", "Sedentary (little or no exercise)"),
        ("lightly_active", "Lightly active (light exercise/sports 1-3 days/week"),
        (
            "moderately_active",
            "Moderately active (moderate exercise/sports 3-5 days/week)",
        ),
        ("very_active", "Very active (hard exercise/sports 6-7 days/week)"),
        (
            "super_active",
            "Super active (very hard exercise/sports & physical job or training twice a day)",
        ),
    ]
    activity = models.CharField(
        max_length=20, choices=ACTIVITY_CHOICES, default="sedentary"
    )
    GOAL_CHOICES = [
        ("weight_loss", "Lose Weight"),
        ("muscle_gain", "Gain Muscle"),
        ("improve_endurance", "Improve Endurance"),
        ("maintain_weight", "Maintain Weight"),
        ("flexibility", "Increase Flexibility"),
        ("overall_health", "Improve Overall Health"),
    ]
    goal = models.CharField(
        max_length=20, choices=GOAL_CHOICES, default="overall health"
    )

    def _str_(self):
        return self.user_name


class WorkoutRoutine(models.Model):
    routine_id = models.AutoField(primary_key=True, db_column="routine_id")
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    routine_name = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True, max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.routine_name


class WorkoutExercise(models.Model):
    workout_exercise_id = models.AutoField(
        primary_key=True, db_column="workout_exercise_id"
    )
    routine_id = models.ForeignKey("WorkoutRoutine", on_delete=models.CASCADE)
    exercise_id = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]


class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    exercise_name = models.TextField(max_length=100)
    description = models.TextField(blank=True, null=True)
    equipment_needed = models.TextField(blank=True, null=True)
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    DIFFICULTY_CHOICES = [
        (EASY, "Easy"),
        (MEDIUM, "Medium"),
        (HARD, "Hard"),
    ]
    STRENGTH = "Strength"
    CARDIO = "Cardio"
    FLEXIBILITY = "Flexibility"
    BALANCE = "Balance"
    EXERCISE_TYPE_CHOICES = [
        (STRENGTH, "Strength"),
        (CARDIO, "Cardio"),
        (FLEXIBILITY, "Flexibility"),
        (BALANCE, "Balance"),
    ]
    level_of_difficulty = models.CharField(
        max_length=6,
        choices=DIFFICULTY_CHOICES,
        default=MEDIUM,
    )
    type = models.CharField(
        max_length=10,
        choices=EXERCISE_TYPE_CHOICES,
        default=STRENGTH,
    )
    CHEST = "Chest"
    BACK = "Back"
    LEGS = "Legs"
    SHOULDERS = "Shoulders"
    ARMS = "Arms"
    ABS = "Abs"
    GLUTES = "Glutes"
    FULL_BODY = "Full Body"

    MUSCLE_GROUP_CHOICES = [
        (CHEST, "Chest"),
        (BACK, "Back"),
        (LEGS, "Legs"),
        (SHOULDERS, "Shoulders"),
        (ARMS, "Arms"),
        (ABS, "Abs"),
        (GLUTES, "Glutes"),
        (FULL_BODY, "Full Body"),
    ]
    muscle_group = models.CharField(
        max_length=10,
        choices=MUSCLE_GROUP_CHOICES,
        default=FULL_BODY,
    )

    def __str__(self):
        return self.exercise_name


class WorkoutSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    routine_id = models.ForeignKey(WorkoutRoutine, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    duration = models.IntegerField()


class WorkoutLog(models.Model):
    log_id = models.CharField(max_length=100, unique=True)
    session_id = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    exercise_id = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    reps = models.PositiveIntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    time = models.DurationField(blank=True, null=True)
    calories_burned = models.FloatField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
