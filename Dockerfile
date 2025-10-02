FROM python:3.13

WORKDIR /app

COPY src /app

RUN pip install uv

ENTRYPOINT ["uv", "run", "server_fastmcp_stdio.py"]
