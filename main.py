import flet as ft
from ui.views.home_view import HomeView

class App(ft.Container):
# ---------------------------------------- CONTROLES ----------------------------------------
   def __init__(self, page):
      super().__init__()
      self.page = page
 
 
      self.content = HomeView(self.page)
 
# ---------------------------------------- GRAPHICS ---------------------------------------- 
   def build(self):
      self.page.window.width = 800
      self.page.window.height = 600
      self.page.add(self.content)
 
# ---------------------------------------- FUNCIONES ---------------------------------------- 
 
 
def main(page: ft.Page):
   app = App(page)
   app.build()
 
if __name__ == '__main__':
   ft.app(target = main)
