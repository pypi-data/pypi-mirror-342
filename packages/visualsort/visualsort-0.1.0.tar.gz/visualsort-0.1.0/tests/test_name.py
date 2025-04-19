import pytest
import pytest_mock
from visualsort import swap, compare

nums = [3, 2, 1]  

def test_swap(mocker):
  global nums
  
  mocker.patch("name.add_clip")
  mocker.patch("name.reset_colors")
  
  swap(0, 1, nums)
  assert nums == [2, 3, 1]
  
  swap(1, 2, nums)
  assert nums == [2, 1, 3]
  
def test_compare(mocker):
  global nums
  
  mocker.patch("name.assign_color")
  
  assert compare(0, 1, nums) == True
  assert compare(1, 0, nums) == False
  assert compare(0, 0, nums) == False
    