import subprocess as sp
import cv2, os, tempfile as tf, time, re, sys
from functools import lru_cache

COLORS = {'GREEN': '\033[92m', 'BLUE': '\033[94m', 'RED': '\033[91m', 'YELLOW': '\033[93m', 'WHITE': '\033[97m', 'RESET': '\033[0m'}

def format_message(messages, width=80, color=COLORS['GREEN']):
    if not messages: return ""
    if isinstance(messages, str): messages = [messages]
    
    border = '─' * (width - 2)
    border_top = f"{color}╭{border}╮{COLORS['RESET']}"
    border_bottom = f"{color}╰{border}╯{COLORS['RESET']}"
    empty_line = f"{color}│{' ' * (width - 2)}│{COLORS['RESET']}"
    
    lines = [border_top]
    for i, msg in enumerate(messages):
        left_pad = (width - len(msg) - 2) // 2
        right_pad = width - len(msg) - left_pad - 2
        lines.append(f"{color}│{' ' * left_pad}{msg}{' ' * right_pad}│{COLORS['RESET']}")
        if i < len(messages) - 1:
            lines.append(empty_line)
    lines.append(border_bottom)
    
    return "\n".join(lines)

format_centered_message = format_multi_line_message = format_message

class Logger:
    @staticmethod
    def message(message="", color="WHITE"): print(format_message([message], color=COLORS[color]))

    @staticmethod
    def log(act="", msg="", *info, c=COLORS['BLUE']): print(format_message([f"{act}: {msg}"] + list(info), color=c))
    
    @staticmethod
    def log_success(act="", msg="", *info): Logger.log(act, msg, *info, c=COLORS['GREEN'])
    
    @staticmethod
    def log_info(act="", msg="", *info):  Logger.log(act, msg, *info, c=COLORS['BLUE'])
    
    @staticmethod
    def log_warning(act="", msg="", *info): Logger.log(act, msg, *info, c=COLORS['YELLOW'])
    
    @staticmethod
    def log_error_warn(act="", msg="", *info): Logger.log(act, msg, *info, c=COLORS['RED'])
    
    @staticmethod
    def log_error(act="", msg="", *info): Logger.log(act, msg, *info, c=COLORS['RED']); os.execv(sys.executable, ['python'] + sys.argv)
    

