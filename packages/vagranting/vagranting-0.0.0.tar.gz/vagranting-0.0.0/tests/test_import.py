#!/usr/bin/env python3
#region Imports
import os
import sys
import unittest

sys.path.insert(0, ".")
from vagrant_host import vagrantfile
#endregion

# Test class inheriting from unittest.TestCase
class TestVMFunction(unittest.TestCase):
  def test_two_vms_exist(self):
    vagrant_config = vagrantfile(cwd=os.path.dirname(__file__))
    self.assertEqual(len(vagrant_config.vms), 2)

  def test_vm_one_basecmd(self):
    vagrant_config = vagrantfile(cwd=os.path.dirname(__file__))
    with vagrant_config.load_vm("one") as vagrant:
        self.assertIsNotNone(vagrant)
        response = vagrant.exec_command("ls /")
        print(response)
        self.assertIsNotNone(response)
        self.assertIn("bin", response['stdout'])
        self.assertIn("boot", response['stdout'])

# Run the tests if the script is executed
if __name__ == '__main__':
  unittest.main()