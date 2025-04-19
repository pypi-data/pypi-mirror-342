from .util.module import *
from collections.abc import Callable
from moviepy.editor import *

def compare(a: int, b: int, nums: list) -> bool:
  """
  Compares two numbers and updates the current frame.
  
  :param a (int): The index of the first number in the array.
  :type a: int
  :param b (int): The index of the second number in the array.
  :type b: int
  :param nums (list): The array of numbers.
  :type nums: list
  :return: True if the first number is greater than the second number, False otherwise.
  :rtype: bool
  :raises IndexError: If either of the indices is out of bounds.
  """
  if(a < 0 or a >= len(nums) or b < 0 or b >= len(nums)):
    raise IndexError("Index out of bounds.")
  
  assign_color(a, "green")
  assign_color(b, "red")
  return nums[a] > nums[b]

def swap(a: int, b: int, nums: list) -> list:
  """
  Swaps two numbers and updates the current frame.

  
  :param a (int): The index of the first number in the array.
  :type a: int
  :param b (int): The index of the second number in the array.
  :type b: int
  :param nums (list): The array of numbers.
  :type nums: list
  :return: The array of numbers after the swap.
  :rtype: list
  :raises IndexError: If either of the indices is out of bounds.
  """
  if(a < 0 or a >= len(nums) or b < 0 or b >= len(nums)):
    raise IndexError("Index out of bounds.")
  
  tmp = nums[a]
  nums[a] = nums[b]
  nums[b] = tmp
  add_clip(nums)
  reset_colors()
  return nums

def render(algorithm: Callable, video_directory: str = os.getcwd(), vidoe_name: str = "movie", fps: int = 50) -> None:
  """
  Renders the given algorithm to a video.

  :param algorithm (function): The sorting algorithm (writen using the provided visualsort functions) that will be rendered.
  :type algorithm: function
  :param video_directory (str): The dirrectory where the video file will be saved.
  :type video_directory: str
  :param video_name (str): The diseried name of the video file.
  :type video_name: str
  :param fps (int): The frame rate of the video.
  :type fps: int
  :raises IndexError: If either of the indices is out of bounds.
  """
  nums = generate_numbers()
  reset_colors()
  
  add_clip(nums)
  
  algorithm(nums)
  
  go_through(nums)

  if not os.path.exists(video_directory):
    os.mkdir(video_directory)

  final_clip = ImageSequenceClip(clips, fps=fps)

  final_clip.write_videofile(os.path.join(video_directory, vidoe_name + ".mp4"), fps=fps)