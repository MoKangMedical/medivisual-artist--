#!/bin/bash
echo "📊 MediVisual Artist — 医学可视化"
echo "================================="
python3 -m py_compile src/engine.py && echo "✅ engine.py"
mkdir -p output
echo "✅ 部署完成"
