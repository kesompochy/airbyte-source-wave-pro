
FROM airbyte/python-connector-base:1.1.0

WORKDIR /airbyte/integration_code
COPY pyproject.toml poetry.lock ./
COPY main.py ./
COPY airbyte_source_wave_pro/ ./airbyte_source_wave_pro/
COPY metadata.yaml ./
COPY README.md ./
RUN pip install .

ENV AIRBYTE_ENTRYPOINT "python /airbyte/integration_code/main.py"
ENTRYPOINT ["python", "/airbyte/integration_code/main.py"]
