import os
import textual_pyfiglet_fonts

ext_fonts_pkg = os.path.dirname(textual_pyfiglet_fonts.__file__)

all_files = []
for root, dirs, files in os.walk(ext_fonts_pkg):
    for file in files:
        # Create relative path from package root
        rel_path = os.path.relpath(os.path.join(root, file), ext_fonts_pkg)
        all_files.append(rel_path)

all_files = sorted(all_files)

# write all_files out to a file:
with open("src/textual_pyfiglet_fonts/__init__.py", "w") as f:
    f.write(
        '"""Extended fonts package for Textual PyFiglet."""\n\n'
        'from typing import Literal \n\n'
    )
    f.write('ALL_FONTS = Literal[\n')
    for file in all_files:
        if file.endswith(".flf") or file.endswith(".tlf"):
            # remove the .txt extension
            font_name = file[:-4]
            f.write(f'"{font_name}",\n')
    f.write(']\n')