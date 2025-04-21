import pytest  # type: ignore
from pathlib import Path
import runpy

demos = (Path(__file__ ).parent.parent / 'demos').glob('*.py')

@pytest.mark.parametrize('demo', demos)
def test_script_execution(demo):
    runpy.run_path(str(demo))