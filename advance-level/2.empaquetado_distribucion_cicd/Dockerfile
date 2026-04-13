# ─────────────────────────────────────────────
#  Stage 1 – builder: build the wheel
# ─────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# pip-build is the lightweight PEP 517 frontend
RUN pip install --no-cache-dir build

# Copy only the files needed to build the package
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Produce the wheel in /app/dist/
RUN python -m build --wheel --outdir dist/

# ─────────────────────────────────────────────
#  Stage 2 – runtime: lean production image
# ─────────────────────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app

# Non-root user for safety
RUN addgroup --system appgroup \
 && adduser  --system --ingroup appgroup appuser

# Copy only the built wheel from the builder stage
COPY --from=builder /app/dist/*.whl ./

# Install the wheel (fastapi + uvicorn are pulled in as dependencies)
RUN pip install --no-cache-dir *.whl \
 && rm -f *.whl

USER appuser

EXPOSE 8000

CMD ["uvicorn", "empaquetado_distribucion_cicd.main:app", "--host", "0.0.0.0", "--port", "8000"]
