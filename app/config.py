from app import app
import yaml


class Config:
    __instance = None

    @staticmethod
    def get_instance():
        if Config.__instance is None:
            Config()
        app.logger.info("Config instance requested.")
        return Config.__instance

    def __init__(self):
        if Config.__instance is not None:
            app.logger.error("Additional config instances attempted to load.")
        else:
            self.data, self.debug_mode = None, None
            Config.__instance = self
            app.logger.info("New config instance generated.")
            self.set_fallbackdata()
            self.load_config()
            self.parse_config()
            if self.debug_mode:
                app.logger.warn("Debug mode is active.")
            self.write_config()

    def load_config(self):
        try:
            with open("config.yaml", "r") as config_file:
                self.data = yaml.load(config_file)
                config_file.close()
            app.logger.info("Config file loaded successfully.")
        except (IOError, FileNotFoundError):
            app.logger.warning("Config file not loaded, resorting to fallback parameters.")
            self.data = {}

    def dump_config(self):
        config_dict = {"Debug": self.debug_mode}
        app.logger.info("Config json dumped.")
        return yaml.dump(config_dict, indent=2)

    def write_config(self):
        try:
            with open("config.json", 'w') as config_writer:
                config_writer.write(self.dump_config())
                config_writer.close()
            app.logger.info("Config write was succesful.")
        except Exception as e:
            app.logger.error("Config file could not be saved.")

    def set_fallbackdata(self):
        self.fallbackdata = {"Debug": False}
        app.logger.info("Fallback configuration data set.")

    def parse_config(self):
        if bool(self.data.get("Debug")) is not None:
            self.debug_mode = bool(self.data.get("Debug"))
            app.logger.info("Debug setting loaded from configuration.")
        else:
            self.debug_mode = bool(self.fallbackdata.get("Debug"))
            app.logger.warning("Debug setting loaded from fallback.")

    def get_debugmode(self):
        return self.debug_mode
