import gzip
import hashlib
import inspect
import logging
import os
import pickle
import re
import sys
import time
import timeit
import warnings
from functools import lru_cache, partial, reduce, wraps
from pathlib import Path
from urllib.parse import urljoin

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import pkg_resources
import plotly.graph_objs as go
import pyranges as pr
import scipy.stats as stats
import xxhash
from scipy.stats import norm, rankdata
from sklearn.linear_model import LinearRegression
from tqdm import tqdm

from mepylome import *
from mepylome.analysis.methyl import *
from mepylome.analysis.methyl_aux import *
from mepylome.analysis.methyl_clf import *
from mepylome.dtypes import *
from mepylome.dtypes.cache import *
from mepylome.dtypes.cnv import *
from mepylome.dtypes.manifests import *
from mepylome.dtypes.plots import *
from mepylome.tests.helpers import *
from mepylome.tests.write_idat import *
from mepylome.utils import *
from mepylome.utils.files import *

pdp = lambda x: print(x.to_string())

# warnings.simplefilter(action="ignore", category=FutureWarning)

# TODO: Delete button for uploaded files and corresponding betas/cnv

ENDING_GZ = ".gz"
ENDING_GRN = "_Grn.idat"
ENDING_RED = "_Red.idat"


LOGGER = logging.getLogger(__name__)
print("imports done")

timer = Timer()

smp_dir = Path("~/mepylome/tutorial/tutorial_analysis").expanduser()
ref_dir = Path("~/mepylome/tutorial/tutorial_reference/").expanduser()

smp_files = sorted(smp_dir.glob("*"))[:8]
ref_files = sorted(ref_dir.glob("*"))[:5]

smp0, smp1, smp2, smp3, smp4, smp5, smp6, smp7 = map(str, smp_files)
ref0, ref1, ref2, ref3, ref4 = map(str, ref_files)

timer = Timer()
idat_data = IdatParser(smp0)
timer.stop("Parsing IDAT")

# timer = Timer()
# idat_data = _IdatParser(smp0)
# timer.stop("Parsing IDAT C++")

timer = Timer()
idat_data = IdatParser(smp0, intensity_only=True)
timer.stop("Parsing IDAT")


GENES = pkg_resources.resource_filename("mepylome", "data/hg19_genes.tsv.gz")
GAPS = pkg_resources.resource_filename("mepylome", "data/gaps.csv.gz")


# quit()

timer.start()
# refs_raw = RawData(ref_dir)
refs_raw = RawData([ref0, ref1])
timer.stop("RawData ref")

timer.start()
ref_methyl = MethylData(refs_raw)
timer.stop("MethylData ref")


timer.start()
manifest = Manifest("epic")
timer.stop("Manifest")


timer.start()
sample_raw = RawData(smp0)
timer.stop("RawData sample")

timer.start()
sample_methyl = MethylData(sample_raw, prep="illumina")
timer.stop("MethylData sample")

timer.start()
betas = sample_methyl.betas_at(cpgs=None, fill=0.49)
timer.stop("beta 1")

timer.start()
betas = sample_methyl.betas_at(cpgs=None, fill=0.49)
timer.stop("beta 2")

gap = pr.PyRanges(pd.read_csv(GAPS))
gap.Start -= 1

timer.start()
genes_df = pd.read_csv(GENES, sep="\t")
genes_df.Start -= 1
genes = pr.PyRanges(genes_df)
genes = genes[["Name"]]
timer.stop("genes")

timer.start()
annotation = Annotation(manifest, gap=gap, detail=genes)
timer.stop("Annotation")

timer.start()
cnv = CNV(sample_methyl, ref_methyl, annotation)
timer.stop("CNV init")


timer.start()
cnv.set_bins()
timer.stop("CNV set_bins")

timer.start()
cnv.set_detail()
timer.stop("CNV set_detail")

timer.start()
cnv.set_segments()
timer.stop("CNV set_segments")

self = cnv
sample = sample_methyl
reference = ref_methyl

timer.start()
cnv = CNV.set_all(sample_methyl, ref_methyl)
timer.stop("CNV set_all")


quit()

