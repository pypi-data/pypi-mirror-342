import ctypes
import sys
from ctypes import wintypes

INT_PTR = ctypes.c_int64 if sys.maxsize > 2**32 else ctypes.c_int32

HCURSOR = wintypes.HANDLE
HICON = wintypes.HANDLE
HBRUSH = wintypes.HANDLE
LPCWSTR = wintypes.LPWSTR
HINSTANCE = wintypes.HANDLE

WNDPROC = ctypes.WINFUNCTYPE(INT_PTR, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", LPCWSTR),
        ("lpszClassName", LPCWSTR),
    ]

class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [
        ("hdc", wintypes.HDC),
        ("fErase", wintypes.BOOL),
        ("rcPaint", wintypes.RECT),
        ("fRestore", wintypes.BOOL),
        ("fIncUpdate", wintypes.BOOL),
        ("rgbReserved", ctypes.c_byte * 32),
    ]
