# Pipeline de Resting-State fMRI
Documentación paso a paso para el procesamiento y análisis de estudios de resting-state fMRI.
Este documento esta creado especificamente para nuestra institución, sin embargo, podría ser replicado por alguien más si fuera necesario.

## Requisitos
- BIDS [https://bidscoin.readthedocs.io/en/stable/index.html]
- fMRIPrep [https://fmriprep.org/en/stable/index.html]
- fMRIPost-AROMA [https://fmripost-aroma.readthedocs.io/latest/index.html] 
- FSL [https://fsl.fmrib.ox.ac.uk/fsl/docs/index.html]

## Estructuración de datos - BIDS
BIDScoin es una herramienta orientada a la conversión sistemática de datos de neuroimagen crudos (por ej., DICOM) al estándar BIDS (Brain Imaging Data Structure), basada en un enfoque declarativo mediante reglas de mapeo. A partir de los metadatos de adquisición, BIDScoin define de forma explícita la correspondencia entre secuencias, entidades BIDS y campos sidecar JSON, permitiendo una conversión reproducible, auditable y escalable. Este enfoque minimiza ambigüedades en la organización de los datos, facilita el control de calidad desde etapas tempranas y garantiza compatibilidad natia con pipelines automatizados como _fMRIPrep_, _fMRIPost_ y herramientas de análisis posteriores, fortaleciendo la validez metodológica y la reproducibilidad del estudio.
BUDScoin requiere que el repositorio de fuente de datos esté organizado de aceurdo a la estructura subject/[session]/data (la carpeta _session_ es siempre opcional). La carpeta data puede estar estructurada como se muestra a continuación:

```text
source_folder/
├── sub-01/
├── sub-02/
├── ...
└── sub-XX/
```

BIDScoin ha sido instalado en un entorno específico. Para ejecutarlo, siga las siguientes instrucciones:

```bash
source bidscoin/bin/activate
bidsmapper source_folder bids_folder # Scans your data and creates a study bidsmap
bidscoiner source_folder bids_folder # Converts your data to BIDS using the study bidsmap
```

Al finalizar bidsmapper, se abrirá un cuadro de diálogo para validar el resultado del proceso. Acá se debe validar que las secuencias hayan sido clasificadas correctamente (por ej. anat, func, ...), excluir aquellas que no sean necesarias, ajustar la estructura de los nombres si fuera necesario, etc.
Al finalizar bidscoiner, todos los archivos estarán organizados siguiendo una estructura:

```text
BIDS/
├── code/
├── sub-01/
│	├── anat/
│	├── dwi/
│	├── fmap/
│	├── func/
│	└── sub-01_scans.tsv
├── sub-02/
├── ...
├── sub-XX/
├── .bidsignore
├── dataset_description.json
├── participants.json
├── participants.tsv
└── README
```

Para validar el resultado, puede utilizar alguna herramienta BIDS validator [https://bids-standard.github.io/bids-validator/]

### Metodología
- Todos los datos DICOM fueron organizados y convertidos al estándar BIDS (Brain Imaging Data Structure) usando BIDScoin (v.4.6.2), siguiendo la metodología y recomendaciones descritas por Zwiers et al. [10.3389/fninf.2021.770608]
- All DICOM data were organized and converted to the standard BIDS (Brain Imaging Data Structure) using BIDScoin (v.4.6.2), following the methodology and recommendations described by Zwiers et al. [10.3389/fninf.2021.770608]

## Preprocesamiento de datos - fMRIPrep
_fMRIPrep_ es un pipeline de preprocesamiento estandarizado y totalmente automatizado para datos de fMRI organizados en estándar BIDS, diseñado para maximizar la reproducibilidad, la transparencia y la robustez metodológica. Integra herramientas consolidadas como FSL, ANTs, FreeSurfer y AFNI para realizar correccción de movimiento, corrección de distorsiones geométricas, normalización espacial a espacios estándar, segmentación tisular y extracción de variables de confusión relacionadas con movimiento y señales fisiológicas. _fMRIPrep_ permite la normalización a distintos espacios de referencia, incluyendo _MNI152NLin6Asym_, un template simétrico y no lineal ampliamente utilizado que resulta especialmente adecuado para análisis de conectividad funcional y comparaciones inter-sujeto. El pipeline adopta un enfoque *analysis-agnostic*, generando salidas mínimamente procesadas junto con reportes visuales exhaustivos de control de calidad, lo que garantiza trazabilidad completa del preprocesamiento y facilita su integración con análisis posteriores de conectividad y modelado estadístico.

Para ejecutar, siga las siguientes instrucciones:

```bash
source fmriprep/bin/activate
fmriprep-docker bids_folder bids_folder_derivatives participant -w work/ --fs-license-file ~/license.txt
fmriprep-docker BIDS/ BIDS/derivatives/ participant -w work/ --fs-license-file ~/license.txt
#  Si se utilizará fMRIPost-Aroma es importante agregar el flag \
## --output-spaces con el valor MNI152NLin6Asym:res-02
fmriprep-docker bids_folder bids_folder_derivatives participant -w work/ \
--output-spaces MNI152NLin6Asym:res-02 --fs-license-file ~/license.txt
```

Al finalizar, los resultados estarán en la carpeta BIDS/derivatives/ siguiendo una estructura así:

```text
BIDS/
├── code/
├── derivatives/
│	├── logs/
│	├── sourcedata/
│	├── sub-01/
│	│	├── anat/
│	│	├── figures/
│	│	├── func/
│	│	└── log/
│	├── sub-02/
│	├── ...
│	├── sub-XX/
│	├── .bidsignore
│	├── dataset_description.json
│	├── sub-01.html
│	├── sub-02-html
│	├── ...
│	└── sub-XX.html
├── sub-01/
├── sub-02/
├── ...
├── sub-XX/
├── .bidsignore
├── dataset_description.json
├── participants.json
├── participants.tsv
└── README
```

Podrá validar los resultados utilizando los html ubicados dentro de la carpeta derivatives/ para cada sujeto.

### Metodología
fMRIPrep (v.25.2.3) [10.1038/s41592-018-0235-4]

## Posprocesamiento de los datos - fMRIPost-AROMA
_fMRIPost-AROMA_ es un pipeline de posprocesamiento diseñado para aplicar _ICA-AROMA_ sobre las salidas de fMRIPrep, con el objetivo de identificar y mitigar artefactos relacionados con movimineto en datos de fMRI en reposo. El método se basa en una descomposición por Análisis de Componentes Independientes (ICA), seguida de una clasificación automática de componentes en señal neuronal o ruido, utilizando métricas espaciales y temporales (por ejemplo, fracción en bordes, correlación con movimiento y contenido de alta frecuencia). fMRIPost-AROMA opera sobre datos previamente normalizados (típicamente en MNI152NLin6Asym) y genera métricas y mezclas ICA que permiten aplicar distintas estrategias de *denoising* (agresivo o no agresivo) mediante regresión de los componentes clasificados como ruido. En este enfoque reduce de forma efectiva la influencia del movimiento sin introducir supuestos anatómicos fuertes, siendo espacialmente adecuado para análisis de conectividad funcional en *resting-state*.

- Antes de utilizar el volumen BOLD de la secuencia de reposo, debemos ejecutar el flujo de AROMA. Es importante garantizar que el preprocesamiento realizado con fMRIPrep incluya las salidas en espacio MNI152NLin6Asym con voxeles de 2 mm3.
- El volumen resultante de interés para fases posteriores es el  sub-0....MNI152NLinAsym_res-2...aggrDenoised...nii.gz.

Para ejecutar el fMRIPost-AROMA, use la siguiente función:

```bash
docker run --rm -it \
-v ~/research/_test/BIDS/derivatives:/data/fmriprep:ro \
-v ~/research/_test/BIDS/derivatives/fmripost_out:/out \
nipreps/fmripost-aroma:0.0.12 /data/fmriprep /out participant \
--denoising-method aggr
```

El volumen resultante de interés se encontrará en la subcarpeta func/ y será el volumen sub-XX...desc-aggrDenoised_bold.nii.gz

### Metodología
fMRIPost-AROMA versión 0.0.12 [10.1016/j.neuroimage.2015.02.063]

## Cálculo de conectividad interna de la Red Neuronal por Defecto (DMN)
Para calcular la conectividad intra-DMN, se extraen las series temporales de cada región de interés que componen la DMN (PCC, mPFC, IPC derecha e izquierda), utilizando como entrada el volumen .nii preprocesado con fMRIPrep. Las regiones de interés son construidas utilizando las coordenadas definidas más adelante y un radio de 6 mm.. Las señales son estandarizadas temporalmente (z-score) para normalizar la señal y minimizar la variabilidad entre regiones. Se calculan las correlaciones de Pearson entre las ROI. Posteriormente, los coeficientes de correlación se transforman mediante la transformación de Fisher z con el fin de cumplir los supuestos de normalidad, permitiendo la aplicación de pruebas estadísticas paramétricas y el cálculo de promedios de conectividad por sujeto y por red en análisis de grupos.
Este proceso se realiza mediante la utilización de dos funciones desarrolladas in-house:

```bash
extract_ts --bold bold_file --confounds conf_file -o results
extract_ts --bold BIDS/derivatives/sub-XX/func/sub-XX_task-reposo...desc-preproc_bold.nii.gz \
--confounds BIDS/derivatives/sub-XX/func/sub-XX_task-reposo...confounds_timeseries.tsv \
--out BIDS/derivatives/dmn_results
```

La carpeta results/ resultante del extract_ts debe estar en una estructura así:

```text
BIDS/derivatives/dmn_results/
├── sub-01/
│	├── IPL_L.txt
│	├── IPL_R.txt
│	├── mPFC.txt
│	└── PCC.txt
├── sub-02/
├── ...
└── sub-XX/
```

Para hacer un procesamiento secuencial de múltiples sujetos, se puede ejecutar la siguiente función:

```bash
for sub in ~/project/BIDS/fmri_post/sub-*; do \
	sid = $(basename $sub); \
	extract_ts \
		--bold $sub/func/${sid}_task-Reposo_dir-AP...-aggrDenoised_bold.nii.gz \
		--confounds ~/project/BIDS/derivatives/${sid}/func/${sid}_task-Reposo_dir-AP...-confounds_timeseries.tsv \
		--out ~/project/BIDS/derivatives/dmn_results/%{sid}; \
done
```

Cuando todos los sujetos han sido procesados, ejecutar dmn_connectivity para extrar las correlaciones de todo el grupo.

```bash
dmn_connectivity --ts-dir BIDS/derivatives/dmn_results/ \
--out BIDS/derivatives/dmn_results/metrics.csv
```

El resultado (metrics.csv) tendrá los valores de correlación de Pearson y la transformación Fisher z para cada par de ROI y cada sujeto, incluyendo también el promedio.

### Metodología
Se definieron regiones de interés esféricas (radio de 6 mm) para equilibrar la especificidad anatómica y la relación señal-ruido, en consonancia con estudios previos de conectividad por fMRI. Las semillas se construyeron en el espacio del Instituto Neurológico de Montreal (MNI): corteza cingulada posterior (PCC) (0, -53, 26), corteza prefrontal medial (mPFC) (3, 54, -2), corteza intraparietal izquierda (LIPC) (-50, -63, 32) y corteza intraparietal derecha (RIPC) (48, -69, 35).
[10.1038/srep46088, 10.1016/j.neuroimage.2013.07.071, 10.3389/fnhum.2016.00014]

## Identificación cuantitativa de la red neuronal por defecto (DMN)
El primer paso es ejecutar el MELODIC ICA de FSL. Para esto, utilizaremos el volumen sub-XX\_task-reposo...desc-preproc\_bold.nii.gz como entrada.
La salida del MELODIC ICA tendrá una estructura:

```text
melodic_results/
├── sub-01.ica/
│	├── .files/
│	├── filtered_func_data.ica/
│	│	├── melodic_IC.nii.gz
│	│	└── ...
│	├── logs/
│	├── mc/
│	├── reg/
│	├── absbrainthresh.txt
│	├── design.fsf
│	├── example_func.nii.gz
│	├── filtered_func_data.nii.gz
│	├── mask.nii.gz
│	├── mean_func.nii.gz
│	├── report.html
│	├── report_log.html
│	├── report_prestats.html
│	├── report_reg.html
│	└── report_unwarp.html
├── sub-02.ica/
├── ...
└── sub-XX.ica/
```

Posteriormente, realizaremos un resampling de la máscara Yeo 7 (DMN), y calcularemos las correlaciones entre la máscara y las redes neuronales encontradas en el análisis ICA a fin de identificar aquella red con la correlación más alta.
El volumen de entrada para este proceso es melodic_IC.nii.gz ubicada en melodic\_results/sub-XX.ica/filtered\_func\_data.ica/

```bash
flirt -in ~/research/__tools/atlas/Yeo7_DMN-3mm-mask_bin.nii.gz \
	-ref filtered_func_data.ica/melodic_IC.nii.gz -applyxfm -usesqform \
	-out rois/Yeo7_DMN-3mm-mask_bin_resampled.nii.gz

fslcc filtered_func_data.ica/melodic_IC.nii.gz rois/Yeo7_DMN-3mm-mask_bin_resampled.nii.gz
```

El resultado será una lista de correlaciones, una por componente, sugiriendo que la correlación más alta corresponde al componente que mayor probabilidad tiene de ser la DMN. 
Esto también puede ser ejecutado con las otras redes de Yeo:
- Yeo 1: Medial visual
- Yeo 2: Sensory motor
- Yeo 3: Dorsal attention
- Yeo 4: Ventral attention
- Yeo 5: Frontoparietal
- Yeo 6: Default Mode Network
- Yeo 7: Subcortical

Todas las redes se encuentran disponibles en ~research/__toolts/atlas/

Para extrer la red del melodic_IC.nii.gz y generar una máscara de la red, en caso de ser necesarios, puede ejecutar los siguientes comandos:

```bash
fslroi filtered_func_data.ica/melodic_IC.nii.gz results/comp_DMN.nii.gz N 1

fslmaths resuts/comp_DMN.nii.gz -thr 3 -bin results/comp_DMN_mask.nii.gz
```

Los componentes están en 4D, en el comando fslroi reemplace N por el # del componente deseado empezando en 0, es decir, si el componente identificado es el #34, defina 33.