timer.start()
# r = RawData(smp7)
r = RawData([ref0, ref1])
timer.stop("1")
m = MethylData(r)
timer.stop("2")
m.illumina_control_normalization()
timer.stop("2.1")
m.illumina_bg_correction()
timer.stop("2.2")
m.preprocess_raw_cached()
timer.stop("2.5")
b = m.beta
timer.stop("3")


cn = CNV(m, ref_methyl, annotation)
imer.stop("2")
timer.stop("3")

self = sample_methyl
self = ref_methyl

timer.start()
cn._set_bins()
# cn.set_bins()
timer.stop("4")
cn.bins

cn.set_detail()
timer.stop("5")
cn.set_segments()
timer.stop("file to csv")


filepath_gz = Path("~/Downloads/manifest.pkl.gz").expanduser()
filepath = Path("~/Downloads/manifest.pkl").expanduser()

timer.start()
with gzip.open(filepath_gz, "wb") as f:
    pickle.dump(manifest, f)

timer.stop("pickel")

timer.start()
with gzip.open(filepath_gz, "rb") as f:
    loaded_data = pickle.load(f)

timer.stop("pickel")


timer.start()
with open(filepath, "wb") as f:
    pickle.dump(manifest, f)

timer.stop("pickel")

timer.start()
with open(filepath, "rb") as f:
    loaded_data = pickle.load(f)

timer.stop("pickel")


# ANNOTATION
filepath = Path("~/Downloads/annotation.pkl").expanduser()
with open(filepath, "wb") as f:
    pickle.dump(annotation, f)

with open(filepath, "rb") as f:
    loaded_data = pickle.load(f)

filepath = Path("~/Downloads/ref_meth_data.pkl").expanduser()
with open(filepath, "wb") as f:
    pickle.dump(ref_meth_data, f)

with open(filepath, "rb") as f:
    loaded_data = pickle.load(f)

timer.start()
self = MethylData(file=smp6, prep="illumina")
timer.stop("*")


timer.start()
self = MethylData(raw, prep="noob")
timer.stop("*")

timer.start()
self = MethylData(sample_raw, prep="noob")
timer.stop("*")

timer.start()
self = MethylData(sample_raw, prep="swan")
timer.stop("*")


timer.start()
idat_data = mepylome._IdatParser(smp0)
timer.stop("Parsing C++")

timer.start()
py_idat_data = IdatParser(smp0, intensity_only=False)
timer.stop("Parsing Python")


# 0 Home
self = MethylAnalysis(
    analysis_dir="/data/epidip_IDAT",
    reference_dir="/data/ref_IDAT",
    overlap=False,
    cpgs=["450k", "epic", "epicv2"],
    load_full_betas=True,
)

# 1 Brain
self = MethylAnalysis(
    analysis_dir="/mnt/ws528695/data/epidip_IDAT",
    reference_dir="/data/ref_IDAT",
    overlap=True,
    load_full_betas=True,
    debug=True,
    # cpgs=["450k", "epic"],
)

timer.start()
reference_dir = "/data/ref_IDAT"
self = ReferenceMethylData(reference_dir, save_to_disk=True)
ref_meth_data = ReferenceMethylData(reference_dir)
timer.stop()

# 2 Chondrosarcoma
cpgs = Manifest("epic").methylation_probes
blacklist = pd.read_csv("~/Downloads/cpg_blacklist.csv", header=None)
cpgs = np.array(list(set(cpgs) - set(blacklist.iloc[:, 0])))
self = MethylAnalysis(
    # analysis_dir="/data/idat_CSA/",
    analysis_dir="/mnt/storage/sarcoma_idat/csa_project/",
    reference_dir="/data/ref_IDAT",
    n_cpgs=25000,
    load_full_betas=True,
    overlap=False,
    cpgs=cpgs,
    debug=True,
)

# 3 10 Samples
self = MethylAnalysis(
    analysis_dir="/mnt/ws528695/data/epidip_IDAT_10",
    reference_dir="/data/ref_IDAT",
    overlap=False,
    debug=True,
)

# 4 166 Samples
self = MethylAnalysis(
    analysis_dir="/mnt/ws528695/data/epidip_IDAT_116",
    reference_dir="/data/ref_IDAT",
    overlap=False,
    debug=True,
)

