#!/bin/bash

echo "🚀 Starte Prefect Setup..."

# 1️⃣ Prefect API URL setzen
export PREFECT_API_URL=http://127.0.0.1:4200/api
echo "✅ PREFECT_API_URL gesetzt: $PREFECT_API_URL"

# 2️⃣ Prefect Server Hinweis
echo "ℹ️ Prefect Server muss laufen! Starte in einem anderen Terminal mit:"
echo "   prefect server start"
echo ""

# 3️⃣ Deployment erstellen (fragt nach Work Pool & Optionen)
echo "📦 Erstelle neues Deployment für 'weather_etl_flow.py'..."
prefect deploy weather_etl_flow.py:weather_etl_flow -n "Weather Flow"

# 4️⃣ Worker starten (Work Pool wird aus Deployment genommen)
echo ""
echo "✅ Deployment erstellt! Jetzt Worker starten mit:"
echo "   export PREFECT_API_URL=http://127.0.0.1:4200/api"
echo "   prefect worker start --pool pool_weather_data"
echo ""
echo "🎯 Danach im Prefect Dashboard unter Deployments → 'Weather Flow' → Run klicken."
