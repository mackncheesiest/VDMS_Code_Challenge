#! python

#Thanks to https://docs.python.org/2/library/unittest.html
import unittest

"""
    I don't fully know how the __init__.py files work, so it looks like I'm
    just going to do this in a not-very-optimal way for now, but at least it's
    better than requiring an absolute path and making the code completely not
    portable between machines
"""
import os, sys
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

from netaddr import IPAddress
from IP_Range import enumerated_ip_range

class Test_IP_Range(unittest.TestCase):

    #When given nothing, test that it returns an empty list
    def test_enumeratedIPRange_both_empty(self):
        out = enumerated_ip_range('', [])
        self.assertEqual([], out)
        
    #Test that when given an empty range and non-empty exclusion list, 
    #it returns an empty list
    def test_enumeratedIPRange_CIDRRange_empty(self):
        out = enumerated_ip_range('', ['192.168.1.1'])
        self.assertEqual([], out)
        
    #Test that when the type doesn't match for both arguments, it returns an empty list
    def test_enumeratedIPRange_incorrect_types(self):
        out = enumerated_ip_range(123, 1283432)
        self.assertEqual([], out)
        
    #Test that when given a non-empty range and empty exclusion list,
    #it returns a fully enumerated list
    def test_enumeratedIPRange_ExclusionList_empty(self):
        out = enumerated_ip_range('192.168.1.0/28', [])
        expected = [IPAddress('192.168.1.0'), IPAddress('192.168.1.1'), IPAddress('192.168.1.2'), IPAddress('192.168.1.3'),
                    IPAddress('192.168.1.4'), IPAddress('192.168.1.5'), IPAddress('192.168.1.6'), IPAddress('192.168.1.7'),
                    IPAddress('192.168.1.8'), IPAddress('192.168.1.9'), IPAddress('192.168.1.10'), IPAddress('192.168.1.11'),
                    IPAddress('192.168.1.12'), IPAddress('192.168.1.13'), IPAddress('192.168.1.14'), IPAddress('192.168.1.15')]
        self.assertEqual(expected, out)
    
    #Test that when given a non-empty range and exclusion list with a mix of IPs
    #that are and aren't included in that range, it only removes the ones that are present
    #to begin with
    def test_enumeratedIPRange_full_test(self):
        out = enumerated_ip_range('192.168.1.0/28', ['192.168.1.3', '111.111.222.2', '192.168.1.12'])
        expected = [IPAddress('192.168.1.0'), IPAddress('192.168.1.1'), IPAddress('192.168.1.2'), IPAddress('192.168.1.4'), 
                    IPAddress('192.168.1.5'), IPAddress('192.168.1.6'), IPAddress('192.168.1.7'), IPAddress('192.168.1.8'), 
                    IPAddress('192.168.1.9'), IPAddress('192.168.1.10'), IPAddress('192.168.1.11'), IPAddress('192.168.1.13'), 
                    IPAddress('192.168.1.14'), IPAddress('192.168.1.15')]
        self.assertEqual(expected, out)
    
if __name__ == '__main__':
    unittest.main()