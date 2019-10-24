import numpy as np


# Apply psophometric weighting to FFT, as per Recommendation ITU-T O.41 [2] Red Book 1994.
# This is sometimes called "CCITT weighting" because the above spec used to be the "CCITT Recommendation".
def apply_psophometric_weighting(fft_samples, sample_rate):
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



def SINAD(samples, sample_rate, test_tone_frequency = 1000,
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
        samples_fft_filt = apply_psophometric_weighting(samples_fft_filt, sample_rate)

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


if __name__ == '__main__':
    T_duration = 0.1 # seconds, duration of the simulation
    F_sample = 48e3 # Hz, sampling frequency

    # The test cases and expected results are copied from https://www.mathworks.com/help/signal/ref/sinad.html.

    # Test case 1: 1kHz sine wave + 2nd harmonic, expected SINAD = 20 * log10(1/0.025) = 32.04dB.
    time = np.arange(0, T_duration, 1.0/F_sample)
    test_signal = np.sin(2 * np.pi * 1e3 * time) + 0.025 * np.sin(2 * np.pi * 2e3 * time)
    print ('Test case 1 expected SINAD=32.04dB, estimated SINAD=', SINAD(test_signal, F_sample))

    # Test case 2: Sinusoidal signal with AWGN. Expecting 32.2dB.
    test_signal = np.sin(2 * np.pi * 1e3 * time) + 0.02 * np.sin(2 * np.pi * 2e3 * time) + 0.01 * np.random.normal(0, 1, len(time))
    print ('Test case 2 expected SINAD=32.2dB, estimated SINAD=', SINAD(test_signal, F_sample, freq_range_min = 10, freq_range_max = 24000))
