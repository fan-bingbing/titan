import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

class SoundCard(object):
    def __init__(self):
        self.gain = 10
        self.duration = 0.1 # sample record duration
        self.sample_rate = 44100
        self.device = ('Microphone (Sound Blaster Play!, MME',
                       'Speakers (Sound Blaster Play! 3, MME')
        sd.query_devices(self.device[0])
        sd.default.device = self.device
        sd.default.channels = 1
        sd.default.samplerate = self.sample_rate

    def get_sample(self, average=5):
        x4 = np.full(3528, 0.0)
        for i in range(0, average):
            x1 = sd.rec(int(self.duration*self.sample_rate), dtype='float32', blocking=True) # record 0.1 seconds input signal from microphone

            x2 = self.gain*x1[int(self.duration*self.sample_rate/1000):int(self.duration*self.sample_rate)] # take effective samples

            x3 = x2[0:int(80*(self.sample_rate/1000))] # take first 80ms duration samples

            x4 = x3.flatten()# transfer 2D array to 1D, ready for fft operation, fft function can only take 1D array as input


        x4 = x4 / average
        # print(x4)


        t = 80*np.linspace(0, 1, np.size(x4))# generate 80ms time axis VS samples for first 80ms

        X = fft(x4) # fft transform
        n = np.size(t)
        self.fr = (self.sample_rate/2)*np.linspace(0, 1, int(n/2)) # generate frequecny axis array

        X_m = (2/n)*abs(X[0:np.size(self.fr)])

        # print(np.size(X_m))# M=2*np.size(X_m)=3528
        # print(X_m)

        return {'Time_level':x4, 'Time':t, 'Freq_level':X_m, 'Freq':self.fr}

    def get_SINAD(self, dict): # accept returned dictionary from get_sample()
        X_mmax = np.max(dict['Freq_level']) # find maximum value in numpy array
        # print(X_mmax)
        fr_index = np.where(dict['Freq_level'] == X_mmax) # locate index in numpy array
        fr_max = dict['Freq'][fr_index] # find corresponding frequency of maximum value

        # print(fr_max)
        # print(fr_index)
        # print(fr_max)

        SND = np.sum(dict['Freq_level'][24:240]) # from 300Hz to 3kHz get SND
        # print(SND)
        mask = self.mask_gen(x=fr_index[0], y=SND, z=self.fr)
        ND = np.sum(dict['Freq_level'][24:240] * mask[24:240]) # from 300Hz to 3kHz get ND
        # print(ND)
        # 1kHz at index 80
        #freq bin width = fs/M = 44100/3528 = 12.5Hz
        # 300/12.5 = 24 meaning 300Hz at index 24
        # 3000/12.5 = 240 meaning 3kHz at index 240
        SINAD = 20 * np.log10(SND/ND) # calculate SINAD
        return SINAD

    def mask_gen(self, x, y, z):
        mask = np.full(np.size(z), 1)
        mask[x]=0
        if y>=9.0:
            for i in range(1,30):
                mask[x-i]=0
                mask[x+i]=0
            print("filter bin set to 30")
        elif y>=8.0:
            for i in range(1,40):
                mask[x-i]=0
                mask[x+i]=0
            print("filter bin set to 40")
        elif y>=7.0:
            for i in range(1,55):
                mask[x-i]=0
                mask[x+i]=0
            print("filter bin set to 55")
        elif y>=6.0:
            for i in range(1,70):
                mask[x-i]=0
                mask[x+i]=0
                print("filter bin set to 70")
        elif y>=5.0:
            for i in range(1,85):
                mask[x-i]=0
                mask[x+i]=0
            print("filter bin set to 85")
        elif y>=4.0:
            for i in range(1,100):
                mask[x-i]=0
                mask[x+i]=0
            print("filter bin set to 100")
        elif y>=3.0:
            for i in range(1,110):
                mask[x-i]=0
                mask[x+i]=0
            print("filter bin set to 110")
        elif y>=2.0:
            for i in range(1,120):
                mask[x-i]=0
                mask[x+i]=0
            print("filter bin set to 120")
        else:
            for i in range(1,130):
                mask[x-i]=0
                mask[x+i]=0
            print("filter bin set to 130")

        return mask


    def live_plots(self):
        dict = self.get_sample()
        fig, (ax0, ax1) = plt.subplots(nrows=2)
        ax0.set_title('Sinusoidal Signal')
        ax0.set_xlabel('Time(ms)')
        ax0.set_ylabel('Amplitude')
        ax0.set_ylim(-2, 2)
        line0, = ax0.plot(dict['Time'], dict['Time_level']) # time VS level plot

        ax1.set_title('Magnitude Spectrum')
        ax1.set_xlabel('Frequency(Hz)')
        ax1.set_ylabel('Magnitude')
        ax1.set_ylim(0, 1.5)
        ax3 = ax1.text(0.3, 0.9, 'SINAD', transform=ax1.transAxes)
        line1, = ax1.plot(dict['Freq'], dict['Freq_level']) # frequency VS level plot

        fig.subplots_adjust(hspace=0.6)

        while True:
            dict = self.get_sample()
            line0.set_ydata(dict['Time_level']) # update data in plots only in loop instead of update entire plots
            line1.set_ydata(dict['Freq_level'])
            ax3.set_text('SINAD = %.2f dB' % self.get_SINAD(dict=dict)) # update SINAD value

            plt.pause(0.01)# this command will call plt.show()

try:
    SC = SoundCard()
except BaseException:
    print("Specified Soundcard does not exist.")
    pass

SC.live_plots()
