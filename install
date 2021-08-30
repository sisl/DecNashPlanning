#!/usr/bin/env sh

poetry install
julia -e "import Pkg; Pkg.instantiate(); Pkg.precompile();"
python -c "import julia; julia.install()"
