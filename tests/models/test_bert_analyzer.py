import unittest
from unittest.mock import patch

from models.bert_analyzer import BertAnalyzer


class TestBertAnalyzer(unittest.TestCase):
    def setUp(self):
        # Set up an instance of BertAnalyzer
        self.analyzer = BertAnalyzer()

    def test_generate_personal_summaries_empty(self):
        print("in test_generate_personal_summaries_empty")
        self.assertEqual(
            self.analyzer.generate_personal_summaries({}, {}),
            {},
            "Should return an empty dictionary when no data is provided."
        )

    def test_generate_personal_summaries_valid(self):
        # Assuming a simplified data structure for the test
        commit_types_per_user = {'Alice': {'Corrective': 2, 'Adaptive': 1, 'Perfective': 0, 'Administrative': 0, 'Other': 0}}
        detailed_contributions = {
            'Alice': {'Corrective': {'Source Code': 3, 'Configuration': 1, 'Tests': 0, 'Documentation': 0, 'Resources': 0}, 'Adaptive': {'Tests': 1, 'Documentation': 2}}
        }
        expected_result = {
            'Alice': 'Alice has mostly done Corrective commits, with 2 commits. These have primarily been done in Source Code files. '
                     'Then, 1 Adaptive commit has mostly been done in Documentation files. '
                     'However, Alice has not done any Perfective, Administrative, Other commits.'
        }
        self.assertEqual(
            self.analyzer.generate_personal_summaries(commit_types_per_user, detailed_contributions),
            expected_result,
            "Should match the expected summary output."
        )

    def test_generate_overall_summaries(self):
        commit_types_in_project = {'Adaptive': 10, 'Corrective': 9, 'Perfective': 8, 'Administrative': 7, 'Documentation': 0}
        detailed_contributions_in_project = {'Adaptive': {'Source Code': 5, 'Configuration': 4, 'Tests': 3, 'Documentation': 2, 'Resources': 0},
                                             'Corrective': {'Source Code': 4, 'Configuration': 5, 'Tests': 3, 'Documentation': 2, 'Resources': 0},
                                             'Perfective': {'Source Code': 5, 'Configuration': 4, 'Tests': 3, 'Documentation': 2, 'Resources': 0},
                                             'Administrative': {'Source Code': 5, 'Configuration': 4, 'Tests': 3, 'Documentation': 2, 'Resources': 0},
                                             'Documentation': {'Source Code': 0, 'Configuration': 0, 'Tests': 0, 'Documentation': 0, 'Resources': 0}}
        expected_result = 'In this project, Adaptive commits have been the most frequent, with 10 commits. These have primarily been done in Source Code files. Then, 9 Corrective commits have mostly been done in Configuration files,  8 Perfective commits have mainly been done in Source Code files, and 7 Administrative commits have primarily been done in Source Code files. However, no Documentation commits have been done in this project'
        self.assertEqual(
            self.analyzer.generate_project_summaries(commit_types_in_project, detailed_contributions_in_project),
            expected_result,
            "Should match the expected summary output."
        )

    def test_get_total_what(self):
        commits_dict = {
            'Alice': [
                ('Fixed a bug', ['src/file1.java']),
                ('Added a new feature', ['src/file2.java']),
                ('Refactored some tests', ['tests/Test.java'])
            ],
            'Bob': [
                ('Renamed some packages', ['src/file3.java']),
                ('Update README.md', ['doc/README.md']),
                ('blabla', ['resources/image.png'])
            ]
        }

        # Expected results for tests
        expected_commit_types = {'Corrective': 1, 'Adaptive': 1, 'Perfective': 2, 'Administrative': 1, 'Other': 1}
        expected_file_types = {'Source Code': 3, 'Tests': 1, 'Documentation': 1, 'Resources': 1, 'Configuration': 0}

        # Call analyze_commits
        self.analyzer.analyze_commits(commits_dict)

        # Verify the internal state is as expected
        self.assertEqual(self.analyzer.get_total_what(), expected_commit_types)
        self.assertEqual(self.analyzer.get_total_where(), expected_file_types)

        # Test get_total_what
        result_what = self.analyzer.get_total_what()
        self.assertEqual(result_what, expected_commit_types)

        # Test get_total_where
        result_where = self.analyzer.get_total_where()
        self.assertEqual(result_where, expected_file_types)

    def test_get_total_where(self):
        commits_dict = {
            'Alice': [
                ('Fixed a bug', ['src/file1.java']),
                ('Added a new feature', ['src/file2.java']),
                ('Refactored some tests', ['tests/Test.java'])
            ],
            'Bob': [
                ('Renamed some packages', ['src/file3.java']),
                ('Update README.md', ['doc/README.md']),
                ('blabla', ['resources/image.png'])
            ]
        }

        expected_file_types = {'Source Code': 3, 'Tests': 1, 'Documentation': 1, 'Resources': 1, 'Configuration': 0}
        self.analyzer.analyze_commits(commits_dict)
        self.assertEqual(self.analyzer.get_total_where(), expected_file_types)

        # Test get_total_where
        result_where = self.analyzer.get_total_where()
        self.assertEqual(result_where, expected_file_types)


    #### 2. Test `analyze_commits` Method
# **Simulate Input**: Pass a sample dictionary mimicking the expected input format and test for correct processing.
# **Check State Reset**: Ensure that `reset_for_new_repository` is called before analyzing new commits to avoid data leakage between tests.

    def test_analyze_commits_reset_called(self):
        # You'll need to patch the reset_for_new_repository method to check if it's called
        with patch.object(self.analyzer, 'reset_for_new_repository') as mocked_reset:
            self.analyzer.analyze_commits({})
            mocked_reset.assert_called_once()