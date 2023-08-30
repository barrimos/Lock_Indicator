import pystray
from PIL import Image
import keyboard
import ctypes

image_c = Image.open("./src/img/c.png")
image_n = Image.open("./src/img/n.png")

def get_icon_image(caps_lock, num_lock):
    """Create an icon image using the provided images."""
    width, height = 32, 32
    icon_image = Image.new("RGB", (width, height), "white")

    if caps_lock:
        resized_image_c = image_c.resize((width // 2, height))
        icon_image.paste(resized_image_c, (0, 0), resized_image_c)
    if num_lock:
        resized_image_n = image_n.resize((width // 2, height))
        icon_image.paste(resized_image_n, (16, 0), resized_image_n)

    return icon_image

def update_icon(icon, caps_lock, num_lock):
    """Update the icon with the appropriate images."""
    icon.icon = get_icon_image(caps_lock, num_lock)
    icon.update_menu()
    
def main():
    caps_lock = True if ctypes.WinDLL("User32.dll").GetKeyState(0x14) else False
    num_lock = True if ctypes.WinDLL("User32.dll").GetKeyState(0x90) else False

    def caps_lock_handler(e):
        nonlocal caps_lock
        caps_lock = not caps_lock
        update_icon(icon, caps_lock, num_lock)

    def num_lock_handler(e):
        nonlocal num_lock
        num_lock = not num_lock
        update_icon(icon, caps_lock, num_lock)

    keyboard.on_press_key("caps lock", caps_lock_handler)
    keyboard.on_press_key("num lock", num_lock_handler)

    icon = pystray.Icon("name", get_icon_image(caps_lock, num_lock))
    menu = (pystray.MenuItem("Quit", lambda: icon.stop()),)
    icon.menu = pystray.Menu(*menu)
    icon.run()

if __name__ == "__main__":
    main()
