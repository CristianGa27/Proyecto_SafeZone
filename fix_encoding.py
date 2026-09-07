import json

def fix_string(s):
    try:
        # Revert the CP850 -> UTF-16 misinterpretation
        # by encoding back to CP850 bytes, then decoding as CP1252 (original bytes)
        return s.encode('cp850').decode('cp1252')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If it fails, return the original string
        return s

def fix_data(data):
    if isinstance(data, dict):
        return {k: fix_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [fix_data(v) for v in data]
    elif isinstance(data, str):
        return fix_string(data)
    else:
        return data

def main():
    print("Leyendo backup_db.json...")
    with open('backup_db.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Corrigiendo codificación...")
    fixed_data = fix_data(data)
    
    print("Guardando backup_db.json...")
    with open('backup_db.json', 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)
    
    print("¡Listo!")

if __name__ == '__main__':
    main()
