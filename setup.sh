#!/bin/bash

mkdir -p ~/.streamlit/

echo "[server]
headless = true
port = $PORT
enableCORS = false
enableXsrfProtection = true
[logger]
level = 'warning'
" > ~/.streamlit/config.toml
