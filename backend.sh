#!/bin/bash
screen -dmS backend bash -c 'source venv/bin/activate && uvicorn server.sensor_data:app --host 172.20.10.2 --port 8000'

