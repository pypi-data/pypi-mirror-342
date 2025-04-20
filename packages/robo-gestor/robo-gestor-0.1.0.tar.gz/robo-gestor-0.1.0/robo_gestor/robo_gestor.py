import uiautomator2 as u2
import time
from functools import wraps

def delay_execution(func):
    """
    Decorator to add a 2-second delay before executing a function.
    Useful for allowing UI transitions to complete.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(2)
        return func(*args, **kwargs)
    return wrapper

class RoboGestor:
    """
    RoboGestor automates interactions with Android devices via uiautomator2.
    It can start/stop apps, unlock the screen, click UI elements, 
    retrieve screen text, and execute ADB shell commands.
    """

    def __init__(self, ip=""):
        """
        Initialize RoboGestor with optional IP address for remote connection.
        If no IP is provided, it connects to the default device.
        """
        self.phone = u2.connect(ip) if ip else u2.connect()

    @delay_execution
    def open_app(self, package_name):
        """
        Launch the specified application by its package name.
        """
        self.phone.app_start(package_name)

    def close_app(self, package_name):
        """
        Force-stop the specified application by its package name.
        """
        self.phone.app_stop(package_name)

    def unlock_phone(self):
        """
        Unlock the phone screen if it is locked.
        """
        self.phone.unlock()

    def lock_with_power_button(self):
        """
        Lock the phone by simulating the power button press.
        """
        self.phone.press("power")

    @delay_execution
    def swipe_up_to_unlock(self, device_ip=None):
        """
        Perform a swipe-up gesture to unlock the screen.
        """
        if not self.phone.info.get('screenOn'):
            self.phone.screen_on()

        width, height = self.phone.window_size()
        start_x = width / 2
        start_y = height * 0.8
        end_x = width / 2
        end_y = height * 0.2

        self.phone.swipe(start_x, start_y, end_x, end_y, duration=0.2)

    @delay_execution
    def find_and_click_text(self, target_text, device_ip=None, max_swipes=10):
        """
        Find a text element on screen and click it.
        If not found, swipe up and retry until max_swipes is reached.
        """
        for attempt in range(max_swipes):
            if self.phone(text=target_text).exists:
                time.sleep(1)
                self.phone(text=target_text).click()
                print(f"✅ Found and clicked: '{target_text}'")
                return True
            else:
                print(f"🔍 '{target_text}' not found, swiping up... ({attempt+1}/{max_swipes})")
                self.phone.swipe_ext("up", scale=0.8)
        print(f"❌ Failed to find '{target_text}' after {max_swipes} swipes.")
        return False

    def get_toggle_state(self, target_text):
        """
        Get the ON/OFF state of an Android Switch next to a specific text.
        Returns True (ON) or False (OFF).
        """
        toggle = self.phone(text=target_text).right(className="android.widget.Switch")
        return toggle.info.get("checked", False)

    @delay_execution
    def bring_text_into_view(self, target_text, device_ip=None, max_swipes=10):
        """
        Bring the target text into visible screen area by swiping until found or limit reached.
        """
        for attempt in range(max_swipes):
            if self.phone(text=target_text).exists:
                print(f"✅ Found '{target_text}'")
                return True
            else:
                print(f"🔍 '{target_text}' not found, swiping up... ({attempt+1}/{max_swipes})")
                self.phone.swipe_ext("up", scale=0.8)
        print(f"❌ Failed to find '{target_text}' after {max_swipes} swipes.")
        return False

    def scroll_to_top(self):
        """
        Scroll a scrollable view back to the top using fling gesture.
        """
        scroll_obj = self.phone(scrollable=True)
        if scroll_obj.exists:
            scroll_obj.fling.toBeginning()
            print("✅ Scrolled to the top!")
        else:
            print("❌ No scrollable element found on this page.")

    def getDevice(self):
        """
        Return the connected uiautomator2 device instance.
        """
        return self.phone

    def check_text_on_view(self, target_text):
        """
        Check if a given text element is visible on the screen.
        Returns True if found, False otherwise.
        """
        return self.phone(text=target_text).exists

    def send_keys(self, keys):
        """
        Send keystrokes to the device, similar to typing.
        """
        self.phone.send_keys(keys)

    def click_text_in_viewport(self, target_text):
        """
        Click a text element if it is present in the current viewport.
        """
        if self.phone(text=target_text).exists:
            self.phone(text=target_text).click()
        else:
            print("❌ Text not found on screen.")

    def get_screen_text(self):
        """
        Return a list of all text elements currently visible on the screen.
        """
        xml = self.phone.dump_hierarchy()
        texts = []
        for node in self.phone.xpath("//*").all():
            text = node.attrib.get('text')
            if text:
                texts.append(text)
        return texts

    def run_command_in_device_shell(self, cmd):
        """
        Execute a shell command on the Android device and return the output as a list of lines.
        """
        return self.phone.shell(cmd).output.split("\n")
robot = RoboGestor()
robot.unlock_phone()