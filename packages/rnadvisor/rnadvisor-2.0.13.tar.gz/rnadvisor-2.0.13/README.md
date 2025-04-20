![img](img/RNAdvisor_page.gif)

<div align="center">

<!-- omit in toc -->
# RNAdvisor v2 🚀
<strong>Fast and easy way to compute RNA 3D structural quality</strong>

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![slim](https://img.shields.io/badge/docker-slim-blue)](https://github.com/slimtoolkit/slim)
[![Python](https://img.shields.io/pypi/pyversions/tensorflow.svg)](https://badge.fury.io/py/tensorflow)
[![DOI](https://img.shields.io/badge/DOI-10.1093/bib/bbae064-green)](https://doi.org/10.1093/bib/bbae064)

</div>

RNAdvisor is a wrapper tool for the computation of RNA 3D structural quality assessment. 
It uses [docker compose](https://docs.docker.com/compose/) to run the RNAdvisor tool in a containerized environment. 

```python
from rnadvisor.rnadvisor_cli import RNAdvisorCLI

rnadvisor_cli = RNAdvisorCLI(
    pred_dir="data/example/PREDS",
    native_path="data/example/NATIVE/R1107.pdb",
    output_path="out.csv",
    scores=["rmsd", "inf", "mcq", "lddt","tm-score", "gdt-ts", "ares", "pamnet"]
)
df_results, df_time = rnadvisor_cli.predict()
```

## Installation

To install RNAdvisor v2 you need to have [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) installed on your system.
Then, you can install the package using pip:

```bash
pip install rnadvisor
```

Then you can compute the RNA 3D structural quality assessment using the command line interface (CLI) or the python API.
```bash
rnadvisor --pred_dir --scores [--native_path] [--out_path ]
          [--out_time_path] [--sort_by] [--params] [--tmp_dir] 
          [--verbose] [--z_score] [--normalise]
``` 
with: 
```
  --pred_dir            Directory to .pdb files or path to a .pdb file of the predictions. 
  --native_path         Path to a .pdb file of the native structure.
  --scores              List of the scores to use, separated by a comma. 
                        If you want to use them all, use `all`. To use all the metrics, use `metrics`
                        To use all the scoring functions, use `sf`.
                        Choice between clash,pamnet,lociparse,3drnascore,tb-mcq,barnaba,cgrnasp,dfire,mcq,
                        lcs,cad-score,tm-score,lddt,rasp,rs-rnasp,rmsd,inf,p-value,di,gdt-ts,ares
  --out_path            Path to a .csv file where to save the predictions.
  --out_time_path       Path to a .csv file where to save the time of the predictions for each score.
  --sort_by             Metric to sort the results by.
  --verbose             Level of verbosity. 0 for no output, 1 for basic output, 2 for detailed output.
  --params              Hyperparameters of the different methods. It could be used to set the threshold for LCS-TA 
   or parameters of MCQ using `--params='{"mcq_threshold": 10, "mcq_mode": 2}'`. Values for `mcq_threshold` are 10, 15, 20 or 25 and values for 
    `mcq_mode` are 0 (relaxed), 1 (comparison without violations) or 2 (comparison of everything regardless violations).
  --z_score             Compute the Z-score for the computed scores. It reverses all the descreasing scores.
  --normalise           If the user doesn't want to normalise the .pdb files. It will run the --rna-puzzles-ready from RNA-tools.
  --sort-by             Metric to sort the results by. Choice between RMSD,P-VALUE,INF-ALL,INF-WC,INF-NWC,INF-STACK,DI,MCQ,TM-SCORE,GDT-TS,GDT-TS@1,GDT-TS@2,GDT-TS@4,GDT-TS@8,CAD,lDDT,RASP,BARNABA,DFIRE,rsRNASP.
```

## Existing tools

Each of the scoring functions and metrics are isolated in individual docker containers.
You can find each of them in dockerhub with: `sayby/rnadvisor-<name>-slim` or `sayby/rnadvisor-<name>`.

`<name>` can be one of the following:

| Scoring Function | Metric      |
|------------------|-------------|
| `3drnascore`     | `rmsd`      |
| `lociparse`      | `inf`       |
| `tb-mcq`         | `p-value`   |
| `escore`         | `di`        |
| `pamnet`         | `mcq`       |
| `cgrnasp`        | `gdt-ts`    |
| `dfire`          | `lddt`      |
| `rasp`           | `tm-score`  |
| `rsRNASP`        | `cad-score` |
| `ares`            | `clash`         |


The `slim` version is a smaller version of the container that only contains the necessary codes to run the scoring function (e.g. no bash, no other commands, etc.).
It corresponds to the original image reduced with [`docker-slim`](https://github.com/slimtoolkit/slim).

## Docker build

If you want to build yourself the docker images, you can do so by running the following command in the root directory of the repository:

```bash
just build-<name>-full 
```
with `<name>` being the name of the scoring function/metric you want to build.

To get the `slim` version, you can run the following command:

```bash
just build-<name>-slim
```