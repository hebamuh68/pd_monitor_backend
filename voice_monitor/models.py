from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .voice_types import GenderChoices, min_pitch, max_pitch

# Trusted Data =================
class PdVoice(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    pitch = models.FloatField(validators=[MinValueValidator(min_pitch),MaxValueValidator(max_pitch)])
    jitter = models.FloatField()
    shimmer = models.FloatField()
    hnr = models.FloatField()
    gender = models.CharField(max_length=1, choices=GenderChoices)

    class Meta:
        db_table = 'pd_voice'

    def __str__(self):
        return self.id


class HcVoice(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    pitch = models.FloatField(validators=[MinValueValidator(min_pitch),MaxValueValidator(max_pitch)])
    jitter = models.FloatField()
    shimmer = models.FloatField()
    hnr = models.FloatField()
    gender = models.CharField(max_length=1, choices=GenderChoices)

    class Meta:
        db_table = 'hc_voice'

    def __str__(self):
        return self.id

# User Uploaded Data =================
class PdVoiceUploaded(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    pitch = models.FloatField(validators=[MinValueValidator(min_pitch),MaxValueValidator(max_pitch)])
    jitter = models.FloatField()
    shimmer = models.FloatField()
    hnr = models.FloatField()
    gender = models.CharField(max_length=1, choices=GenderChoices)

    class Meta:
        db_table = 'pd_voice_u'

    def __str__(self):
        return self.id


class HcVoiceUploaded(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    pitch = models.FloatField(validators=[MinValueValidator(min_pitch),MaxValueValidator(max_pitch)])
    jitter = models.FloatField()
    shimmer = models.FloatField()
    hnr = models.FloatField()
    gender = models.CharField(max_length=1, choices=GenderChoices)

    class Meta:
        db_table = 'hc_voice_u'

    def __str__(self):
        return self.id