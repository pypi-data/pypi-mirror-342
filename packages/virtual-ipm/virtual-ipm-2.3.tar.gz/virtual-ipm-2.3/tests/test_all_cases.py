from pathlib import Path
from subprocess import run, DEVNULL

import pytest


CASES_DIR = Path('cases')
TMP_CONFIG = CASES_DIR / '_tmp.xml'


@pytest.mark.parametrize('f_path', list(CASES_DIR.glob('*.xml')))
def test_case(f_path, read_template):
    TMP_CONFIG.write_text(read_template(f_path))
    try:
        run(['virtual-ipm', str(TMP_CONFIG.resolve())], check=True, stdout=DEVNULL, cwd=CASES_DIR)
    finally:
        TMP_CONFIG.unlink()
