#!/bin/bash

REQUIRED=(
  "PyQt6"
  "opencv-python"
  "fastapi"
  "uvicorn"
  "RPi.GPIO"
)

echo "🔍 Перевірка середовища Python..."

for pkg in "${REQUIRED[@]}"; do
  echo -n "📦 $pkg: "
  python3 -c "import ${pkg%%-*}" &>/dev/null && echo "✅ OK" || echo "❌ НЕ ВСТАНОВЛЕНО"
done

echo -e "\n📦 Щоб встановити все необхідне, виконай:"
echo -e "\n sudo raspi-config3 Interface Options->P8 GPIO->Enable"
echo "sudo apt install python3-pip python3-gpiozero python3-lgpio python3-rpi.gpio -y"
echo "pip install --break-system-packages PyQt6 opencv-python fastapi uvicorn RPi.GPIO"
