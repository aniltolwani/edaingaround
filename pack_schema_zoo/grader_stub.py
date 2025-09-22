#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, pathlib, subprocess
if len(sys.argv)!=2:
    print("Usage: python grader_stub.py result.json"); sys.exit(2)
pack_dir = pathlib.Path(__file__).parent
ug = pack_dir.parent / "universal_grader_v2.py"
ret = subprocess.call([sys.executable, str(ug), str(pack_dir), sys.argv[1]])
sys.exit(ret)
