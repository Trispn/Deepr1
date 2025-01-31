# Copyright 2025 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Adapted from huggingface/transformers: https://github.com/huggingface/transformers/blob/21a2d900eceeded7be9edc445b56877b95eda4ca/setup.py


import re
import shutil
from pathlib import Path

from setuptools import find_packages, setup


# Remove stale open_r1.egg-info directory to avoid https://github.com/pypa/pip/issues/5466
stale_egg_info = Path(__file__).parent / "open_r1.egg-info"
if stale_egg_info.exists():
    print(
        (
            "Warning: {} exists.\n\n"
            "If you recently updated open_r1, this is expected,\n"
            "but it may prevent open_r1 from installing in editable mode.\n\n"
            "This directory is automatically generated by Python's packaging tools.\n"
            "I will remove it now.\n\n"
            "See https://github.com/pypa/pip/issues/5466 for details.\n"
        ).format(stale_egg_info)
    )
    shutil.rmtree(stale_egg_info)


# IMPORTANT: all dependencies should be listed here with their version requirements, if any.
#   * If a dependency is fast-moving (e.g. transformers), pin to the exact version
_deps = [
    "accelerate>=1.2.1",
    "bitsandbytes>=0.43.0",
    "black>=24.4.2",
    "datasets>=3.2.0",
    "deepspeed==0.15.4",
    "distilabel[vllm,ray,openai]>=1.5.2",
    "einops>=0.8.0",
    "flake8>=6.0.0",
    "hf_transfer>=0.1.4",
    "huggingface-hub[cli]>=0.19.2,<1.0",
    "isort>=5.12.0",
    "liger_kernel==0.5.2",
    "lighteval @ git+https://github.com/huggingface/lighteval.git@0e462692436e1f0575bdb4c6ef63453ad9bde7d4#egg=lighteval[math]",
    "math-verify>=0.3.3",  # Used for math verification in grpo
    "packaging>=23.0",
    "parameterized>=0.9.0",
    "pytest",
    "safetensors>=0.3.3",
    "sentencepiece>=0.1.99",
    "torch>=2.5.1",
    "transformers @ git+https://github.com/huggingface/transformers.git@main",
    "trl @ git+https://github.com/huggingface/trl.git@main",
    "vllm>=0.7.0",
    "wandb>=0.19.1",
]

# this is a lookup table with items like:
#
# tokenizers: "tokenizers==0.9.4"
# packaging: "packaging"
#
# some of the values are versioned whereas others aren't.
deps = {b: a for a, b in (re.findall(r"^(([^!=<>~ \[\]]+)(?:\[[^\]]+\])?(?:[!=<>~ ].*)?$)", x)[0] for x in _deps)}


def deps_list(*pkgs):
    return [deps[pkg] for pkg in pkgs]


extras = {}
extras["tests"] = deps_list("pytest", "parameterized")
extras["torch"] = deps_list("torch")
extras["quality"] = deps_list("ruff", "isort", "flake8")
extras["eval"] = deps_list("lighteval", "math-verify")
extras["dev"] = extras["quality"] + extras["tests"] + extras["eval"]

# core dependencies shared across the whole project - keep this to a bare minimum :)
install_requires = [
    deps["accelerate"],
    deps["bitsandbytes"],
    deps["einops"],
    deps["datasets"],
    deps["deepspeed"],
    deps["hf_transfer"],
    deps["huggingface-hub"],
    deps["liger_kernel"],
    deps["packaging"],  # utilities from PyPA to e.g., compare versions
    deps["safetensors"],
    deps["sentencepiece"],
    deps["transformers"],
    deps["trl"],
]

setup(
    name="open-r1",
    version="0.1.0.dev0",  # expected format is one of x.y.z.dev0, or x.y.z.rc1 or x.y.z (no to dashes, yes to dots)
    author="The Hugging Face team (past and future)",
    author_email="lewis@huggingface.co",
    description="Open R1",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="llm inference-time compute reasoning",
    license="Apache",
    url="https://github.com/huggingface/open-r1",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    extras_require=extras,
    python_requires=">=3.10.9",
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
