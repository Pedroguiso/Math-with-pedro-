import zipfile
from pathlib import Path

_original_extractall = zipfile.ZipFile.extractall

def _patched_extractall(self, path=None, members=None, pwd=None):
    result = _original_extractall(self, path=path, members=members, pwd=pwd)
    if path:
        root = Path(path) / "math-with-pedro-deploy-v17"
        replacements = {
            root / "index.html": ('alt="UCF logo" loading="lazy"/>', 'alt="UCF logo" referrerpolicy="no-referrer" loading="eager"/>'),
            root / "pt" / "index.html": ('alt="Logo da UCF" loading="lazy"/>', 'alt="Logo da UCF" referrerpolicy="no-referrer" loading="eager"/>'),
        }
        for file_path, (old, new) in replacements.items():
            if file_path.exists():
                text = file_path.read_text(encoding="utf-8")
                if old in text:
                    file_path.write_text(text.replace(old, new), encoding="utf-8")
    return result

zipfile.ZipFile.extractall = _patched_extractall
