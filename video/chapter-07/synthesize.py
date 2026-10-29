"""Generate Chapter 7 with the approved original synthetic Q1 voice."""
from pathlib import Path
import runpy,sys
sys.argv[1:1]=['--chapters','07']
runpy.run_path(str(Path(__file__).resolve().parents[1]/'qwen-production'/'synthesize.py'),run_name='__main__')