# 5 GSE140686_RAW
self = MethylAnalysis(
    analysis_dir="/mnt/storage/cns_tumours/",
    reference_dir="/data/ref_IDAT",
    overlap=False,
    debug=True,
)

# 6 Tutorial
self = MethylAnalysis()
self = MethylAnalysis(
    analysis_dir="~/mepylome/tutorial/tutorial_analysis",
    reference_dir="~/mepylome/tutorial/tutorial_reference",
    test_dir="~/mepylome/tutorial/test_dir",
    debug=True,
    verbose=True,
    do_seg=True,
)

self.run_app(open_tab=True)

# 7 Sarcoma
self = MethylAnalysis(
    analysis_dir="~/Downloads/CSA/E-MTAB-9875",
    reference_dir="/data/ref_IDAT",
    n_cpgs=25000,
    load_full_betas=True,
    debug=True,
)

# 8 Error file
cpgs = Manifest("epic").methylation_probes
self = MethylAnalysis()
self = MethylAnalysis(
    analysis_dir="~/Downloads/mepylome_test_06022025",
    reference_dir="/data/ref_IDAT/",
    debug=True,
    verbose=True,
    do_seg=True,
)

self = MethylAnalysis()
self.run_app(open_tab=True)
self.make_umap()
self.set_betas()

mfile = Path(
    "~/Downloads/Screening_Array_GSE270195_RAW/GSA-24v3-0_A1.csv"
    # "/applications/mepylome_cache/infinium-methylationepic-v-1-0-b5-manifest-file.csv"
).expanduser()
manifest = Manifest(raw_path=mfile)
idat_file = (
    Path("~/Downloads/Screening_Array_GSE270195_RAW")
    / "GSM8336639_204009170074_R01C01_Grn.idat.gz"
)
rdata = RawData(idat_file, manifest=manifest)

from cuml.manifold import UMAP

umap_2d = UMAP(**self.umap_parms).fit_transform(matrix_to_use)


import cupy as cp
import numpy as np
from cuml.manifold import UMAP

np.random.seed(42)
matrix_to_use = cp.asarray(np.random.rand(1000, 50))
matrix_to_use = cp.asarray(analysis.betas_all)
umap_parms = {"n_neighbors": 15, "min_dist": 0.1}
umap_2d = UMAP(**umap_parms).fit_transform(matrix_to_use).get()
fig = px.scatter(x=umap_2d[:, 0], y=umap_2d[:, 1])
fig.show()

print(umap_2d)


np.random.seed(42)
matrix_to_use = cp.asarray(np.random.rand(1000, 50))  # Convert to GPU array
umap_parms = {"n_components": 2, "n_neighbors": 15, "min_dist": 0.1}
umap_2d = UMAP(**umap_parms).fit_transform(matrix_to_use)
umap_2d = cp.asnumpy(umap_2d)  # Convert back to NumPy for plotting
fig = px.scatter(x=umap_2d[:, 0], y=umap_2d[:, 1])
fig.show()

config_path = Path(
    "~/MEGA/programming/mepylome/scripts/diagnostics/config.yaml"
).expanduser()


DIR = Path.home() / "mepylome" / "tutorial"
ANALYSIS_DIR = DIR / "tutorial_analysis"
REFERENCE_DIR = DIR / "tutorial_reference"
from mepylome.utils import setup_tutorial_files

setup_tutorial_files(ANALYSIS_DIR, REFERENCE_DIR)
idat_file = ANALYSIS_DIR / "200925700125_R07C01_Grn.idat"
idat_data = IdatParser(idat_file)
methyl_data = MethylData(file=idat_file)
reference = MethylData(file=REFERENCE_DIR)
cnv = CNV.set_all(methyl_data, reference)
cnv.plot()

short_keys = [
    "analysis_dir",
    "prep",
    "n_cpgs",
    "cpg_selection",
    "analysis_ids",
    "test_ids",
]


