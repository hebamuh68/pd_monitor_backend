# this files contains fixed values of voice features


from django.db import models
from django.utils.translation import gettext_lazy as _


# Feature 1: Pitch (Fundamental Frequency) =================
# Min pitch: 75 Hz, Lowest expected human voice (deep male)
# Max pitch: 500 Hz, Highest expected voice (female/child)
min_pitch= 75
max_pitch= 500


# Feature 2: Jitter (Pitch Instability) =================
# Feature 3: Shimmer (Volume Instability) =================
# Feature 4: HNR (Harmonics-to-Noise Ratio) =================
# Feature 5: Gender =================
class GenderChoices(models.TextChoices):
    FEMALE = 'F', _("Female")
    MALE = 'M', _("Male")
    UNSURE = 'U', _("Unsure")