# neuro_tools

Utilities for resting-state fMRI analysis focused on DMN connectivity

## Features 
- ROI time series extraction from fMRIPrep outputs
- Intra-DMN connectivity metrics
- CLI-based workflow

## Requirements
- Python 3.9+
- NiLearn
- Nibabel
- fMRIPrep (external)
- FSL (optional, external)

## Example
```bash
extract_ts \
	--bold sub-01_task-rest_space-MNI152_desc-preproc-bold.nii.gz \
	--confounds confounds.tsv \
	--out results/

dmn_connectivity --in results/
```

## Notes
ROIs are defined in MNI space using canonical DMN coordinates.
- PCC (0, -52, 26)
- mPFC (3, 54, -2)
- IPL L (-50, -63, 32)
- IPL R (48, -69, 35)