class HashManager:
    def __init__(self, short_keys, long_keys):
        self._internal_cpgs_hash = None
        self.short_keys = short_keys
        self.long_keys = long_keys
        self.key_cache = {x: None for x in long_keys}

    def delete(self, key):
        self.long_keys[key] = None

    def get(self, key):
        if key in short_keys:
            return key
        cache = key_cache.get(key)
        if cache is not None:
            return cache

        self.key_cache[key] = value
        return value
        return self._internal_cpgs_hash

    def get_test_files_hash(self):
        if not self.parent.test_dir.exists():
            return ""
        return input_args_id(
            extra_hash=sorted(str(x) for x in self.parent.test_dir.iterdir())
        )

    def get_vars_or_hashes(self):
        vars_hash = {key: getattr(self.parent, key) for key in self.short_keys}
        vars_hash.update(
            {
                "cpgs": self.get_cpgs_hash(),
                "test_files": self.get_test_files_hash(),
            }
        )
        return vars_hash

    def reset_cpgs_hash(self):
        self._internal_cpgs_hash = None


dependencies = ["analysis_dir", "prep", "output_dir"]


logger = logging.getLogger(__name__)


class CacheManager:
    def __init__(self, class_instance):
        self.cache = {}
        self.dependencies = {}
        self.class_instance = class_instance
        self.previous = {}
        self.previous_hashes = {}

    def set_dependencies(self, key, dependencies):
        if key not in self.dependencies:
            self.dependencies[key] = dependencies
            self._update(key, log=False)
        # for dep in dependencies:
        #     self._update(dep)

    def get(self, key):
        """Retrieve a cached value if dependencies haven't changed."""
        self._update(key)
        return self.cache.get(key)

    def set_value(self, key, value):
        """Store a value in the cache."""
        self.cache[key] = value

    def _value_or_hash(self, key):
        hash_value = self.previous_hashes.get(key)
        if hash_value:
            return hash_value
        value = getattr(self.class_instance, key)
        if hasattr(value, "__len__"):
            hash_value = input_args_id(value)
            self.previous_hashes[key] = hash_value
            return hash_value
        return value

    def _update(self, key, log=True):
        current = {
            dep: self._value_or_hash(dep) for dep in self.dependencies[key]
        }
        changed_keys = {
            key for key in current if current[key] != self.previous.get(key)
        }
        if changed_keys:
            if log:
                logger.warning(
                    "Attributes changed: %s", ", ".join(changed_keys)
                )  # TODO: del this
            for key, deps in self.dependencies.items():
                if changed_keys.intersection(deps):
                    self.cache[key] = None
            self.previous = current

    def __repr__(self):
        title = f"{self.__class__.__name__}()"
        header = title + "\n" + "*" * len(title)
        lines = [header]

        def format_value(value):
            length_info = ""
            if isinstance(value, (pd.DataFrame, pd.Series, pd.Index)):
                display_value = str(value)
            elif isinstance(value, np.ndarray):
                display_value = str(value)
                length_info = f"\n\n[{len(value)} items]"
            elif hasattr(value, "__len__"):
                display_value = str(value)[:80] + (
                    "..." if len(str(value)) > 80 else ""
                )
                if len(str(value)) > 80:
                    length_info = f"\n\n[{len(value)} items]"
            elif isinstance(value, (plotly.graph_objs.Figure)):
                data_str = (
                    str(value.data[0])[:70].replace("\n", " ")
                    if value.data
                    else "No data"
                )
                layout_str = str(value.layout)[:70].replace("\n", " ")
                data_str += "..." if len(data_str) == 70 else ""
                layout_str += "..." if len(layout_str) == 70 else ""
                display_value = (
                    f"Figure(\n"
                    f"    data: {data_str}\n"
                    f"    layout: {layout_str}\n"
                    f")"
                )
            else:
                display_value = str(value)[:80] + (
                    "..." if len(str(value)) > 80 else ""
                )
            return display_value, length_info

        for attr, value in sorted(self.__dict__.items()):
            display_value, length_info = format_value(value)
            lines.append(f"{attr}:\n{display_value}{length_info}")
        return "\n\n".join(lines)


analysis = MethylAnalysis(
    analysis_dir="~/mepylome/tutorial/tutorial_analysis",
    reference_dir="~/mepylome/tutorial/tutorial_reference",
)

analysis.cpgs = [1, 2, 3]

self = CacheManager(analysis)
self.set_dependencies("betas_dir", ["n_cpgs", "analysis_dir", "cpgs"])
self.set_value("betas_dir", 999)
self.get("betas_dir")

key = "betas_dir"
dependencies = ["n_cpgs", "analysis_dir", "cpgs"]

