#!/bin/bash
screen -dmS backend bash -c 'source venv/bin/activate && uvicorn server.gas:app --host 192.168.0.245 --port 8000'

