# ──────────────────────────────────────────────────────────────────────────────
# MIT License
#
# Copyright (c) 2025 BODIT Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ──────────────────────────────────────────────────────────────────────────────

import os
import importlib.util

pyd_path = r"\\bodit-analysis\FarmersHands\fh-module\fhFeature.cp311-win_amd64.pyd"

if not os.path.isfile(pyd_path):
    raise ImportError("잘못된 접근입니다.")

spec = importlib.util.spec_from_file_location("fhFeature", pyd_path)
_fhFeature_ext = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_fhFeature_ext)

def __getattr__(name: str):
    try:
        return getattr(_fhFeature_ext, name)
    except AttributeError:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

def __dir__():
    public = [n for n in dir(_fhFeature_ext) if not n.startswith("_")]
    return sorted(list(globals().keys()) + public)

__all__ = [n for n in dir(_fhFeature_ext) if not n.startswith("_")]