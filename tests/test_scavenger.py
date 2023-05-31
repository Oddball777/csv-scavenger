from calendar import c
import csv
import unittest
from unittest import mock

from scavenger import _determine_header_start_last, read_csv, _determine_format


class TestReadCSV(unittest.TestCase):
    def test_read_csv(self):
        result = read_csv("csv-scavenger/example_csvs/people.csv")
        self.assertEqual(result.shape, (1000, 9))

    def test_read_csv_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            read_csv("csv-scavenger/example_csvs/missing.csv")


class TestDetermineHeaderStartLast(unittest.TestCase):
    def test_determine_header_start_last(self):
        mock_lines = ["a,b,c\n", "1,2,3\n", "4,5,6\n", "7,8,9\n"]
        csv_format = (",", 3)
        result = _determine_header_start_last(csv_format, mock_lines)
        self.assertEqual(result, (0, 1, 4))

    def test_determine_header_with_noise_before_and_after(self):
        mock_lines = [
            "this file,",
            "a,b,c\n",
            "1,2,3\n",
            "4,5,6\n",
            "7,8,9\n",
            "a,b,c\n",
            "ka,sa,f,,f,f,,",
        ]
        csv_format = (",", 3)
        result = _determine_header_start_last(csv_format, mock_lines)
        self.assertEqual(result, (1, 2, 6))

    def test_determine_header_start_last_with_noise_before(self):
        mock_lines = ["this file,", "a,b,c\n", "1,2,3\n", "4,5,6\n", "7,8,9\n"]
        csv_format = (",", 3)
        result = _determine_header_start_last(csv_format, mock_lines)
        self.assertEqual(result, (1, 2, 5))

    def test_determine_header_start_last_with_noise_after(self):
        mock_lines = [
            "a,b,c\n",
            "1,2,3\n",
            "4,5,6\n",
            "7,8,9\n",
            "a,b,c\n",
            "ka,sa,f,,f,f,,",
        ]
        csv_format = (",", 3)
        result = _determine_header_start_last(csv_format, mock_lines)
        self.assertEqual(result, (0, 1, 5))

    def test_determine_header_start_last_just_one_line(self):
        mock_lines = ["a,b,c\n"]
        csv_format = (",", 3)
        result = _determine_header_start_last(csv_format, mock_lines)
        self.assertEqual(result, (0, 1, 1))

    def test_determine_header_start_last_just_one_line_plus_header(self):
        mock_lines = ["a,b,c\n", "1,2,3\n"]
        csv_format = (",", 3)
        result = _determine_header_start_last(csv_format, mock_lines)
        self.assertEqual(result, (0, 1, 2))


class TestDetermineFormat(unittest.TestCase):
    def test_determine_format(self):
        mock_lines = ["a,b,c\n", "1,2,3\n", "4,5,6\n", "7,8,9\n"]
        result = _determine_format(mock_lines)
        self.assertEqual(result, (",", 3))

    def test_determine_format_with_noise_before_and_after(self):
        mock_lines = [
            "this file,",
            "a,b,c\n",
            "1,2,3\n",
            "4,5,6\n",
            "7,8,9\n",
            "a,b,c\n",
            "ka,sa,f,,f,f,,",
        ]
        result = _determine_format(mock_lines)
        self.assertEqual(result, (",", 3))

    def test_determine_format_with_semicolon(self):
        mock_lines = ["a;b;c\n", "1;2;3\n", "4;5;6\n", "7;8;9\n"]
        result = _determine_format(mock_lines)
        self.assertEqual(result, (";", 3))

    def test_determine_format_with_tab(self):
        mock_lines = ["a\tb\tc\n", "1\t2\t3\n", "4\t5\t6\n", "7\t8\t9\n"]
        result = _determine_format(mock_lines)
        self.assertEqual(result, ("\t", 3))

    def test_determine_format_with_space(self):
        mock_lines = ["a b c\n", "1 2 3\n", "4 5 6\n", "7 8 9\n"]
        result = _determine_format(mock_lines)
        self.assertEqual(result, (" ", 3))

    def test_determine_format_with_newline(self):
        mock_lines = ["a\nb", "1\n2", "4\n5", "7\n8"]
        result = _determine_format(mock_lines)
        self.assertEqual(result, ("\n", 2))

    def test_determine_format_with_unknown_delimiter(self):
        mock_lines = ["a[b[c\n", "1[2[3\n", "4[5[6\n", "7[8[9\n"]
        with self.assertRaises(IndexError):
            _determine_format(mock_lines)

    def test_determine_format_with_different_number_of_columns(self):
        mock_lines = ["a,b,c\n", "1,2,3\n", "4,5,6\n", "7,8,9,10\n"]
        result = _determine_format(mock_lines)
        self.assertEqual(result, (",", 3))
