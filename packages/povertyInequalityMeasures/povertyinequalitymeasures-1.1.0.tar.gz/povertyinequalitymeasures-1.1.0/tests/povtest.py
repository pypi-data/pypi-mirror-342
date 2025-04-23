import unittest
import pandas as pd

from povertyInequalityMeasures import poverty


class TestPovertyMeasures(unittest.TestCase):
    def test_headline_poverty(self):
        """
        Test the headline poverty function
        """
        data = pd.DataFrame({'total_expenditure': [ 110,120,150,160], 'weight':[1,1,1,1]})
        poverty_line= 125
        result = poverty.get_headcount_index(poverty_line, data, "total_expenditure","weight")
        self.assertEqual(result, 0.5)

    def test_poverty_gap(self):
        """
        Test the poverty gap index function
        """
        data = pd.DataFrame({'total_expenditure': [ 100,110,150,160], 'weight':[1,1,1,1]})
        poverty_line= 125
        result = poverty.get_poverty_gap_index(poverty_line, data, "total_expenditure","weight")
        self.assertEqual(result, 0.08)
    
    def test_poverty_severity(self):
      """
      Test the poverty severity index function
      """
      data = pd.DataFrame({'total_expenditure': [ 100,110,150,160], 'weight':[1,1,1,1]})
      poverty_line= 125
      result = poverty.get_poverty_severity_index(poverty_line, data, "total_expenditure","weight")
      self.assertEqual(result, 0.0136)

    def test_poverty_severity_generic_1(self):
        """
        Test the generic poverty severity index function
        """
        data = pd.DataFrame({'total_expenditure': [ 100,110,150,160], 'weight':[1,1,1,1]})
        poverty_line= 125
        result = poverty.get_poverty_severity_index_generic(poverty_line, data, "total_expenditure","weight",0)
        self.assertEqual(result, 0.5)

    def test_poverty_severity_generic_2(self):
        """
        Test the generic poverty severity index function
        """
        data = pd.DataFrame({'total_expenditure': [ 100,110,150,160], 'weight':[1,1,1,1]})
        poverty_line= 125
        result = poverty.get_poverty_severity_index_generic(poverty_line, data, "total_expenditure","weight",1)
        self.assertEqual(result, 0.08)

    def test_poverty_severity_generic_3(self):
        """
        Test the generic poverty severity index function
        """
        data = pd.DataFrame({'total_expenditure': [ 100,110,150,160], 'weight':[1,1,1,1]})
        poverty_line= 125
        result = poverty.get_poverty_severity_index_generic(poverty_line, data, "total_expenditure","weight",2)
        self.assertEqual(result, 0.0136)

    def test_sen_index(self):
        """
        Test the sen index function
        """
        data = pd.DataFrame({'total_expenditure': [ 100,110,150,160], 'weight':[1,1,1,1]})
        poverty_line= 125
        result = poverty.get_sen_index(poverty_line, data, "total_expenditure","weight")
        self.assertEqual(result, 0.143)

    def test_watts_index(self):
        """
        Test the watts index function
        """
        data = pd.DataFrame({'total_expenditure': [ 100,110,150,160], 'weight':[1,1,1,1]})
        poverty_line= 125
        result = poverty.get_watts_index(poverty_line, data, "total_expenditure","weight")
        self.assertEqual(result, 0.08774)

    # TODO def test_time_to_exit(self):

if __name__ == '__main__':
    unittest.main()