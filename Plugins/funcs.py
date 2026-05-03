from colorama import init
from pystyle import Colorate, Colors, Center, Col, Add, Anime

from Plugins.logger import Logger
from Plugins.colors import Palette



palette = Palette()



class Funcs:
    
    @staticmethod
    def get_input(text: str, checker=lambda _: True):
        
        
        
        text = f"{palette.red}{text}{palette.better_grassy_green}"

        validator = checker if callable(checker) else (lambda _: bool(checker))

        v = input(text)
        if not validator(v):
            while not validator(v):
                Logger.Error.error("Try Again")
                v = input(text)
        
        return v
    
    @staticmethod
    def print_logo():
        logo = """
      █████╗ ██╗  ██╗███╗   ███╗███████╗██████╗ 
     ██╔══██╗██║  ██║████╗ ████║██╔════╝██╔══██╗
     ███████║███████║██╔████╔██║█████╗  ██║  ██║
     ██╔══██║██╔══██║██║╚██╔╝██║██╔══╝  ██║  ██║
     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██████╔╝
     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═════╝ 
                 Ahmed
        """


        print(Colorate.Vertical(Colors.DynamicMIX((Col.red, Col.dark_red)), logo))