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

Al finalizar bidscoiner, los resultados tendrán una estructura:

```text
BIDS/
├── code/
├── derivatives/
│	├── logs/
│	├── sourcedata/
│	├── sub-01/
│	├── sub-02/
│	├── ...
│	├── sub-XX/
│	├── .bidsignore
│	├── dataset_description.json
│	├── sub-01.html
│	├── sub-02-html
│	├── ...
│	└── sub-XX.html
│
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