class ADBCommand:
    @staticmethod
    def execute(cmd, shell=False, capture=False):
        try:
            if capture: 
                return sp.run(cmd, shell=shell, capture_output=True, text=True)
            sp.run(cmd, shell=shell, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            return True
        except:
            Logger.log_error("ERROR", "Failed to execute ADB command", f"Command: {cmd}")
            return False
    
    @staticmethod
    def tap(x, y, duration=0):
        cmd = ['adb', 'shell', 'input']
        cmd.extend(['tap', str(x), str(y)] if duration <= 0
                   else ['swipe', str(x), str(y), str(x+1), str(y+1), str(duration)])
        return ADBCommand.execute(cmd)
    
    @staticmethod
    def keyevent(k, desc=None):
        if desc: Logger.log_warning("KEYEVENT", desc)
        return ADBCommand.execute(['adb', 'shell', 'input', 'keyevent', k])
    
    @staticmethod
    def notification(action, desc):
        cmds = {
            'open': ['adb', 'shell', 'cmd', 'statusbar', 'expand-notifications'],
            'close': ['adb', 'shell', 'cmd', 'statusbar', 'collapse'],
            'clear': ['adb', 'shell', 'service', 'call', 'notification', '1']
        }
        
        if action in cmds:
            Logger.log_success("NOTIFICATIONS", desc)
            ADBCommand.execute(cmds[action])
            return True
        return False


class ImageProcessor:
    _template_cache = {}
    
    @staticmethod
    def parse_coords(txt):
        if not txt or not isinstance(txt, str) or not (matches := re.findall(r'(TL|TR|BL|BR|Mid): (\d+),(\d+)', txt)):
            return None
        return {pos: (int(x), int(y)) for pos, x, y in matches}
    
    @staticmethod
    def capture_screenshot():
        path = os.path.join(tf.gettempdir(), "screenshot.png")
        ADBCommand.execute(['adb', 'exec-out', 'screencap', '-p', '>', path], shell=True)
        return cv2.imread(path)
    
    @staticmethod
    def crop_image(img, region):
        if img is None or not isinstance(region, dict) or 'TL' not in region or 'BR' not in region:
            return img, (0, 0)
        (tl_x, tl_y), (br_x, br_y) = region['TL'], region['BR']
        h, w = img.shape[:2]
        tl_x, tl_y = max(0, tl_x), max(0, tl_y)
        br_x, br_y = min(w, br_x), min(h, br_y)
        return (img[tl_y:br_y, tl_x:br_x], (tl_x, tl_y)) if tl_x < br_x and tl_y < br_y else (img, (0, 0))
    
    @staticmethod
    @lru_cache(maxsize=32)
    def get_template(path):
        if path not in ImageProcessor._template_cache:
            tmpl = cv2.imread(path)
            if tmpl is not None: ImageProcessor._template_cache[path] = tmpl
            return tmpl
        return ImageProcessor._template_cache[path]
    
    @staticmethod
    def create_region(tl=None, br=None):
        if tl is None or br is None: return None
        coords = {'TL': tuple(tl) if isinstance(tl, (list, tuple)) else tl,
                 'BR': tuple(br) if isinstance(br, (list, tuple)) else br}
        coords['Mid'] = ((coords['TL'][0] + coords['BR'][0]) // 2, 
                         (coords['TL'][1] + coords['BR'][1]) // 2)
        return coords
    
    @staticmethod
    def process_template(name, prefix="images/", suffix=".png", tl=None, br=None):
        reg, direct, center, valid = None, False, None, True
        
        if tl is not None and br is not None:
            reg = ImageProcessor.create_region(tl, br)
            if name == "*": direct, center = True, reg['Mid']
        elif isinstance(name, str) and "TL:" in name and "BR:" in name:
            coords = ImageProcessor.parse_coords(name)
            if coords: reg, direct, center = coords, True, coords.get('Mid')
        elif isinstance(name, (list, tuple)) and len(name) == 2:
            direct, center = True, name
        
        if not direct and not os.path.isfile(f"{prefix}{name}{suffix}"):
            Logger.log_error("ERROR", f"Template file '{prefix}{name}{suffix}' does not exist")
            valid = False
        
        return reg, direct, center, valid
    
    @staticmethod
    def find_image(name, timeout=5, thresh=0.8, prefix="images/", suffix=".png", region=None):
        t0 = time.time()
        tmpl = ImageProcessor.get_template(f"{prefix}{name}{suffix}")
        if tmpl is None: return False, None, 0, 0, 0
        
        h, w = tmpl.shape[:2]
        ox, oy = 0, 0
        timeout_sec = timeout / 1000 if timeout > 20 else timeout
        interval = min(0.3, max(0.1, timeout_sec/10))
        last_check = t0 - interval
        
        while time.time() - t0 < timeout_sec:
            if time.time() - last_check >= interval:
                last_check = time.time()
                ss = ImageProcessor.capture_screenshot()
                if ss is None: 
                    time.sleep(0.05)
                    continue
                
                cropped, (ox, oy) = ImageProcessor.crop_image(ss, region)
                result = cv2.matchTemplate(cropped, tmpl, cv2.TM_CCOEFF_NORMED)
                _, val, _, loc = cv2.minMaxLoc(result)
                
                if val >= thresh:
                    ax, ay = loc[0] + ox, loc[1] + oy
                    return True, (ax + w // 2, ay + h // 2), time.time() - t0, w, h
            else:
                time.sleep(0.02)
        
        return False, None, time.time() - t0, 0, 0


class DeviceHelper:
    @staticmethod
    def wait(ms, context=""):
        if ms <= 0: return
        sec = ms/1000
        Logger.log_warning("WAIT", f"Waiting {sec:.2f}s {context}")
        time.sleep(sec)
    
    @staticmethod
    def exists(name, timeout=5000, thresh=0.8, prefix="images/", suffix=".png", region=None, 
               tl=None, br=None, description=None, wait_before=0, wait_after=0, fatal_error=False):
        if wait_before > 0:
            DeviceHelper.wait(wait_before, f"before checking if '{name}' exists")
        
        if isinstance(name, list) and not name:
            return False if not isinstance(name, list) else None
        
        if not isinstance(name, list):
            r, direct, center, valid = ImageProcessor.process_template(name, prefix, suffix, tl, br)
            if not valid: return False
            if direct: return True
            if r is not None: region = r
            
            Logger.log_info("SEARCH", f"Searching for image '{name}'... (timeout: {timeout/1000:.1f}s)")
            found, center, elapsed, w, h = ImageProcessor.find_image(name, timeout, thresh, prefix, suffix, region)
            
            if found:
                pos = f"Position: TL=({center[0]-w//2}, {center[1]-h//2}), BR=({center[0]+w//2}, {center[1]+h//2}), MID={center}"
                Logger.log_success("EXISTS", f"Image '{name}' found", pos)
                if wait_after > 0:
                    DeviceHelper.wait(wait_after, f"after finding '{name}'")
            else:
                log_fn = Logger.log_error if fatal_error else Logger.log_error_warn
                log_fn("EXISTS", f"Image '{name}' not found", f"Timeout after: {elapsed:.2f}s (timeout: {timeout/1000:.1f}s)")
            
            return found
        
        Logger.log_info("SEARCH", f"Searching for any of {len(name)} images... (timeout: {timeout/1000:.1f}s)")
        templates = {}
        for img_name in name:
            tmpl = ImageProcessor.get_template(f"{prefix}{img_name}{suffix}")
            if tmpl is not None:
                templates[img_name] = tmpl
            elif fatal_error:
                Logger.log_error("EXISTS", f"Template '{prefix}{img_name}{suffix}' not found")
            else:
                Logger.log_error_warn("EXISTS", f"Template '{prefix}{img_name}{suffix}' not found")
        
        if not templates:
            return False if not isinstance(name, list) else None
        
        timeout_sec = timeout / 1000
        check_interval = min(0.3, timeout_sec/(5 * len(templates)))
        start_time = time.time()
        last_check = 0
        
        while time.time() - start_time < timeout_sec:
            if time.time() - last_check >= check_interval:
                last_check = time.time()
                ss = ImageProcessor.capture_screenshot()
                if ss is None:
                    time.sleep(0.05)
                    continue
                
                cropped, (ox, oy) = ImageProcessor.crop_image(ss, region)
                best_match, best_val, best_img, best_size = None, 0, None, (0, 0)
                
                for img_name, tmpl in templates.items():
                    h, w = tmpl.shape[:2]
                    _, val, _, loc = cv2.minMaxLoc(cv2.matchTemplate(cropped, tmpl, cv2.TM_CCOEFF_NORMED))
                    if val > best_val and val >= thresh:
                        best_val, best_match, best_img, best_size = val, loc, img_name, (w, h)
                
                if best_match:
                    w, h = best_size
                    ax, ay = best_match[0] + ox, best_match[1] + oy
                    best_center = (ax + w//2, ay + h//2)
                    pos = f"Position: TL=({best_center[0]-w//2}, {best_center[1]-h//2}), BR=({best_center[0]+w//2}, {best_center[1]+h//2}), MID={best_center}"
                    Logger.log_success("EXISTS", f"Image '{best_img}' found", pos)
                    
                    if wait_after > 0:
                        DeviceHelper.wait(wait_after, f"after finding '{best_img}'")
                    
                    return best_img if isinstance(name, list) else (True, best_img, best_center)
            else:
                time.sleep(0.02)
        
        elapsed = time.time() - start_time
        log_fn = Logger.log_error if fatal_error else Logger.log_error_warn
        log_fn("EXISTS", f"None of the images were found", f"Timeout after: {elapsed:.2f}s (timeout: {timeout_sec:.1f}s)")
        
        return False if not isinstance(name, list) else None
    
    @staticmethod
    def touch(name, timeout=10000, thresh=0.8, prefix="images/", suffix=".png", dur=0, 
              region=None, tl=None, br=None, wait_before=0, wait_after=0, description=None, ss_path=None):
        if wait_before > 0:
            DeviceHelper.wait(wait_before, f"before touching '{name}'")
            
        if ss_path:
            try:
                os.makedirs(ss_path, exist_ok=True)
                Logger.log_info("TOUCH", f"Screenshot path set to: {ss_path}")
            except Exception as e:
                Logger.log_error_warn("TOUCH", f"Failed to create screenshot directory: {e}")
        
        def save_failed_screenshot(img_name, reason=""):
            if not ss_path:
                return
            try:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                failed_path = os.path.join(ss_path, f"failed_{reason}_{img_name}_{timestamp}.png")
                ss = last_ss if last_ss is not None else ImageProcessor.capture_screenshot()
                if ss is not None and cv2.imwrite(failed_path, ss):
                    Logger.log_warning("SCREENSHOT", f"Saved failed screenshot to {failed_path}")
                else:
                    Logger.log_error_warn("SCREENSHOT", f"Failed to save screenshot to {failed_path}")
            except Exception as e:
                Logger.log_error_warn("SCREENSHOT", f"Error saving screenshot: {str(e)}")
        
        last_ss = None
        
        if isinstance(name, list):
            if not name:
                return False
                
            Logger.log_info("SEARCH", f"Searching for any of {len(name)} images to touch... (timeout: {timeout/1000:.1f}s)")
            
            templates = {img_name: tmpl for img_name in name 
                        if (tmpl := ImageProcessor.get_template(f"{prefix}{img_name}{suffix}")) is not None}
            
            if not templates:
                return False
                
            start_time = time.time()
            timeout_sec = timeout / 1000
            check_interval = min(0.3, timeout_sec/(5 * len(templates)))
            last_check = 0
            
            while time.time() - start_time < timeout_sec:
                if time.time() - last_check >= check_interval:
                    last_check = time.time()
                    ss = ImageProcessor.capture_screenshot()
                    if ss is None:
                        time.sleep(0.05)
                        continue
                    
                    last_ss = ss.copy()
                    cropped, (ox, oy) = ImageProcessor.crop_image(ss, region)
                    
                    best_match, best_val, best_img, best_size = None, 0, None, (0, 0)
                    
                    for img_name, tmpl in templates.items():
                        h, w = tmpl.shape[:2]
                        _, val, _, loc = cv2.minMaxLoc(cv2.matchTemplate(cropped, tmpl, cv2.TM_CCOEFF_NORMED))
                        if val > best_val and val >= thresh:
                            best_val, best_match, best_img, best_size = val, loc, img_name, (w, h)
                    
                    if best_match:
                        w, h = best_size
                        ax, ay = best_match[0] + ox, best_match[1] + oy
                        center = (ax + w // 2, ay + h // 2)
                        x, y = center
                        
                        action = "pressed" if dur > 0 else "tapped"
                        cmd = ['adb', 'shell', 'input', 'swipe' if dur > 0 else 'tap'] + \
                              ([str(x), str(y), str(x+1), str(y+1), str(dur)] if dur > 0 else [str(x), str(y)])
                        
                        pos = f"Position: TL=({x-w//2}, {y-h//2}), BR=({x+w//2}, {y+h//2}), MID={center}"
                        
                        if ADBCommand.execute(cmd):
                            Logger.log_success("TOUCH", f"Successfully {action} '{best_img}'" + (f" for {dur}ms" if dur > 0 else ""), pos)
                            if wait_after > 0:
                                DeviceHelper.wait(wait_after, f"after touching '{best_img}'")
                            return best_img
                        else:
                            Logger.log_error("TOUCH", f"Failed to {action} '{best_img}'", pos)
                            return False
                else:
                    time.sleep(0.02)
            
            Logger.log_error("TOUCH", f"None of the images were found to touch", 
                            f"Timeout after: {time.time()-start_time:.2f}s (timeout: {timeout_sec:.1f}s)")
            save_failed_screenshot(str(name))
            return False
        
        r, direct, center, valid = ImageProcessor.process_template(name, prefix, suffix, tl, br)
        
        if not valid:
            save_failed_screenshot(name, "invalid")
            return False
            
        if r is not None:
            region = r
        
        if direct and center:
            x, y = center
            action = "pressed" if dur > 0 else "tapped"
            cmd = ['adb', 'shell', 'input', 'swipe' if dur > 0 else 'tap'] + \
                  ([str(x), str(y), str(x+1), str(y+1), str(dur)] if dur > 0 else [str(x), str(y)])
            
            if ADBCommand.execute(cmd):
                Logger.log_success("TOUCH", f"{action.capitalize()} at coordinates ({x}, {y})" + 
                                  (f" for {dur} ms" if dur > 0 else ""))
                if wait_after > 0:
                    DeviceHelper.wait(wait_after, "after touching coordinates")
                return True, "direct_coords", center
            return False, None, None
        
        Logger.log_info("SEARCH", f"Searching for image '{name}'...")
        
        t0 = time.time()
        timeout_sec = timeout / 1000
        
        while time.time() - t0 < timeout_sec:
            ss = ImageProcessor.capture_screenshot()
            if ss is None:
                time.sleep(0.2)
                continue
                
            last_ss = ss.copy()
            cropped, (ox, oy) = ImageProcessor.crop_image(ss, region)
            path = f"{prefix}{name}{suffix}"
            tmpl = ImageProcessor.get_template(path)
            
            if tmpl is None:
                Logger.log_error("TOUCH", f"Template '{path}' not found")
                save_failed_screenshot(name, "notemplate")
                return False, None, None
                
            h, w = tmpl.shape[:2]
            _, val, _, loc = cv2.minMaxLoc(cv2.matchTemplate(cropped, tmpl, cv2.TM_CCOEFF_NORMED))
            
            if val >= thresh:
                center = (loc[0] + ox + w // 2, loc[1] + oy + h // 2)
                x, y = center
                
                action = "pressed" if dur > 0 else "tapped"
                cmd = ['adb', 'shell', 'input', 'swipe' if dur > 0 else 'tap'] + \
                      ([str(x), str(y), str(x+1), str(y+1), str(dur)] if dur > 0 else [str(x), str(y)])
                
                pos = f"Position: TL=({x-w//2}, {y-h//2}), BR=({x+w//2}, {y+h//2}), MID={center}"
                
                if ADBCommand.execute(cmd):
                    Logger.log_success("TOUCH", f"Successfully {action} '{name}'" + (f" for {dur}ms" if dur > 0 else ""), pos)
                    if wait_after > 0:
                        DeviceHelper.wait(wait_after, f"after touching '{name}'")
                    return True, name, center
                else:
                    Logger.log_error("TOUCH", f"Failed to {action} '{name}'", pos)
                    return False, name, None
            
            time.sleep(0.3)
        
        Logger.log_error("TOUCH", f"Image '{name}' not found", f"Timeout after: {time.time()-t0:.2f}s (timeout: {timeout_sec:.2f}s)")
        save_failed_screenshot(name)
        return False, None, None
    
    @staticmethod
    def run_shell_command(cmd, description=None):
        Logger.log_warning("SHELL", f"Executing '{cmd}'")
        ADBCommand.execute(['adb', 'shell', cmd])
    
    @staticmethod
    def swipe(sx, sy, ex, ey, dur=300, wait_before=0, wait_after=0, description=None):
        if wait_before > 0: DeviceHelper.wait(wait_before, "before swiping")
        Logger.log_success("SWIPE", f"From ({sx}, {sy}) to ({ex}, {ey})", f"Duration: {dur}ms")
        ADBCommand.execute(['adb', 'shell', 'input', 'swipe', str(sx), str(sy), str(ex), str(ey), str(dur)])
        if wait_after > 0: DeviceHelper.wait(wait_after, "after swiping")
    
    @staticmethod
    def input_text(txt, submit=False, wait_before=0, wait_after=0, description=None):
        if wait_before > 0: DeviceHelper.wait(wait_before, "before inputting text")
        
        Logger.log_warning("TEXT", f"Inputting text \"{txt}\"" + (" with Submit" if submit else ""))
        ADBCommand.execute(['adb', 'shell', 'input', 'text', txt.replace(' ', '%s')])
        
        if submit: ADBCommand.keyevent('KEYCODE_ENTER')
        if wait_after > 0: DeviceHelper.wait(wait_after, "after inputting text")
    
    @staticmethod
    def paste_from_clipboard(submit=False, wait_before=0, wait_after=0, description=None):
        if wait_before > 0: DeviceHelper.wait(wait_before, "before pasting from clipboard")
        
        Logger.log_info("PASTE", "Pasting content from clipboard")
        ADBCommand.execute(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_PASTE'])
        
        if submit: 
            time.sleep(0.5)
            ADBCommand.keyevent('KEYCODE_ENTER')
        
        if wait_after > 0: DeviceHelper.wait(wait_after, "after pasting from clipboard")
        return True
    
    @staticmethod
    def take_screenshot(path):
        Logger.log_success("SCREENSHOT", f"Taking screenshot and saving to {path}")
        
        if (ss := ImageProcessor.capture_screenshot()) is not None and cv2.imwrite(path, ss):
            return path
        
        tmp = "/sdcard/screenshot.png"
        ADBCommand.execute(['adb', 'shell', 'screencap', '-p', tmp])
        ADBCommand.execute(['adb', 'pull', tmp, path])
        ADBCommand.execute(['adb', 'shell', 'rm', tmp])
        Logger.log_warning("SCREENSHOT", "Used fallback method")
        return path


class AppManager:   
    @staticmethod
    def install_app(apk):
        Logger.log_success("INSTALL", f"Installing app from /data/local/tmp/{apk}")
        
        from threading import Thread
        install_thread = Thread(target=ADBCommand.execute, 
                               args=(['adb', 'shell', 'pm', 'install', f'/data/local/tmp/{apk}'],), 
                               kwargs={'capture': True})
        install_thread.start()
        
        if not DeviceHelper.exists("INSTALL", timeout=10000):
            Logger.log_error("INSTALL", "Application was not installed")
            return False
            
        DeviceHelper.touch("INSTALL")
        Logger.log_success("INSTALL", "Application was installed successfully")
        install_thread.join()
    
    @staticmethod
    def uninstall_app(pkg):
        Logger.log_success("UNINSTALL", f"Uninstalling app {pkg}")
        res = ADBCommand.execute(['adb', 'uninstall', pkg], capture=True)
        time.sleep(1)
        if res and res.returncode == 0 and "Success" in (res.stdout or ""):
            Logger.log_success("UNINSTALL", "Successfully uninstalled")
            return True
        Logger.log_error_warn("UNINSTALL", "Failed to uninstall", 
                             f"Error: {res.stderr if res and res.stderr else 'Uninstallation failed'}")
        return False
    
    @staticmethod
    def clear_recent_apps(clear_package=None, windscribe=False):
        Logger.log_warning("CLEAR_RECENT", "Clearing recent apps")
        ADBCommand.keyevent('KEYCODE_HOME')
        time.sleep(1)
        ADBCommand.keyevent('KEYCODE_APP_SWITCH')
        time.sleep(1)
        AppManager.clear_app(clear_package) if clear_package else None
        time.sleep(1)
        ADBCommand.tap(535, 2220)
        if windscribe:
            AppManager.start_app("com.windscribe.vpn")
            DeviceHelper.touch("BEST_LOCATION", tl=[153,1036], br=[440,1110], wait_after=5000)
    
    @staticmethod
    def clear_recent_apps_and_change_ip(clear_package=None):
        Logger.log_warning("CLEAR_RECENT_AND_CHANGE_IP", "Clearing recent apps and changing IP address")
        ADBCommand.execute(['adb', 'shell', 'cmd', 'connectivity', 'airplane-mode', 'disable'])
        ADBCommand.keyevent('KEYCODE_HOME')
        ADBCommand.execute(['adb', 'shell', 'cmd', 'connectivity', 'airplane-mode', 'enable'])
        time.sleep(1)
        ADBCommand.keyevent('KEYCODE_APP_SWITCH')
        time.sleep(3)
        ADBCommand.tap(535, 2220)
        ADBCommand.execute(['adb', 'shell', 'cmd', 'connectivity', 'airplane-mode', 'disable'])
        time.sleep(2)
        AppManager.clear_app(clear_package) if clear_package else None
        time.sleep(5)
        Logger.log_success("IP CHANGE", "IP address has been changed successfully")


class NetworkHelper:
    @staticmethod
    def toggle_airplane_mode():
        status = ADBCommand.execute(['adb', 'shell', 'cmd', 'connectivity', 'airplane-mode'], capture=True)
        if "enabled" in (status.stdout or ""):
            Logger.log_warning("AIRPLANE", "Disabling airplane mode")
            ADBCommand.execute(['adb', 'shell', 'cmd', 'connectivity', 'airplane-mode', 'disable'])
        elif "disabled" in (status.stdout or ""):
            Logger.log_warning("AIRPLANE", "Enabling airplane mode")
            ADBCommand.execute(['adb', 'shell', 'cmd', 'connectivity', 'airplane-mode', 'enable'])
        return True
    
    @staticmethod
    def change_ip_address():
        Logger.log_warning("IP CHANGE", "Toggling airplane mode to change IP address")
        ADBCommand.execute(['adb', 'shell', 'cmd', 'connectivity', 'airplane-mode', 'disable'])
        ADBCommand.execute(['adb', 'shell', 'cmd', 'connectivity', 'airplane-mode', 'enable'])
        ADBCommand.execute(['adb', 'shell', 'cmd', 'connectivity', 'airplane-mode', 'disable'])
        time.sleep(5)
        Logger.log_success("IP CHANGE", "IP address change process completed")
        return True

def exists(name, timeout=5000, thresh=0.8, prefix="images/", suffix=".png", region=None, tl=None, br=None, description=None, wait_before=0, wait_after=0, fatal_error=False):
    return DeviceHelper.exists(name, timeout, thresh, prefix, suffix, region, tl, br, description, wait_before, wait_after, fatal_error)

def touch(name, timeout=10000, thresh=0.8, prefix="images/", suffix=".png", dur=0, region=None, tl=None, br=None, wait_before=0, wait_after=0, description=None, ss_path=None):
    return DeviceHelper.touch(name, timeout, thresh, prefix, suffix, dur, region, tl, br, wait_before, wait_after, description, ss_path)

def wait(sec): Logger.log_info("WAIT", f"Waiting for {sec} seconds"); time.sleep(sec)

def home(): Logger.log_info("HOME", "Pressing Home button"); ADBCommand.execute(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])

def back(): Logger.log_info("BACK", "Pressing Back button"); ADBCommand.execute(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_BACK'])

def keyevent(k, description=None): Logger.log_info("KEYEVENT", f"Sending key '{k}'"); ADBCommand.execute(['adb', 'shell', 'input', 'keyevent', k])

def shell(cmd, description=None): DeviceHelper.run_shell_command(cmd, description)

def swipe(sx, sy, ex, ey, dur=300, wait_before=0, wait_after=0, description=None): DeviceHelper.swipe(sx, sy, ex, ey, dur, wait_before, wait_after, description)

def text(txt, submit=False, wait_before=0, wait_after=0, description=None): DeviceHelper.input_text(txt, submit, wait_before, wait_after, description)

def paste(submit=False, wait_before=0, wait_after=0, description=None): DeviceHelper.paste_from_clipboard(submit, wait_before, wait_after, description)

def screenshot(path): DeviceHelper.take_screenshot(path)

def start_app(pkg, clear_before=False): Logger.log_success("START", f"Launching app '{pkg}'"); clear_app(pkg) if clear_before else None; ADBCommand.execute(['adb', 'shell', 'monkey', '-p', pkg, '-c', 'android.intent.category.LAUNCHER', '1'])

def stop_app(pkg): Logger.log_warning("STOP", f"Stopping app '{pkg}'"); ADBCommand.execute(['adb', 'shell', 'am', 'force-stop', pkg])

def clear_app(pkg): Logger.log_info("CLEAR", f"Clearing app data for '{pkg}'"); ADBCommand.execute(['adb', 'shell', 'pm', 'clear', pkg])

def install_app(apk): AppManager.install_app(apk)

def uninstall_app(pkg): AppManager.uninstall_app(pkg)

def clear_recent_apps(clear_package=None, windscribe=False): AppManager.clear_recent_apps(clear_package, windscribe)

def clear_recent_apps_and_change_ip(clear_package=None): AppManager.clear_recent_apps_and_change_ip(clear_package)

def notifications_open(): ADBCommand.notification('open', "Opened notification drawer")

def notifications_close(): ADBCommand.notification('close', "Closed notification drawer")

def notifications_clear(): ADBCommand.notification('clear', "Cleared all notifications")

def toggle_airplane_mode(): NetworkHelper.toggle_airplane_mode()

def change_ip_address(): NetworkHelper.change_ip_address()

def reboot(): Logger.log_warning("REBOOT", "Initiating device reboot"); ADBCommand.execute(['adb', 'reboot'])

def message(message="", color="WHITE"): Logger.message(message, color) 