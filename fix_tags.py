import os
import glob
import re

template_dir = r"c:\Users\CRISTIAN\OneDrive\Escritorio\proyecto SafeZone (1)\proyecto SafeZone\proyecto SafeZone\safezone_app\templates\safezone_app"

count = 0
for filepath in glob.glob(os.path.join(template_dir, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Regex que busca el bloque roto
    pattern = re.compile(r'\{%\s*if message\.tags == \'error\'\s*%\}❌\{%\s*elif message\.tags == \'success\'\s*%\}✅\{%\s*elif message\.tags ==\s*[\n\r]*\s*\'warning\'\s*%\}⚠️\{%\s*else\s*%\}ℹ️\{%\s*endif\s*%\}', re.MULTILINE)
    replacement = "{% if message.tags == 'error' %}❌{% elif message.tags == 'success' %}✅{% elif message.tags == 'warning' %}⚠️{% else %}ℹ️{% endif %}"
    
    if pattern.search(content):
        new_content = pattern.sub(replacement, content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        count += 1
        print(f"Fixed: {os.path.basename(filepath)}")

print(f"Total fixed: {count}")
