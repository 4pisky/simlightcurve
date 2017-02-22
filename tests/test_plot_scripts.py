# """Check the syntax in example files is valid"""
# import os
# import sys
# import tempfile
# from unittest import TestCase
#
#
# class TestExamples(TestCase):
#     def setUp(self):
#         # Run in a tempdir, in case the examples dump any output
#         self.orig_dir = os.getcwd()
#         self.tempdir = tempfile.mkdtemp()
#         os.chdir(self.tempdir)
#
#         repo_topdir = os.path.dirname(
#             os.path.dirname(os.path.dirname(__file__)))
#         self.plots_dir = os.path.join(repo_topdir, 'docs', 'source', 'pyplots')
#         sys.path.insert(0, self.plots_dir)
#
#     def tearDown(self):
#         os.chdir(self.orig_dir)
#         sys.path.pop(0)
#
#     def test_modsigmoid(self):
#         pass
#
#     def test_minishell(self):
#         pass
#
#     def test_risedecay(self):
#         pass
#
#     def test_powerlaw(self):
#         pass