from ctypes import wintypes
import sys
import ctypes
NAMED_COLORS = {
    "black": (0, 0, 0), "white": (255, 255, 255),
    "red": (255, 0, 0), "green": (0, 255, 0),
    "blue": (0, 0, 255), "yellow": (255, 255, 0),
    "purple": (128, 0, 128), "gray": (128, 128, 128)
}

INT_PTR = ctypes.c_int64 if sys.maxsize > 2**32 else ctypes.c_int32
HCURSOR = wintypes.HANDLE
HICON = wintypes.HANDLE
HBRUSH = wintypes.HANDLE
LPCWSTR = wintypes.LPWSTR
HINSTANCE = wintypes.HANDLE
