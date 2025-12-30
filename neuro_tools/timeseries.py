import pandas as pd
from nilearn.maskers import NiftiSpheresMasker

def extract_roi_timeseries(
	bold_img,
	confounds_tsv,
	roi_coords,
	radius=6,
	tr=2.0,
	low_pass=0.1,
	high_pass=0.01,
	confound_cols=None,
	standardize=True
):

	"""
	Extract ROI-based BOLD time series from preprocessed fMRI data.

	Parameters
	----------------
	bold_img : str
		Path to preprocessed BOLD NIfTI (MNI Space).
	confounds_tsv : str
		Path to fMRIPrep confounds TSV.
	roi_coords : dict
		Dict of ROI_name -> [(x, y, z)] in MNI.
	radius : int
		Radius of spherical ROI in mm.
	tr : float
		Repetition time (seconds).
	low_pass, high_pass : float
		Temporal filtering (Hz)
	confound_cols : list
		Confound columns to regress out.
	Standardize : bool
		Z-score time series.

	Returns
	----------------
	dict
		ROI_name -> 1D numpy array (time series)
	"""

	if confound_cols is None:
		confounds_cols = [
			"trans_x","trans_y","trans_z",
			"rot_x","rot_y","rot_z",
			"csf","white_matter"
		]

	confounds = pd.read_csv(confounds_tsv, sep="\t")
	confounds = confounds[confounds_cols]
	
	ts_dict = {}
	
	for roi, coords in roi_coords.items():
		masker = NiftiSpheresMasker(
			coords,
			radius=radius,
			detrend=True,
			standardize=standardize,
			low_pass=low_pass,
			high_pass=high_pass,
			t_r=tr
		)

		ts = masker.fit_transform(
			bold_img,
			confounds=confounds
		)
		
		ts_dict[roi] = ts.squeeze()
	
	return ts_dict
