#!/bin/bash
screen -dmS backend bash -c 'source venv/bin/activate && uvicorn server.gas:app --host 172.20.10.2 --port 8000'

