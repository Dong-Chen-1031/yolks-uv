#!/usr/bin/env python3
"""
Egg Generator (hen.py)
自動從 hens/ 模板和 .sh 腳本生成完整的 egg JSON
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone


def load_template(template_path: Path) -> dict:
    """載入 egg 模板 JSON"""
    with template_path.open('r', encoding='utf-8') as f:
        return json.load(f)


def load_script(script_path: Path) -> str:
    """載入 shell 腳本內容"""
    with script_path.open('r', encoding='utf-8') as f:
        return f.read()


def escape_for_json(script: str, format_type: str) -> str:
    """
    轉義 script 內容以便嵌入 JSON
    
    Args:
        script: shell 腳本內容
        format_type: 'pelican' 或 'pterodactyl'
    """
    if format_type == 'pelican':
        # Pelican (PLCN_v3) 使用正常的 JSON 轉義
        return script
    else:
        # Pterodactyl (PTDL_v2) 需要 \r\n 和反斜線轉義
        return script.replace('\\', '\\\\').replace('\n', '\\r\\n').replace('"', '\\"')


def generate_egg(template_path: Path, install_script: Path, start_script: Path, output_path: Path):
    """
    生成 egg JSON 檔案
    
    Args:
        template_path: egg 模板路徑
        install_script: 安裝腳本路徑 (.sh)
        start_script: 啟動腳本路徑 (.sh)
        output_path: 輸出 egg JSON 路徑
    """
    print(f"📖 Loading template: {template_path.name}")
    egg = load_template(template_path)
    
    print(f"📖 Loading install script: {install_script.name}")
    install_content = load_script(install_script)
    
    print(f"📖 Loading start script: {start_script.name}")
    start_content = load_script(start_script)
    
    # 偵測格式類型
    format_type = 'pelican' if egg['meta']['version'] == 'PLCN_v3' else 'pterodactyl'
    print(f"🔍 Detected format: {format_type.upper()}")
    
    # 更新時間戳
    egg['exported_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    # 注入安裝腳本
    escaped_install = escape_for_json(install_content, format_type)
    egg['scripts']['installation']['script'] = escaped_install
    
    # 注入啟動腳本
    if format_type == 'pelican':
        # Pelican 使用 startup_commands.Default
        egg['startup_commands']['Default'] = start_content.strip()
    else:
        # Pterodactyl 使用 startup
        # Pterodactyl 的 startup 需要轉義內部的引號
        escaped_start = start_content.strip().replace('"', '\\"')
        egg['startup'] = escaped_start
    
    # 寫出檔案
    print(f"💾 Writing egg: {output_path}")
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(egg, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Successfully generated: {output_path.name}")


def main():
    script_dir = Path(__file__).parent
    hens_dir = script_dir / 'hens'
    output_dir = script_dir.parent / 'egg'
    
    # 確保輸出目錄存在
    output_dir.mkdir(exist_ok=True)
    
    # 腳本路徑
    install_script = script_dir / 'install.sh'
    start_script = script_dir / 'start.sh'
    
    if not install_script.exists():
        print(f"❌ Error: {install_script} not found")
        sys.exit(1)
    
    if not start_script.exists():
        print(f"❌ Error: {start_script} not found")
        sys.exit(1)
    
    # 找到所有模板
    templates = list(hens_dir.glob('*.json'))
    
    if not templates:
        print(f"❌ Error: No egg templates found in {hens_dir}")
        sys.exit(1)
    
    print(f"\n🐔 Hen - Egg Generator")
    print(f"═" * 50)
    print(f"Found {len(templates)} template(s)\n")
    
    # 處理每個模板
    for template in templates:
        output_file = output_dir / template.name
        
        try:
            generate_egg(template, install_script, start_script, output_file)
            print()
        except Exception as e:
            print(f"❌ Error generating {template.name}: {e}")
            sys.exit(1)
    
    print(f"═" * 50)
    print(f"🎉 All eggs generated successfully!")


if __name__ == '__main__':
    main()
