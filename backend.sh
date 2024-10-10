#!/bin/bash
screen -dmS backend source venv/bin/activate && uvicorn backend.gas:app --host 192.168.0.245 --port 8000
