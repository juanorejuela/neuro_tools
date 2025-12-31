# Pipeline de Resting-State fMRI
Documentación paso a paso para el procesamiento y análisis de estudios de resting-state fMRI.
Este documento esta creado especificamente para nuestra institución, sin embargo, podría ser replicado por alguien más si fuera necesario.

## Requisitos
- BIDS
- fMRIPrep
- FSL

## BIDS
BIDScoin es una herramienta que permite convertir los datos crudos de las neuroimágenes en conjuntos de datos organizados y estructurados de acuerdo al estándar Brain Imaging Data Structure (BIDS).
BIDScoin espera una carpeta con la siguiente estructura:

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
bidsmapper source_folder bids_folder
bidscoiner source_folder bids_folder
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
### Metodología
Todos los datos DICOM fueron organizados y convertidos al estándar BIDS (Brain Imaging Data Structure) usando BIDScoin (v.4.6.2), siguiendo la metodología y recomendaciones descritas por Zwiers et al. [10.3389/fninf.2021.770608]

All DICOM data were organized and converted to the standard BIDS (Brain Imaging Data Structure) using BIDScoin (v.4.6.2), following the methodology and recommendations described by Zwiers et al. [10.3389/fninf.2021.770608]

## fMRIPrep
fMRIPrep es una aplicación NiPreps (Neuroimaging PREProcessing toolS) utilizada para el preprocesamiento de los estudios de resonancia magnética funcional basada en tareas y reposo.
Esta aplicación utiliza una combinación de herramientas incluyendo FSL, ANTs, FreeSurfer y AFNI para la ejecución de pasos básicos de preprocesamiento como coregistro, normalización, unwarping, extracción de componentes de ruido, segmentación, extracción de cráneo, entre otros. El uso de esta aplicación permite de manera fácil acceder a una interfaz actualizada y robusta ante variaciones en los protocolos de adquisición requiriendo mínimas intervenciones por parte del usuario.

Para ejecutar, siga las siguientes instrucciones:

```bash
source fmriprep/bin/activate
fmriprep-docker bids_folder bids_folder_derivatives participant -w work/
fmriprep-docker BIDS/ BIDS/derivatives/ participant -w work/
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
│	│	└── log7
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

## Identificación cuantitativa de la red neuronal por defecto (DMN)
