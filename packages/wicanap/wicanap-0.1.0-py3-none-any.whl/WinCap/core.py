import time
import ctypes
import os
from math import cos, sin, pi
from PIL import Image, ImageWin
from ctypes import wintypes
from .input import Mouse, Keyboard
from .constants import NAMED_COLORS
from .winapi import WNDCLASS, PAINTSTRUCT, WNDPROC, INT_PTR


class Canvas:
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    kernel32 = ctypes.windll.kernel32

    def __init__(self, width=800, height=600, title="Window"):
        self.width = width
        self.height = height
        self.title = title
        self.bgcolor = (255, 255, 255)
        self.color = (0, 0, 0)
        self._fps = 60
        self.running = True
        self.draw_func = None
        self.lines = []
        self.sprites = []
        self.texts = []
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.rotation = 0
        self.key_down_callback = None
        self.key_up_callback = None
        self.camera_x = 0
        self.camera_y = 0
        self.camera_target_x = 0
        self.camera_target_y = 0
        self.camera_smooth = 0.1

        self.hInstance = self.kernel32.GetModuleHandleW(None)
        self.className = "CustomWindowClass"
        self.wndProc = WNDPROC(self._wnd_proc)

        wndClass = WNDCLASS()
        wndClass.lpfnWndProc = self.wndProc
        wndClass.hInstance = self.hInstance
        wndClass.lpszClassName = self.className
        wndClass.hCursor = self.user32.LoadCursorW(None, 32512)
        wndClass.hbrBackground = 0
        self.user32.RegisterClassW(ctypes.byref(wndClass))

        WS_OVERLAPPEDWINDOW = 0x00CF0000
        self.hwnd = self.user32.CreateWindowExW(
            0, self.className, self.title, WS_OVERLAPPEDWINDOW,
            100, 100, self.width, self.height,
            None, None, self.hInstance, None
        )

        self.user32.ShowWindow(self.hwnd, 1)
        self.user32.UpdateWindow(self.hwnd)

    def icon(self, filename):
        if os.path.exists(filename):
            hIcon = self.user32.LoadImageW(None, filename, 1, 0, 0, 0x00000010)
            self.user32.SendMessageW(self.hwnd, 0x80, 1, hIcon)

    def set_color(self, *args):
        if len(args) == 1:
            self.color = NAMED_COLORS.get(args[0].lower(), (0, 0, 0))
        elif len(args) == 3:
            self.color = tuple(map(int, args))

    def back_fill(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            self.bgcolor = NAMED_COLORS.get(args[0].lower(), (255, 255, 255))
        elif len(args) == 3:
            self.bgcolor = tuple(map(int, args))

    def set_rotate(self, angle):
        self.rotation = angle

    def set_camera(self, x, y):
        self.camera_target_x = x
        self.camera_target_y = y

    def draw_line(self, width, x1, y1, x2, y2):
        self.lines.append((width, self.color, x1, y1, x2, y2))

    def sprite(self, x, y, image, size):
        self.sprites.append((x, y, image, size))

    def DrawRect(self, size, x, y, sizex, sizey):
        self.draw_line(size, x, y, x + sizex, y)
        self.draw_line(size, x + sizex, y, x + sizex, y + sizey)
        self.draw_line(size, x + sizex, y + sizey, x, y + sizey)
        self.draw_line(size, x, y + sizey, x, y)

    def DrawCircle(self, radius, x, y, steps=36):
        angle_step = 2 * pi / steps
        for i in range(steps):
            a1 = angle_step * i
            a2 = angle_step * (i + 1)
            x1 = x + cos(a1) * radius
            y1 = y + sin(a1) * radius
            x2 = x + cos(a2) * radius
            y2 = y + sin(a2) * radius
            self.draw_line(1, int(x1), int(y1), int(x2), int(y2))

    @property
    def fps(self):
        return self._fps

    def updaterate(self, fps):
        self._fps = fps

    def run(self, draw_func=None):
        self.draw_func = draw_func
        interval = 1 / self._fps
        while self.running:
            msg = wintypes.MSG()
            while self.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
                self.user32.TranslateMessage(ctypes.byref(msg))
                self.user32.DispatchMessageW(ctypes.byref(msg))
            if self.draw_func:
                self.draw_func(self)
            self._repaint()
            time.sleep(interval)

    def _repaint(self):
        dx = self.camera_target_x - self.camera_x
        dy = self.camera_target_y - self.camera_y
        if abs(dx) > 0.1:
            self.camera_x += dx * self.camera_smooth
        if abs(dy) > 0.1:
            self.camera_y += dy * self.camera_smooth

        hdc = self.user32.GetDC(self.hwnd)
        memdc = self.gdi32.CreateCompatibleDC(hdc)
        bmp = self.gdi32.CreateCompatibleBitmap(hdc, self.width, self.height)
        self.gdi32.SelectObject(memdc, bmp)

        brush = self.gdi32.CreateSolidBrush(
            self.bgcolor[0] | (self.bgcolor[1] << 8) | (self.bgcolor[2] << 16)
        )
        rect = wintypes.RECT(0, 0, self.width, self.height)
        self.user32.FillRect(memdc, ctypes.byref(rect), brush)
        self.gdi32.DeleteObject(brush)

        cx, cy = int(self.width // 2 - self.camera_x), int(self.height // 2 + self.camera_y)

        for width, color, x1, y1, x2, y2 in self.lines:
            pen = self.gdi32.CreatePen(0, width, color[0] | (color[1] << 8) | (color[2] << 16))
            old_pen = self.gdi32.SelectObject(memdc, pen)
            self.gdi32.MoveToEx(memdc, int(cx + x1), int(cy - y1), None)
            self.gdi32.LineTo(memdc, int(cx + x2), int(cy - y2))
            self.gdi32.SelectObject(memdc, old_pen)
            self.gdi32.DeleteObject(pen)

        for x, y, image, size in self.sprites:
            if image.lower().endswith(".bmp"):
                hbmp = self.user32.LoadImageW(None, image, 0, 0, 0, 0x00000010)
                if hbmp:
                    hdcMem = self.gdi32.CreateCompatibleDC(memdc)
                    self.gdi32.SelectObject(hdcMem, hbmp)
                    self.gdi32.StretchBlt(memdc, int(cx + x), int(cy - y), size, size, hdcMem, 0, 0, size, size, 0x00CC0020)
                    self.gdi32.DeleteDC(hdcMem)
                    self.gdi32.DeleteObject(hbmp)
            else:
                img = Image.open(image).convert("RGBA").resize((size, size))
                if self.rotation != 0:
                    img = img.rotate(self.rotation, expand=True)
                dib = ImageWin.Dib(img)
                dib.draw(memdc, (int(cx + x), int(cy - y - img.height), int(cx + x + img.width), int(cy - y)))

        for size, font_file, color, x, y, text in self.texts:
            hfont = self.gdi32.CreateFontW(
                -size, 0, 0, 0, 400, 0, 0, 0, 1, 0, 0, 0, 0, font_file
            )
            self.gdi32.SelectObject(memdc, hfont)
            self.gdi32.SetTextColor(memdc, color[0] | (color[1] << 8) | (color[2] << 16))
            self.gdi32.SetBkMode(memdc, 1)
            self.gdi32.TextOutW(memdc, int(cx + x), int(cy - y), text, len(text))
            self.gdi32.DeleteObject(hfont)

        self.gdi32.BitBlt(hdc, 0, 0, self.width, self.height, memdc, 0, 0, 0x00CC0020)
        self.gdi32.DeleteObject(bmp)
        self.gdi32.DeleteDC(memdc)
        self.user32.ReleaseDC(self.hwnd, hdc)

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == 0x0002:
            self.running = False
            self.user32.PostQuitMessage(0)
            return 0
        elif msg == 0x0201:
            self.mouse.press = True
        elif msg == 0x0202:
            self.mouse.press = False
        elif msg == 0x0200:
            self.mouse.x = ctypes.c_short(lparam & 0xFFFF).value
            self.mouse.y = ctypes.c_short((lparam >> 16) & 0xFFFF).value
        elif msg == 0x0100:
            if not self.keyboard[wparam]:
                if self.key_down_callback:
                    self.key_down_callback(wparam)
            self.keyboard.update_key(wparam, True)
        elif msg == 0x0101:
            if self.key_up_callback:
                self.key_up_callback(wparam)
            self.keyboard.update_key(wparam, False)
        elif msg == 0x000F:
            ps = PAINTSTRUCT()
            hdc = self.user32.BeginPaint(hwnd, ctypes.byref(ps))
            self._repaint()
            self.user32.EndPaint(hwnd, ctypes.byref(ps))
            return 0
        DefWindowProc = ctypes.WINFUNCTYPE(
            INT_PTR, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM
        )(("DefWindowProcW", self.user32))
        return DefWindowProc(hwnd, msg, wparam, lparam)
