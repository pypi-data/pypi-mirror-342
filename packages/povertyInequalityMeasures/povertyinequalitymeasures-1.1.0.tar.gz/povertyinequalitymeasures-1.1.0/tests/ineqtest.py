import unittest
import pandas as pd
import numpy as np

from povertyInequalityMeasures import inequality

class TestPovertyMeasures(unittest.TestCase):
    def test_gini(self):
        """
        Test the gini coefficient function
        """
        data = pd.DataFrame({'total_expenditure': [7,10,15,18], 'weight':np.ones((4,), dtype=float)})
        result = inequality.get_gini(data, "total_expenditure","weight")
        self.assertEqual(result, 0.22)
    
    def test_palma(self):
        """
        Test the Palma coefficient function
        """
        data = pd.DataFrame({'total_expenditure': np.ones((10,), dtype=float), 'weight':np.ones((10,), dtype=float)})
        result = inequality.get_palma(data, "total_expenditure","weight")
        self.assertEqual(result, 0.25)

if __name__ == '__main__':
    unittest.main()