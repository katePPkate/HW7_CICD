#!/usr/bin/env python3
"""Скрипт для переключения весов Canary стратегии"""

import os
import subprocess

def switch_weight(weight):
    """Переключение конфига Nginx"""
    config_map = {
        10: "nginx/nginx.10.conf",
        50: "nginx/nginx.50.conf",
        0: "nginx/nginx.rollback.conf"
    }
    
    if weight not in config_map:
        print("Доступные веса: 10 (canary 10%), 50 (50/50), 0 (rollback на stable)")
        return False
    
    config_file = config_map[weight]
    
    # Копируем конфиг в рабочую папку Nginx
    os.system(f"cp {config_file} nginx/nginx.conf")
    
    # Перезагружаем Nginx
    result = subprocess.run(["docker", "exec", "nginx_canary", "nginx", "-s", "reload"], 
                           capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Веса изменены: canary получает {weight}% трафика")
        return True
    else:
        print(f"❌ Ошибка: {result.stderr}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        switch_weight(int(sys.argv[1]))
    else:
        print("Использование: python switch_weight.py [10|50|0]")
        print("  10 - 90/10 (начало канарейки)")
        print("  50 - 50/50 (увеличение трафика)")
        print("  0  - 100/0 (полный откат на stable)")
