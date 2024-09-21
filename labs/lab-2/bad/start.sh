#!/bin/sh
cd /app/frontend && nohup python3 server.py &
cd /app/backend && python3 server.py
