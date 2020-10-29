import os


class mapping:
    def __init__(self, controller_keyboard=None):
        self.default_key_mappings = "./default_mappings.ini"
        if controller_keyboard is None:
            self.controller_keyboard = {
                "BTN_Y": None,
                "BTN_B": None,
                "BTN_A": None,
                "BTN_X": None,
                "BTN_L": None,
                "BTN_R": None,
                "BTN_ZL": None,
                "BTN_ZR": None,
                "BTN_MINUS": None,
                "BTN_PLUS": None,
                "BTN_LCLICK": None,
                "BTN_RCLICK": None,
                "BTN_HOME": None,
                "BTN_CAPTURE": None,
                "DPAD_U": None,
                "DPAD_R": None,
                "DPAD_D": None,
                "DPAD_L": None,
                "LSTICK_R": None,  # 0 (000)
                "LSTICK_U": None,  # 90 (05A)
                "LSTICK_L": None,  # 180 (0B4)
                "LSTICK_D": None,  # 270 (10E)
                "RSTICK_R": None,  # 0 (000)
                "RSTICK_U": None,  # 90 (05A)
                "RSTICK_L": None,  # 180 ()# 180 (0B4)
                "RSTICK_D": None,
            }
            self.read_key_mappings(self.default_key_mappings)
        else:
            self.controller_keyboard = controller_keyboard
        self.keyboard_controller = {v: k for k, v in self.controller_keyboard.items()}
        pass

    def read_key_mappings(self, inipath):
        with open(inipath, "r") as f:
            # self.key_mappings = {}
            for line in f:
                target_button = line.split(" ")[0]
                user_key = line.split(" ")[-1][:-1]
                if user_key != "None":
                    self.controller_keyboard[target_button] = user_key

        self.keyboard_controller = {v: k for k, v in self.controller_keyboard.items()}
        # return key_mappings

    def save_mapping_ini(self, filename):
        path = os.path.join("mapping", filename)
        with open(path, "w+") as f:
            for k, v in self.controller_keyboard.items():
                f.write("{} {}\n".format(v, k))
