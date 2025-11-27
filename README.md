# zinc-downloader

[![PyPI](https://img.shields.io/pypi/v/zincdl.svg)](https://pypi.org/project/zincdl/)
![Python](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12%20|%203.13-blue)
![License](https://img.shields.io/github/license/seungchan-an/zinc-downloader)

Reproducible and scriptable downloader for **ZINC tranches**. 
`zincdl` allows reconstruction of ZINC tranche codes from property subsets, retrieval of corresponding download URLs, and batch file download from the public ZINC repository.

**Relevant links**  
- [ZINC tranche browser (ZINC20)](https://zinc.docking.org/tranches) – where tranches are browsable
- [ZINC static files](https://files.docking.org/) – source of downloadable tranche data  
- [ZINC Wiki](https://wiki.docking.org/index.php/Tranche_Browser) – background on tranche organization

> ⚠️ **Note**
> `zincdl` is an independent open-source utility for ZINC data access, and **not affiliated with** or **maintained by** the Irwin Lab @ UCSF.
> This tool only automates access to publicly available ZINC files and does not redistribute any data. Please **avoid excessive parallel downloads**.

---

## 🔧 Installation

```bash
$ pip install zincdl
```

## Usage
You can generate tranche codes and corresponding URLs for arbitrary property selections, and optionally download them.
Note: using predefined subsets (via `subset` in generate_urls or `--subset` in CLI) yields the highest chance of successful downloads.

#### Python API
```python
from zincdl import generate_urls
from zincdl.download import download_tranches

# Generate tranche URLs from an MW × logP region
urls = generate_urls(
    mw=[300, 325],
    logp=[2, 3],
    fmt="mol2",
)

print(urls)
# [
#   'https://files2.docking.org/3D/CD/EBRN/CDEBRN.xaa.mol2.gz',
#   'https://files2.docking.org/3D/CF/EBRN/CFEBRN.xaa.mol2.gz',
#   ...
# ]

# Download into a local directory
download_tranches(urls, out_dir="my_zinc")
```

#### CLI
```bash
# Show help
zincdl --help

# Preview tranche URLs (no download)
zincdl --mw 300,325 --logp 2,3 --fmt smi

# Download predefined subsets
zincdl --subset fragments --fmt mol2 --download --out-dir downloads/fragments
zincdl --subset leadlike --fmt smi --download --out-dir downloads/leadlike

# Include charge, pH, and reactivity filters
zincdl --subset druglike --charge 1 --fmt sdf --download --out-dir downloads/druglike_cationic
```

## Citation
Please cite ZINC20 when using downloaded data:

> Irwin, J. J.; Tang, K. G.; Young, J.; Dandarchuluun, C.; Wong, B. R.; Khurelbaatar, M.; Moroz, Y. S.; Mayfield, J.; Sayle, R. A. **ZINC20 — A Free Ultralarge-Scale Chemical Database for Ligand Discovery.** *J. Chem. Inf. Model.* **2020**, 60, 6065–6073. https://doi.org/10.1021/acs.jcim.0c00675