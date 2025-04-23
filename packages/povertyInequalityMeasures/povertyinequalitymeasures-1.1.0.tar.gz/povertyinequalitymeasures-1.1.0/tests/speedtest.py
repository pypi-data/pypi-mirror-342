import unittest
import pandas as pd
import numpy as np

from povertyInequalityMeasures import poverty, inequality

class TestPovertyMeasures(unittest.TestCase):
    def test_headline_poverty(self):
        """
        Test the headline poverty function
        """
        data = pd.DataFrame({'total_expenditure': np.random.randint(1000, size=(100000)), 'weight':np.ones(100000, dtype = int)})
        poverty_line= 125
        result = poverty.get_headcount_index(poverty_line, data, "total_expenditure","weight")
        print(result)

    def test_poverty_gap(self):
        """
        Test the poverty gap index function
        """
        data = pd.DataFrame({'total_expenditure': np.random.randint(1000, size=(100000)), 'weight':np.ones(100000, dtype = int)})
        poverty_line= 125
        result = poverty.get_poverty_gap_index(poverty_line, data, "total_expenditure","weight")
        print(result)
    
    def test_poverty_severity(self):
        """
        Test the poverty severity index function
        """
        data = pd.DataFrame({'total_expenditure': np.random.randint(1000, size=(100000)), 'weight':np.ones(100000, dtype = int)})
        poverty_line= 125
        result = poverty.get_poverty_severity_index(poverty_line, data, "total_expenditure","weight")
        print(result)

    def test_poverty_severity_generic_1(self):
        """
        Test the generic poverty severity index function
        """
        data = pd.DataFrame({'total_expenditure': np.random.randint(1000, size=(100000)), 'weight':np.ones(100000, dtype = int)})
        poverty_line= 125
        result = poverty.get_poverty_severity_index_generic(poverty_line, data, "total_expenditure","weight",0)
        print(result)
    
    def test_poverty_severity_generic_2(self):
        """
        Test the generic poverty severity index function
        """
        data = pd.DataFrame({'total_expenditure': np.random.randint(1000, size=(100000)), 'weight':np.ones(100000, dtype = int)})
        poverty_line= 125
        result = poverty.get_poverty_severity_index_generic(poverty_line, data, "total_expenditure","weight",1)
        print(result)

    def test_poverty_severity_generic_3(self):
        """
        Test the generic poverty severity index function
        """
        data = pd.DataFrame({'total_expenditure': np.random.randint(1000, size=(100000)), 'weight':np.ones(100000, dtype = int)})
        poverty_line= 125
        result = poverty.get_poverty_severity_index_generic(poverty_line, data, "total_expenditure","weight",2)
        print(result)

    def test_sen_index(self):
        """
        Test the sen index function
        """
        data = pd.DataFrame({'total_expenditure': np.random.randint(1000, size=(100000)), 'weight':np.ones(100000, dtype = int)})
        poverty_line= 125
        result = poverty.get_sen_index(poverty_line, data, "total_expenditure","weight")
        print(result)

    def test_watts_index(self):
        """
        Test the watts index function
        """
        data = pd.DataFrame({'total_expenditure': np.random.randint(1000, size=(100000)), 'weight':np.ones(100000, dtype = int)})
        poverty_line= 125
        result = poverty.get_watts_index(poverty_line, data, "total_expenditure","weight")
        print(result)

    # TODO def test_time_to_exit(self):
    def test_gini(self):
        """
        Test the gini coefficient function
        """
        data = pd.DataFrame({'total_expenditure': np.random.randint(1000, size=(100000)), 'weight':np.ones(100000, dtype = float)})
        result = inequality.get_gini(data, "total_expenditure","weight")
        print(result)
    
    def test_palma(self):
        """
        Test the Palma coefficient function
        """
        data = pd.DataFrame({'total_expenditure': np.ones((100000,), dtype=float), 'weight':np.ones((100000,), dtype=float)})
        result = inequality.get_palma(data, "total_expenditure","weight")
        print(result)

if __name__ == '__main__':
    unittest.main()