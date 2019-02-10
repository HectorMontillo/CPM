import wx 
import constantes as c

class Index(wx.Frame):
    def __init__(self, parent, id, ancho, alto):
        wx.Frame.__init__(self, parent, id, title=c.CAPTION, size=c.SIZE, 
            style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        
        self.iniciarinterfaz()
    
    def iniciarinterfaz(self):
        print("Interfaz Inicializada")
        #PANEL----------------------------------
        panel = wx.Panel(self)
        #Fuentes--------------------------------
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        font2 = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font2.SetPointSize(8)

        titulo = wx.StaticText(panel, -1, label=c.CAPTION, pos=(32,32))
        titulo.SetFont(font)


if __name__=="__main__":
    app = wx.App()
    frame = Index(None, -1, 960, 512)
    frame.Show()

    app.MainLoop()
