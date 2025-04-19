# MIT License
#
# Copyright (c) 2024 Chronulus AI Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from pydantic import BaseModel


def get_deep_size_bytes(obj) -> int:
    """Get a more comprehensive size for complex objects"""
    if isinstance(obj, (str, bytes, int, float, bool, type(None))):
        return sys.getsizeof(obj)

    size = sys.getsizeof(obj)
    if issubclass(obj.__class__, BaseModel) or isinstance(obj, BaseModel):
        obj = obj.model_dump()

    if isinstance(obj, dict):
        size += sum(get_deep_size_bytes(k) + get_deep_size_bytes(v) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set)):
        size += sum(get_deep_size_bytes(i) for i in obj)

    return size


def get_object_size_mb(obj) -> float:
    # Get object size in bytes
    size_in_bytes = get_deep_size_bytes(obj)
    # Convert to mb
    size_in_mb = size_in_bytes / (1024 * 1024)
    return size_in_mb