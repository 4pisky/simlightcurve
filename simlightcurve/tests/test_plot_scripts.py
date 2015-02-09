"""Check the syntax in example files is valid"""
from unittest import TestCase
import tempfile
import os
import sys


class TestExamples(TestCase):
    def setUp(self):
        # Run in a tempdir, in case the examples dump any output
        self.orig_dir = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

        repo_topdir = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__)))
        self.plots_dir = os.path.join(repo_topdir, 'docs', 'source', 'pyplots')
        sys.path.insert(0, self.plots_dir)

    def tearDown(self):
        os.chdir(self.orig_dir)
        sys.path.pop(0)

    def test_modsigmoid(self):
        import plot_modsigmoidexp

    def test_minishell(self):
        import plot_minishell

    def test_risedecay(self):
        import plot_risedecay

    def test_powerlaw(self):
        import plot_powerlaw