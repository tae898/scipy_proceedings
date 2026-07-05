# Generic benchmark image. Pin the package set via build ARG so each backend
# (arcadedb, duckdb, ladybug, chroma, faiss, ...) gets its own pinned image later.
# arcadedb-embedded bundles its own JRE, so no Java install is needed.
FROM python:3.12-slim

ARG PIP_PACKAGES="arcadedb-embedded>=26.8.1  # TODO: pin exact version once the perf-fix release (to_json_list, new_edges, run_in_transaction) is on PyPI numpy"
RUN if [ -n "${PIP_PACKAGES}" ]; then pip install --no-cache-dir ${PIP_PACKAGES}; fi

WORKDIR /work
# Scripts are mounted at run time (-v) so we can iterate without rebuilding.
CMD ["python", "--version"]
