# wincap

**wincap** is a lightweight 2D graphics library for Python, built on top of WinAPI using `ctypes`.

It's designed for creating simple Windows-based applications with support for:
- primitives (lines, rectangles, circles)
- sprites with transparency
- smooth camera movement
- keyboard and mouse input
- and basic sound playback

---

## 🚀 Quick Example

```python
from wincap import Canvas, sound

win = Canvas(800, 600, "PixAPI Demo")
win.set_color("green")
win.DrawRect(2, -50, -50, 100, 100)

def draw(win):
    win.set_camera(0, 0)

win.run(draw)
