import disnake
from disnake.ext import commands

class HandleModal(disnake.ui.Modal):
    def __init__(self):
        self.platform = ""
        self.handle = ""
        component = []
    

