from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import parselmouth                    # Voice analysis library (Python wrapper for Praat)
from parselmouth.praat import call    # For jitter/shimmer calculations
import pandas as pd                   # Data manipulation
import numpy as np                    # Numerical operations


"""
Voice Feature Extraction for Parkinson's Disease Detection

What We Measure
Feature,	What It Measures,	Healthy vs PD
Pitch,	How high/low the voice sounds (Hz),	Varies by gender
Jitter,	Voice shakiness (pitch instability),	PD: Higher (more shaky)
Shimmer,	Volume variations (amplitude instability),	PD: Higher (more unstable)
HNR,	Voice clarity vs breathiness,	PD: Lower (more breathy)
"""
class VoiceMonitorViews():

    def __init__(self, parsed_voice):
        self.parsed_voice = parsed_voice

    def extract_pitch_mean(self):
        """
        Calculate the average pitch (fundamental frequency) of a voice recording.
        Parameters:
            voice: parselmouth.Sound object
        Returns:
            float: Mean pitch in Hz (e.g., 120.5 Hz)
        """

        # Analyze pitch over time
        pitch = self.parsed_voice.to_pitch()
        # Get all pitch measurements
        pitch_values = pitch.selected_array['frequency']
        # Remove silent frames (0 = no voice)
        voiced_pitch = pitch_values[pitch_values > 0]
        mean_pitch = np.mean(voiced_pitch)
        return mean_pitch

    def extract_jitter_local(self):
        """
        Calculate jitter (pitch instability) of a voice recording.
        Parameters:
            voice: parselmouth.Sound object
        Returns:
            float: Jitter as a ratio (e.g., 0.005 = 0.5%)
                Higher values = more voice instability
        """

        # Detect each vocal cord vibration (glottal pulse)
        # 75-500 Hz = range of human voice pitch
        point_process = call(self.parsed_voice, "To PointProcess (periodic, cc)", 75, 500)
        
        # Calculate jitter from the timing variations between pulses
        jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        
        return round(jitter, 5)

    def extract_shimmer_local(self):
        """
        Calculate shimmer (volume instability) of a voice recording.
        Parameters:
            voice: parselmouth.Sound object
        Returns:
            float: Shimmer as a ratio (e.g., 0.03 = 3%)
                Higher values = more volume instability
        """

        # Detect vocal cord vibrations
        point_process = call(self.parsed_voice, "To PointProcess (periodic, cc)", 75, 500)
        
        # Calculate shimmer - needs both the sound AND timing information
        # The extra parameter (1.6) filters out extreme amplitude outliers
        shimmer = call([self.parsed_voice, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        
        return round(shimmer, 5)

    def extract_HNR_mean(self):
        """
        Calculate HNR (voice clarity) of a voice recording.
        Parameters:
            voice: parselmouth.Sound object
        Returns:
            float: HNR in decibels (e.g., 22.5 dB)
                Higher values = clearer voice
                Lower values = breathier/hoarser voice
        """

        # Analyze harmonics vs noise
        harmonicity = self.parsed_voice.to_harmonicity() 
        # Remove unvoiced frames (-200 = no voice)
        hnr_values = harmonicity.values[harmonicity.values != -200]
        hnr_mean = np.mean(hnr_values)
        return round(hnr_mean, 2)

    def check_male_female(self):
        """
        Determine likely sex based on pitch and formants.
        Uses appropriate formant settings based on estimated sex.
        """

        mean_pitch = self.extract_pitch_mean()
        
        # Choose max_frequency based on pitch
        # Male voices typically < 165 Hz, Female > 165 Hz
        if mean_pitch < 165:
            estimated_sex = "male"
        else:
            estimated_sex = "female"
        
        return estimated_sex


"""
The APIs user interact with
"""
class VoiceMonitorAPI(APIView):

    
    def post(self, request, format=None):

        self.audio = request.data.get('audio')
        self.parsed_voice = parselmouth.Sound(self.audio)

        views_obj = VoiceMonitorViews(self.parsed_voice)

        pitch = views_obj.extract_pitch_mean()
        jitter = views_obj.extract_jitter_local()
        shimmer = views_obj.extract_shimmer_local()
        hnr = views_obj.extract_HNR_mean()
        gender = views_obj.check_male_female()

        data = {'pitch': pitch, 'jitter':jitter, 'shimmer':shimmer, 'hnr':hnr, 'gender':gender}

        return Response(data)