analysis.n_cpgs += 1
self.get("betas_dir")


@property
def betas_dir(self):
    if not cache_manager.get("betas_dir"):
        dependencies = ["analysis_dir", "prep", "output_dir"]
        betas_hash_key = input_args_id(
            self.analysis_dir,
            "betas",
            self.prep,
        )
        cache_manager.set("betas_dir", self.output_dir / f"{betas_hash_key}")
    return cache_manager.get("betas_dir")


class ExampleClass:
    def __init__(self):
        self.analysis_dir = "/data/analysis"
        self.prep = "default"
        self.output_dir = "/data/output"
        self.cache_manager = CacheManager(self)

    @property
    def betas_dir(self):
        dependencies = ["analysis_dir", "prep", "output_dir"]
        cached_value = self.cache_manager.get("betas_dir", dependencies)
        if cached_value is not None:
            return cached_value
        betas_hash_key = f"{self.analysis_dir}_{self.prep}"
        new_value = f"{self.output_dir}/{betas_hash_key}"
        self.cache_manager.cache("betas_dir", new_value)
        return new_value


# Example usage
example = ExampleClass()
print(example.betas_dir)  # Computes and caches the value
example.analysis_dir = "/new/analysis/path"  # Change a dependency
print(example.betas_dir)  # Recomputes since a dependency changed


def resolve_path(path_value):
    """Convert a path to absolute if it's relative."""
    if path_value is None:
        return INVALID_PATH
    return Path(path_value).expanduser


resolve_path("/adsf")

print("xy")

print("line0")
print("line1")


def stupidfunc(boo):
    """dd"""
    print("s")

    print("t")


self = MethylAnalysis(
    analysis_dir="~/mepylome/tutorial/tutorial_analysis",
    reference_dir="~/mepylome/tutorial/tutorial_reference",
)
self.set_betas()


# !pip install git+https://github.com/brj0/mepylome.git@dev psutil

# MEMORY LEAK
import gc
import os
import tracemalloc

import psutil

# import objgraph
# from pympler.tracker import SummaryTracker

tracemalloc.start()


def print_mem(msg=""):
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1024**2
    print(f"[{msg}] RSS Memory: {mem:.2f} MB")
    # gc.collect()
    # print("Top object types:")
    # for name, count in objgraph.most_common_types()[:10]:
    #     print(f"  {name:<30} {count}")


def print_snapshot_diff(snapshot1, snapshot2):
    top_stats = snapshot2.compare_to(snapshot1, "lineno")
    print("[ Top 10 differences ]")
    for stat in top_stats[:10]:
        print(stat)


print_mem("Start")

from mepylome import *
from mepylome.analysis import *
from mepylome.analysis.methyl_plots import write_cnv_to_disk

# snapshot_0 = tracemalloc.take_snapshot()

print_mem("Before init")

self = MethylAnalysis(
    analysis_dir="~/mepylome/data/salivary_gland_tumors/",
    reference_dir="~/mepylome/cnv_references/",
)

print_mem("After MethylAnalysis init")
# [After MethylAnalysis init] RSS Memory: 907.71 MB

# snapshot_1 = tracemalloc.take_snapshot()
# print_snapshot_diff(snapshot_0, snapshot_1)

self.set_betas()
print_mem("After set_betas")


self.make_umap()
print_mem("After make_umap")
# [After set_betas] RSS Memory: 3063.21 MB

# snapshot_2 = tracemalloc.take_snapshot()
# print_snapshot_diff(snapshot_1, snapshot_2)

ids = self.idat_handler.ids
ids = ids[:30]

write_cnv_to_disk(
    sample_path=[self.idat_handler.id_to_path[x] for x in ids],
    reference_dir=self.reference_dir,
    cnv_dir=self.cnv_dir,
    prep=self.prep,
    do_seg=self.do_seg,
    # n_cores=1,
)
# self.precompute_cnvs()

print_mem("After write_cnv_to_disk")
# [After write_cnv_to_disk] RSS Memory: 5323.46 MB

# snapshot_3 = tracemalloc.take_snapshot()
# print_snapshot_diff(snapshot_2, snapshot_3)

import mepylome

mepylome.clear_cache()

print_mem("After clean_cache")
# snapshot_4 = tracemalloc.take_snapshot()
# print_snapshot_diff(snapshot_3, snapshot_4)

