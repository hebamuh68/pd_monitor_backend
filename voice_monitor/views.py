from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class VoiceMonitor():

    def extract_pitch_mean(voice):
        """
        Calculate the average pitch (fundamental frequency) of a voice recording.
        
        Parameters:
            voice: parselmouth.Sound object
        
        Returns:
            float: Mean pitch in Hz (e.g., 120.5 Hz)
        """
        pitch = voice.to_pitch()                           # Analyze pitch over time
        pitch_values = pitch.selected_array['frequency']   # Get all pitch measurements
        voiced_pitch = pitch_values[pitch_values > 0]      # Remove silent frames (0 = no voice)
        mean_pitch = np.mean(voiced_pitch)                 # Calculate average
        return round(mean_pitch, 2)


    def extract_jitter_local(voice):
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
        point_process = call(voice, "To PointProcess (periodic, cc)", 75, 500)
        
        # Calculate jitter from the timing variations between pulses
        jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        
        return round(jitter, 5)

    def extract_shimmer_local(voice):
        """
        Calculate shimmer (volume instability) of a voice recording.
        
        Parameters:
            voice: parselmouth.Sound object
        
        Returns:
            float: Shimmer as a ratio (e.g., 0.03 = 3%)
                Higher values = more volume instability
        """
        # Detect vocal cord vibrations
        point_process = call(voice, "To PointProcess (periodic, cc)", 75, 500)
        
        # Calculate shimmer - needs both the sound AND timing information
        # The extra parameter (1.6) filters out extreme amplitude outliers
        shimmer = call([voice, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        
        return round(shimmer, 5)

    def extract_HNR_mean(voice):
        """
        Calculate HNR (voice clarity) of a voice recording.
        
        Parameters:
            voice: parselmouth.Sound object
        
        Returns:
            float: HNR in decibels (e.g., 22.5 dB)
                Higher values = clearer voice
                Lower values = breathier/hoarser voice
        """
        harmonicity = voice.to_harmonicity()                        # Analyze harmonics vs noise
        hnr_values = harmonicity.values[harmonicity.values != -200] # Remove unvoiced frames (-200 = no voice)
        hnr_mean = np.mean(hnr_values)                              # Calculate average
        return round(hnr_mean, 2)

    def check_male_female(voice):
        """
        Determine likely sex based on pitch and formants.
        Uses appropriate formant settings based on estimated sex.
        """
        # Step 1: Get pitch to estimate sex
        pitch = voice.to_pitch()
        pitch_values = pitch.selected_array['frequency']
        voiced_pitch = pitch_values[pitch_values > 0]
        mean_pitch = np.mean(voiced_pitch)
        
        # Step 2: Choose max_frequency based on pitch
        # Male voices typically < 165 Hz, Female > 165 Hz
        if mean_pitch < 165:
            estimated_sex = "male"
        else:
            estimated_sex = "female"
        
        return estimated_sex