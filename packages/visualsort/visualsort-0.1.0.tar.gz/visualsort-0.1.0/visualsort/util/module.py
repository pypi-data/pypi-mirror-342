from PIL import Image, ImageDraw
import random
import os
from numpy import asarray
from moviepy.editor import *

video_width = 1280
video_height = 720
header_height = 40
length = 100

column_width = video_width / length
column_height = ((video_height - header_height) / length)

clips = []

colors = {
  "white": (255, 255, 255),
  "red": (255, 0, 0),
  "green": (0, 255, 0),
  "black": (0, 0, 0),
}

column_colors = []
default_colors = []

def make_frame(nums):
  global video_height
  global video_width
  global column_width
  global column_height
  global column_colors
  
  img = Image.new('RGB', (video_width, video_height))

  draw = ImageDraw.Draw(img)

  for i in range(len(nums)):
    draw.rectangle([(i * column_width, video_height - nums[i] * column_height), ((i + 1) * column_width, video_height)], column_colors[i], outline=colors["black"])

  return asarray(img)

def add_clip(nums):
  clips.append(make_frame(nums))

def assign_color(x, color):
  global column_colors
  global colors
  
  column_colors[x] = colors[color]

def generate_numbers():
  global default_colors
  
  nums = []
  for i in range(1, length + 1):
    nums.append(i)
    default_colors.append(colors["white"])

  random.shuffle(nums)

  return nums

def go_through(nums):
  for i in range(len(nums)):
    assign_color(i, "red")
    add_clip(nums)
    assign_color(i, "green")

  reset_colors()
  
  add_clip(nums)

def reset_colors():
  global column_colors
  global default_colors
  column_colors = default_colors.copy()