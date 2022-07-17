import tkinter as tk
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


BG = (0, 0, 0)  # black
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

root = tk.Tk()
root.geometry("600x500+600+95")

root.configure(bg=rgb_to_hex(BG))

fg_faded = bg_faded = None
STEP = 5
DELAY = 18


def fade_widget(attribute,color,e,fade_loop):
    global fg_faded, bg_faded

    if abs(color[0] - BG[0]) > STEP:
        if color[0] > BG[0]:
            color[0] -= STEP
        else:
            color[0] += STEP

    if abs(color[1] - BG[1]) > STEP:
        if color[1] > BG[1]:
            color[1] -= STEP
        else:
            color[1] += STEP

    if abs(color[2] - BG[2]) > STEP:
        if color[2] > BG[2]:
            color[2] -= STEP
        else:
            color[2] += STEP

    e.widget[attribute] = rgb_to_hex(tuple(color))

    if abs(color[0] - BG[0]) <= STEP and abs(color[1] - BG[1]) <= STEP and abs(color[2] - BG[2]) <= STEP:
        root.after_cancel(fade_loop)
        fade_loop = None

        if attribute == "fg":
            fg_faded = True
        else:
            bg_faded = True

        if fg_faded and bg_faded:
            e.widget.destroy()

    if fade_loop:
        fade_loop = root.after(DELAY, lambda: fade_widget(attribute, color, e, fade_loop))


def get_color_and_fade(e):
    bg_hex = e.widget["bg"]
    fg_hex = e.widget["fg"]
    fg_rgb = list(hex_to_rgb(fg_hex))
    bg_rgb = list(hex_to_rgb(bg_hex))

    fade_fg = fade_bg = None

    fade_fg = root.after(DELAY, lambda: fade_widget("fg",fg_rgb,e,fade_fg))
    fade_bg = root.after(DELAY, lambda: fade_widget("bg",bg_rgb,e,fade_bg))


b1 = tk.Button(root, text="Click To Fade", font="Arial 14 bold", fg=rgb_to_hex(GREEN), bg=rgb_to_hex(RED), bd=0)
b1.bind("<Button-1>", get_color_and_fade)
b1.pack(fill="x", pady=100, padx=10)

root.mainloop()
