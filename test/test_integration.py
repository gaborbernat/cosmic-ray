import builtins
import os
import shutil
import subprocess
from unittest import mock

import pytest

from cosmic_ray.cli import main
from cosmic_ray.commands.format import survival_rate

TEST_PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir,
                                                'test_project'))


@pytest.mark.parametrize('config', ["unittest.dist",
                                    "unittest.local",
                                    "pytest.dist",
                                    "pytest.local",
                                    "nosetest.dist",
                                    "nosetest.dist"])
def test_outcome(monkeypatch, config, tmpdir, capfd):
    session = 'adam_tests.{}'.format(config)
    conf_file = 'cosmic-ray.{}.conf'.format(config)

    test_dir = os.path.join(tmpdir, 'test')
    shutil.copytree(TEST_PROJECT_DIR, test_dir,
                    ignore=shutil.ignore_patterns('*.conf'))
    shutil.copy(os.path.join(TEST_PROJECT_DIR, conf_file),
                os.path.join(test_dir, conf_file))
    monkeypatch.chdir(test_dir)
    try:
        main(argv=['init', conf_file, session])
    except subprocess.CalledProcessError:
        pass
    out, err = capfd.readouterr()

    main(argv=['exec', session])
    out, err = capfd.readouterr()

    with mock.patch.object(builtins, 'input', lambda: out):
        survival_rate()