self.idat_handler.selected_columns = ["Methylation class"]
clf_out_sg = self.classify(
    ids=ids,
    clf_list=[
        "none-kbest-et",
        "none-kbest-lr",
    ],
)

print_mem("After clf")
# snapshot_5 = tracemalloc.take_snapshot()
# print_snapshot_diff(snapshot_4, snapshot_5)

self.betas_all = None
self.betas_sel = None
gc.collect()

print_mem("After deleting betas")
# snapshot_6 = tracemalloc.take_snapshot()
# print_snapshot_diff(snapshot_5, snapshot_6)


# Final snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")
print("\nTop memory lines:")
for stat in top_stats[:20]:
    print(stat)


# Releases some memory
import ctypes

ctypes.CDLL("libc.so.6").malloc_trim(0)


import gc
import sys

import numpy as np
import pandas as pd

for obj in gc.get_objects():
    try:
        if isinstance(obj, pd.DataFrame):
            print(
                f"[DataFrame] shape={obj.shape}, memory={obj.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
            )
        elif isinstance(obj, np.ndarray):
            print(
                f"[ndarray] shape={obj.shape}, dtype={obj.dtype}, memory={obj.nbytes / 1024**2:.2f} MB"
            )
    except Exception:
        pass


for obj in gc.get_objects():
    try:
        size = sys.getsizeof(obj)
        if size > 10**6:
            print(f"{type(obj)} - {size / 1024**2:.2f} MB")
    except:
        pass

for obj in gc.get_objects():
    try:
        if isinstance(obj, pd.core.internals.blocks.Block):
            print(
                f"Block values: {obj.values.shape}, dtype={obj.dtype}, size={obj.values.nbytes / 1024**2:.2f} MB"
            )
    except:
        pass


print_mem("Before")

# self.betas_all = None
# self.betas_sel = None
# del self
print_mem("AFter")


import sys

sys.modules[__name__].__dict__.clear()


from multiprocessing import Pool, cpu_count

import psutil

num_cores = max(1, cpu_count() - 1)

mem_per_proc_gb = 4
available_gb = psutil.virtual_memory().available / (1024**3)
num_cores = max(1, min(os.cpu_count(), int(available_gb / mem_per_proc_gb)))


# import multiprocessing as mp
# mp.set_start_method("fork", force=True)


# pip install git+https://github.com/brj0/mepylome.git@dev psutil


# %% [markdown]
# ### Run Tutorial

# %%
import gc
import os
import tracemalloc
from pathlib import Path

import psutil

tracemalloc.start()


def print_mem(msg=""):
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1024**2
    print(f"[{msg}] RSS Memory: {mem:.2f} MB")


def print_snapshot_diff(snapshot1, snapshot2):
    top_stats = snapshot2.compare_to(snapshot1, "lineno")
    print("[ Top 10 differences ]")
    for stat in top_stats[:10]:
        print(stat)


print_mem("Start")
# [Start] RSS Memory: 18.77 MB

from pathlib import Path

from mepylome import clear_cache
from mepylome.analysis import MethylAnalysis
from mepylome.analysis.methyl_plots import write_cnv_to_disk
from mepylome.utils import setup_tutorial_files

snapshot_0 = tracemalloc.take_snapshot()

DIR = Path.home() / "mepylome" / "tutorial"
ANALYSIS_DIR = DIR / "tutorial_analysis"
REFERENCE_DIR = DIR / "tutorial_reference"

setup_tutorial_files(ANALYSIS_DIR, REFERENCE_DIR)

print_mem("Before init")
# [Before init] RSS Memory: 478.20 MB

self = MethylAnalysis(
    analysis_dir=ANALYSIS_DIR,
    reference_dir=REFERENCE_DIR,
    do_seg=True,
)

print_mem("After MethylAnalysis init")
# [After MethylAnalysis init] RSS Memory: 678.20 MB

snapshot_1 = tracemalloc.take_snapshot()
# print_snapshot_diff(snapshot_0, snapshot_1)

self.set_betas()
print_mem("After set_betas")
# [After set_betas] RSS Memory: 2705.72 MB

snapshot_2 = tracemalloc.take_snapshot()
# print_snapshot_diff(snapshot_1, snapshot_2)

