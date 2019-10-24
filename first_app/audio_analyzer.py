import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft


class SoundCard(object):
    def __init__(self):
        self.gain = 1
        self.duration = 0.1 # sample record duration
        self.sample_rate = 44100
        self.device = ('Microphone (Sound Blaster Play!, MME',
                       'Speakers (Sound Blaster Play! 3, MME')
        sd.query_devices(self.device[0])
        sd.default.device = self.device
        sd.default.channels = 1
        sd.default.samplerate = self.sample_rate

    def get_sample(self):
        x1 = sd.rec(int(self.duration*self.sample_rate), dtype='float32', blocking=True) # record 0.1 seconds input signal from microphone

        x2 = self.gain*x1[int(self.duration*self.sample_rate/1000):int(self.duration*self.sample_rate)] # take effective samples

        x3 = x2[0:int(80*(self.sample_rate/1000))] # take first 80ms duration samples

        x4 = x3.flatten()# transfer 2D array to 1D, ready for fft operation, fft function can only take 1D array as input

        # x4 = np.zeros(3528)
        # for i in range(0, 5):
        #     x1 = sd.rec(int(self.duration*self.sample_rate), dtype='float32', blocking=True) # record 0.1 seconds input signal from microphone
        #
        #     x2 = self.gain*x1[int(self.duration*self.sample_rate/1000):int(self.duration*self.sample_rate)] # take effective samples
        #
        #     x3 = x2[0:int(80*(self.sample_rate/1000))] # take first 80ms duration samples
        #
        #     x4 += x3.flatten()# transfer 2D array to 1D, ready for fft operation, fft function can only take 1D array as input
        #
        # x4 = x4/5.0
        # print(len(x4))
        # print(self.SINAD(x4, self.sample_rate, psophometric_weighting = True))
        return self.SINAD(x4, self.sample_rate, psophometric_weighting = True)

        # t = 80*np.linspace(0, 1, np.size(x4))# generate 80ms time axis VS samples for first 80ms
    def apply_psophometric_weighting(self, fft_samples, sample_rate):
        ccitt_frequencies = (
            16.6, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200,
            1400, 1600, 1800, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000)
        ccitt_response = (
            -85.0, -63.0, -41.0, -21.0, -10.6, -6.3, -3.6, -2.0, -0.9, 0.0,
            0.6, 1.0, 0.0, -0.9, -1.7, -2.4, -3.0, -4.2, -5.6, -8.5, -15.0,
            -25.0, -36.0, -43.0)
        n_fft = len(fft_samples)
        masked_fft_samples = np.zeros_like(fft_samples)
        for i in range(n_fft):
            f_fft = i * float(sample_rate) / n_fft
            # Zero out the output outside of the CCITT range
            if f_fft < ccitt_frequencies[0] or f_fft > ccitt_frequencies[-1]:
                masked_fft_samples[i] = 1e-99
            # Interpolate in log-x axis domain when within the range
            else:
                for j in range(0, len(ccitt_frequencies) - 1):
                    if f_fft >= ccitt_frequencies[j] and f_fft <= ccitt_frequencies[j+1]:
                        x = np.log10(f_fft)
                        x0 = np.log10(ccitt_frequencies[j])
                        x1 = np.log10(ccitt_frequencies[j+1])
                        y0 = ccitt_response[j]
                        y1 = ccitt_response[j+1]
                        y_dB = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
                        masked_fft_samples[i] = fft_samples[i] * 10**(y_dB/20.0)
                        break
        return masked_fft_samples



    def SINAD(self, samples, sample_rate, test_tone_frequency = 1000,
        freq_range_min = 50, freq_range_max = 15000, psophometric_weighting = False):

        '''Return SINAD (signal to noise and distortion) in dB of real-valued sinusoidal signal.

        Arguments:
            samples... a numpy array of input audio samples. This needs at least a few k of samples to ensure the accuracy.
            sample_rate... sampling frequency in Hz
            test_tone_frequency... frequency of the tone (default: 1000)
            freq_range_min... high pass filter cutoff in Hz (default: 50, same as HP8920)
            freq_range_max... low pass filter cutoff in Hz (default: 15000, same as HP8920)
            psophometric_weighting... apply psophometric weighting if True (default: False)
        '''

        # Ensure input is an array of floats
        samples = np.array(samples, np.float)
        n_samples = len(samples)
        samples_w = samples * np.kaiser(n_samples, beta = 16.0)
        notch_width = 0.1 # notch width depends on the kaiser Beta coefficient

        # Zero pad to adjust the size to the next power of two
        n_fft = int(2**np.ceil(np.log2(n_samples)))
        samples_w = np.concatenate((samples_w, np.zeros(n_fft - n_samples)))

        # Go to frequency domain
        samples_fft = np.fft.rfft(samples_w)

        # Apply the band pass filter
        samples_fft_filt = samples_fft
        hpf_bin = int(n_fft * float(freq_range_min) / sample_rate)
        samples_fft_filt[:hpf_bin] = 1e-99
        lpf_bin = int(n_fft * float(freq_range_max) / sample_rate)
        samples_fft_filt[lpf_bin:] = 1e-99

        # Apply the psophometric weighting
        if psophometric_weighting:
            samples_fft_filt = self.apply_psophometric_weighting(samples_fft_filt, sample_rate)

        # Transform the filtered signal + noise back to time domain and measure the power
        samples_filt = np.fft.irfft(samples_fft_filt)
        signal_plus_noise_power = np.mean(np.absolute(samples_filt)**2)

        # Notch out the test tone
        notch_low_bin = int(n_fft * (1.0 - 0.5 * notch_width) * test_tone_frequency / sample_rate)
        notch_high_bin = int(n_fft * (1.0 + 0.5 * notch_width) * test_tone_frequency / sample_rate)
        samples_fft_filt[notch_low_bin : notch_high_bin] = 1e-99

        # Transform the left over noise (+ distortion) back to time domain and measure the power
        noise_filt = np.fft.irfft(samples_fft_filt)
        noise_power = np.mean(np.absolute(noise_filt)**2)

        # Return the SINAD in dB
        return 10 * np.log10(signal_plus_noise_power / noise_power)

try:
    SC = SoundCard()
except BaseException:
    print("Specified Soundcard does not exist.")
    pass

while True:
    SINAD = 0
    for i in range(0, 5):
        SINAD += SC.get_sample()
    print(SINAD / 5.0)
