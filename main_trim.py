"""
31 Dec 2015, Keunwoo Choi

Trim the audio file that contains basic chords with differnt form using many instrument + drum track.

"""
import sys
import os
import numpy as np
import librosa

from constants import *

class template_info:
	def __init__(self):
		#components
		self.harmonic_ins = ['Sine', 'Piano', 'Acoustic_guitar', 'Electric_guiar', 'Saxophone', 'Strings']
		self.percussive_ins=['drums']
		self.instruments = [self.harmonic_ins, self.percussive_ins]
		
		self.harmonic_chords=['intevals', 'M_m', 'sus4_M7', '7_m', 'dim_blank']
		self.harmonic_keys = ['Bb2', 'Eb2', 'A3', 'G4'] # -2, -9, +9, +19
		
		self.percussive_rhythms = ['4beat', '8beat', '16beat', 'fills']


if __name__=="__main__":

	tpl_info = template_info()
	#load file
	
	path_in = 'src_template_original/templates.wav'
	path_out_src = 'src_templates/'
	path_out_SRC = 'src_templates_stft/'

	for path in [path_out_src, path_out_SRC]:
		if not os.path.exists(path):
			os.makedirs(path)
	
	src, sr = librosa.load(path_in, mono=True, sr=SR)
	#how to segment 
	len_seg = 4 # [sec]
	sp_per_seg = len_seg * sr

	len_each_h_ins = len_seg * len(tpl_info.harmonic_chords)
	len_each_key = len_seg * len(tpl_info.instruments)
	len_harmonic = len_each_key * len(tpl_info.harmonic_keys)

	len_percussive = len_seg * len(tpl_info.percussive_rhythms)

	# trim, get stft, and save.
	out_filenames = []
	seg_idx = -1
	for h_key in tpl_info.harmonic_keys:
		for h_inst in tpl_info.harmonic_ins:
			for h_chord in tpl_info.harmonic_chords:
				segment_name = '%s_%s_%s' % (h_key, h_inst, h_chord)
				seg_idx += 1
				sp_from = seg_idx*sp_per_seg
				sp_to = sp_from + sp_per_seg
				src_here = src[sp_from:sp_to]
				SRC = librosa.stft(src_here, n_fft=N_FFT, hop_length=HOP_LEN)
				librosa.output.write_wav(path_out_src + segment_name + '.wav', src_here, sr)
				np.save(path_out_SRC + segment_name + '.npy', SRC)
				out_filenames.append(segment_name + '.npy')
	
	for p_inst in tpl_info.percussive_ins:
		for p_rhythm in tpl_info.percussive_rhythms:
			segment_name = '%s_%s' % (p_inst, p_rhythm)
			seg_idx += 1
			sp_from = seg_idx*sp_per_seg
			sp_to = sp_from + sp_per_seg
			src_here = src[sp_from:sp_to]
			SRC = librosa.stft(src_here, n_fft=N_FFT, hop_length=HOP_LEN)
			librosa.output.write_wav(path_out_src + segment_name + '.wav', src_here, sr)
			np.save(path_out_SRC + segment_name + '.npy', SRC)
			out_filenames.append(segment_name + '.npy')


