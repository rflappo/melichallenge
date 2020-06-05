import os
from configparser import ConfigParser


class FileParserConfig:
    def __init__(self):
        config = ConfigParser()
        config_file = os.path.join(os.getcwd(), 'parserconfig.ini')
        config.read(config_file)

        self.settings = {}
        if 'FILE' in config.sections():
            self.settings = config['FILE']

    def file_with_headers(self):
        if 'HEADERS_LINE' in self.settings.keys():
            return self.settings['HEADERS_LINE'].lower() == 'true'
        return False

    def get_encoding(self):
        if 'ENCODING' in self.settings.keys():
            return self.settings['ENCODING'].lower()
        return 'utf-8'

    def get_allowed_extension(self):
        if 'EXTENSION' in self.settings.keys():
            return self.settings['EXTENSION'].lower()
        return 'text'


class LineParserConfig:
    def __init__(self):
        config = ConfigParser()
        config_file = os.path.join(os.getcwd(), 'parserconfig.ini')
        config.read(config_file)

        self.settings = {}
        if 'LINE' in config.sections():
            self.settings = config['LINE']
    
    def get_line_feed(self):
        line_feed = '\n'

        is_there = 'LINE_FEED' in self.settings.keys()
        if is_there and self.settings['LINE_FEED'].lower() != 'unix':
            line_feed == '\r\n'
        
        return line_feed

    def get_separator(self):
        if 'SEPARATOR' in self.settings.keys():
            return self.settings['SEPARATOR']
        return ','

    def get_parse_module(self):
        parse_module = None

        is_there = 'MODULE' in self.settings.keys()
        if is_there and self.settings['MODULE'].lower() != 'none':
            parse_module = self.settings['MODULE']

        return parse_module
    
    def get_parse_method(self):
        parse_method = None

        is_there = 'METHOD' in self.settings.keys()
        if is_there and self.settings['METHOD'].lower() != 'none':
            parse_method = self.settings['METHOD'].lower()

        return parse_method