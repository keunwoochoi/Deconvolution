"""
01 Jan 2016
"""

import matplotlib.pyplot as plt
import numpy as np
import librosa
import pdb
import os
import sys
from multiprocessing import Pool
from main_trim import template_info
from constants import *

def export_image(args):
	feat, tpl_info, h_key, layer = args
	harmonic_ins = tpl_info.harmonic_ins
	harmonic_chords = tpl_info.harmonic_chords

	sub_folder = '%d_%d/' % (layer ,feat)

	path_deconv_results = 'results/'
	path_img_results = 'images/'
	if not os.path.exists(path_img_results):
		os.makedirs(path_img_results)
	path_img_out = '%s%s/' % (path_img_results, sub_folder)
	path_img_out2= '%slayer-%d/' % (path_img_results, layer)

	if not os.path.exists(path_img_out):
		os.makedirs(path_img_out)
	if not os.path.exists(path_img_out2):
		os.makedirs(path_img_out2)

	img_name = '%d_%d_%s.png' % (layer, feat, h_key)
	if os.path.exists(path_img_out2 + img_name):
		return

	wav_name_suffix = '_deconved_from_depth_%d_feature_%d' % (layer, feat)

	fig, axes = plt.subplots(nrows=len(harmonic_ins), 
							ncols=len(harmonic_chords),
							sharex='col', 
							sharey='row')
	for inst_idx, h_inst in enumerate(harmonic_ins):
		for chord_idx, h_chord in enumerate(harmonic_chords):
			ax = axes[inst_idx][chord_idx]
			segment_name = '%s_%s_%s' % (h_key, h_inst, h_chord)
			path_wav = '%s%s/' % (path_deconv_results, segment_name)
			filename_wav = segment_name + wav_name_suffix
			src_here, sr = librosa.load(path_wav+filename_wav+'.wav', 
										sr=SAMPLE_RATE, 
										mono=True)
			SRC = librosa.stft(src_here, 
								n_fft=N_FFT, 
								hop_length=N_FFT/2)
			ax.imshow(librosa.logamplitude(np.flipud(np.abs(SRC))), aspect=200)
			ax.set_xticks([], [])
			ax.set_yticks([], [])
			ax.axis('auto')
			if chord_idx == 0:
				ax.set_ylabel(harmonic_ins[inst_idx][:6])
			if inst_idx == len(harmonic_ins)-1:
				ax.set_xlabel(harmonic_chords[chord_idx])

	fig.savefig(os.path.join(path_img_out, img_name), dpi=200, bbox_inches='tight')
	fig.savefig(os.path.join(path_img_out2, img_name), dpi=200, bbox_inches='tight')
	plt.close(fig)
	print '%s: done' % img_name
	return

if __name__=="__main__":

	if len(sys.argv) == 2:
		layers = [int(sys.argv[1])]
	else:
		layers = [5,4,3,2,1]	

	tpl_info = template_info()
	
	p = Pool(8)
	p.daemon = True

	
	num_features = 64
	features = range(64)

	seg_idx = -1
	for layer in layers:
		for h_key in tpl_info.harmonic_keys:
			# multiprocessing doesn't work due to matplotlib/GUI/main_thread/etc..
			# args = zip(features, [tpl_info]*num_features, [h_key]*num_features, [layer]*num_features)
			# p.map(export_image, args)
			for feat in features:
				args= (feat, tpl_info, h_key, layer)
				export_image(args)

			
	'''
	for p_inst in tpl_info.percussive_ins:
		for p_rhythm in tpl_info.percussive_rhythms:
			segment_name = '%s_%s' % (p_inst, p_rhythm)
			seg_idx += 1
	'''
