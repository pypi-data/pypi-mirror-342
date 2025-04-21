import os
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("choprotarget", nargs='?', default=os.getcwd(), help=".chopro filename or directory containing .chopro files")
  parser.add_argument("--pagesize", type=str, default='a6')
  parser.add_argument("--showchords", type=str, default='false')
  args = parser.parse_args()

  if os.path.exists(args.choprotarget):
    print(f"choprotarget = {args.choprotarget}")
    if os.path.isdir(args.choprotarget):
      print("target is directory")
    else:
      print("target is file")
  else:
    print(f"chopro target '{args.choprotarget}' does not exist")

main()