ids = self.idat_handler.ids
ids = ids[:10]

write_cnv_to_disk(
    sample_path=[self.idat_handler.id_to_path[x] for x in ids],
    reference_dir=self.reference_dir,
    cnv_dir=self.cnv_dir,
    prep=self.prep,
    do_seg=self.do_seg,
    n_cores=1,
)

print_mem("After write_cnv_to_disk")
# [After write_cnv_to_disk] RSS Memory: 3761.93 MB

snapshot_3 = tracemalloc.take_snapshot()
print_snapshot_diff(snapshot_2, snapshot_3)

clear_cache()

print_mem("After clean_cache")
# [After clean_cache] RSS Memory: 3870.91 MB
# PARALLEL [After clean_cache] RSS Memory: 2898.22 MB

snapshot_4 = tracemalloc.take_snapshot()
# print_snapshot_diff(snapshot_3, snapshot_4)

# Final snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")
print("\nTop memory lines:")
for stat in top_stats[:20]:
    print(stat)


from mepylome import CNV, Annotation, ReferenceMethylData, clear_cache

clear_cache()

for file in Path(self.cnv_dir).glob("*"):
    if file.is_file():
        file.unlink()


###############
tracemalloc.start()
print_mem("Start")
snapshot0 = tracemalloc.take_snapshot()
###############

for id_ in self.idat_handler.ids[:5]:
    self.make_cnv_plot(id_)
# self.precompute_cnvs()

###############
print_mem("After CNV")
snapshot1 = tracemalloc.take_snapshot()
print_snapshot_diff(snapshot0, snapshot1)
###############

clear_cache()

###############
print_mem("After clear_cache")
snapshot2 = tracemalloc.take_snapshot()
print_snapshot_diff(snapshot1, snapshot2)
print_snapshot_diff(snapshot0, snapshot2)
###############

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")
print("\nTop memory lines:")
for stat in top_stats[:20]:
    print(stat)

tracemalloc.stop()


from mepylome import (
    CNV,
    Annotation,
    Manifest,
    MethylData,
    ReferenceMethylData,
    clear_cache,
)
from mepylome.analysis.methyl_plots import get_reference_methyl_data

for file in Path(self.cnv_dir).glob("*"):
    if file.is_file():
        file.unlink()


clear_cache()
###############
tracemalloc.start()
snapshot0 = tracemalloc.take_snapshot()
print_mem("Start")
###############

for path in self.idat_handler.paths[:5]:
    sample_methyl = MethylData(file=path)
    reference = get_reference_methyl_data(self.reference_dir, self.prep)
    cnv = CNV.set_all(sample_methyl, reference, do_seg=self.do_seg)
    del cnv
    del sample_methyl
    del reference

# self.precompute_cnvs()
# for i in range(10):
#     x = Manifest("epic")
#     del x
clear_cache()

###############
print_mem("After CNV")
snapshot1 = tracemalloc.take_snapshot()
print_snapshot_diff(snapshot0, snapshot1)
tracemalloc.stop()
###############




parse_component_key("rf(8,6,5,u=9,e=7,rt=98)")

make_clf_pipeline("SelectKBest-lr(max_iter=50)")


clf_out = analysis.classify(
    ids=ids,
    clf_list=[
        # Classifiers optimized for low-memory platforms (e.g. Google Colab)
        "TopVarianceSelector-SelectKBest-ExtraTreesClassifier",
        "TopVarianceSelector-SelectKBest-LogisticRegression(max_iter=10000)",
        "top-kbest-lr",
        "top-kbest-rf",
        # "vtl-kbest-et",
        # "vtl-kbest-lr",
        # "vtl-kbest-rf",
    ],
)

for x in components.values():
    print(x[1]().__class__.__name__)

clf = make_clf_pipeline(
    "vtl-kbest(k=10000)-svc"
)
clf.fit(X,y)

clf_out = self.classify(
    ids=self.idat_handler.ids,
    clf_list=[
        # Classifiers optimized for low-memory platforms (e.g. Google Colab)
        "vtl-kbest(k=10000)-svc"
        # "vtl-kbest-et",
        # "vtl-kbest-lr",
        # "vtl-kbest-rf",
    ],
)




