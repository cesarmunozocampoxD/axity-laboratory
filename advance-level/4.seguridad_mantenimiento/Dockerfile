# =============================================================================
# Multi-stage build — hardened container (no root, minimal attack surface)
# =============================================================================

# ---- Stage 1: build the wheel -----------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# Only install the build frontend; PEP 517 pulls poetry-core automatically
RUN pip install --no-cache-dir build==1.2.2

# Copy only what is needed to build the package
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Produce a wheel in /dist
RUN python -m build --wheel --outdir /dist

# =============================================================================
# ---- Stage 2: minimal runtime image -----------------------------------------
# =============================================================================
FROM python:3.12-slim AS runtime

# -------------------------------------------------------------------
# Security: create a dedicated non-root user and group.
# --no-create-home and /usr/sbin/nologin reduce attack surface.
# -------------------------------------------------------------------
RUN groupadd --gid 1001 appgroup \
 && useradd  --uid 1001 \
             --gid 1001 \
             --no-create-home \
             --shell /usr/sbin/nologin \
             appuser

WORKDIR /app

# Copy and install the wheel; then remove it to keep the layer clean
COPY --from=builder /dist/*.whl ./
RUN pip install --no-cache-dir *.whl \
 && rm -f *.whl

# Give ownership to appuser *before* dropping privileges
RUN chown -R appuser:appgroup /app

# -------------------------------------------------------------------
# Security: drop to non-root for all subsequent instructions and RUN
# -------------------------------------------------------------------
USER appuser

# Non-secret runtime configuration (secrets should be injected at
# deploy time via orchestrator secrets — not here)
ENV APP_NAME=seguridad-mantenimiento \
    DEBUG=false \
    PORT=8000

EXPOSE 8000

CMD ["python", "-m", "seguridad_mantenimiento.app"]
