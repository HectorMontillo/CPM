import wx 
import constantes as c
import modelo as mo

class IndexFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title=c.CAPTION, size=c.SIZE, 
            style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.proyecto = mo.Proyecto("default")
        
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
        #TITULO----------------------------------
        titulo = wx.StaticText(panel, -1, label=c.CAPTION, pos=(32,32))
        titulo.SetFont(font)
        #SEPARADORES------------------------------
        separator = wx.StaticLine(panel, -1, pos=(32, 56),size=(c.ANCHO-96,-1), style=wx.LI_HORIZONTAL)
        separator1 = wx.StaticLine(panel, -1, pos=(32, c.ALTO-64),size=(c.ANCHO-96,-1), style=wx.LI_HORIZONTAL)

        #BOTONES-----------------------------------
        BtnAgregarActividad = wx.Button(panel,label="Agregar actividad",pos=(c.ANCHO-128-64,32-16),size=(128,32))
        self.Bind(wx.EVT_BUTTON, self.AgregarActividad, BtnAgregarActividad)

        BtnGraficarRed = wx.Button(panel,label="Graficar Red",pos=(c.ANCHO-128-64,c.ALTO-144),size=(128,32))
        self.Bind(wx.EVT_BUTTON, self.GraficarRed, BtnGraficarRed)

        BtnCPM = wx.Button(panel,label="CPM",pos=(32,c.ALTO-144),size=(128,32))
        self.Bind(wx.EVT_BUTTON, self.CPM, BtnCPM)
        #LISTADO ACTIVIDADES-----------------------
        self.TAConsola = wx.TextCtrl(panel, id=wx.ID_ANY, value="No ha agregado actividades", pos=(32, 96), size=(c.ANCHO-96, c.ALTO-256), style=wx.TE_MULTILINE | wx.TE_RICH)
        #VALOR RUTA CRITICA------------------------
        '''
        self.LRutaCriticaValue = wx.StaticText(panel, -1, label="Duracion del proyecto: ", pos=(32,c.ALTO-144))
        self.LRutaCritica = wx.StaticText(panel, -1, label="Ruta Critica: ", pos=(32,c.ALTO-144+32))
        '''
        #FRAMES
        self.FAgregarActividad = AgregarActividadFrame(self, -1, c.ANCHO_A, c.ALTO_A,self.proyecto)

    def AgregarActividad(self,event):
        print("Agregando Actividad")
        self.FAgregarActividad.Show(True)


    def GraficarRed(self,event):
        self.proyecto.DibujarRed()
    
    def CPM(self,event):

        self.proyecto.Cpm('m')
        self.TAactualizar()
    
    def TAactualizar(self):
        self.TAConsola.SetValue("")
        rutacritica = list(self.proyecto.rutacritica)
        dura = str(self.proyecto.DuracionProyecto())
        for act in self.proyecto.actividades:
            self.TAConsola.WriteText(str(act)+"\n")
        self.TAConsola.WriteText("Duracion del proyecto: "+dura+"\n")       
        self.TAConsola.WriteText("Ruta Critica: "+str(rutacritica)+"\n")

class AgregarActividadFrame(wx.Frame):
    def __init__(self, parent, id, ancho, alto, proyecto):
        wx.Frame.__init__(self, parent, id, title=c.CAPTION_A, size=(ancho, alto),
                style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.CLOSE_BOX))
        self.proyecto = proyecto
        self.iniciarinterfaz()
    
    def iniciarinterfaz(self):
         #PANEL----------------------------------
        panel = wx.Panel(self)
        #Fuentes--------------------------------
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        font2 = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font2.SetPointSize(8)
        #TITULO----------------------------------
        titulo = wx.StaticText(panel, -1, label=c.CAPTION_A, pos=(32,32))
        titulo.SetFont(font)
        #SEPARADORES------------------------------
        separator = wx.StaticLine(panel, -1, pos=(32, 56),size=(c.ANCHO_A-64,-1), style=wx.LI_HORIZONTAL)
        #CAMPOS DE TEXTO--------------------------
        wx.StaticText(panel, -1, label="Nombre Actividad:", pos=(32, 64))
        self.TFNombre = wx.TextCtrl(panel, id=wx.ID_ANY, value="A", pos=(192, 64), size=(c.ANCHO_A-228, -1))
        wx.StaticText(panel, -1, label="Tiempo optimo:", pos=(32, 96))
        self.TFTiempoOptimo = wx.TextCtrl(panel, id=wx.ID_ANY, value="no disponible", pos=(192, 96), size=(c.ANCHO_A-228, -1))
        wx.StaticText(panel, -1, label="Tiempo probable:", pos=(32, 128))
        self.TFTiempoProbable = wx.TextCtrl(panel, id=wx.ID_ANY, value="1", pos=(192, 128), size=(c.ANCHO_A-228, -1))
        wx.StaticText(panel, -1, label="Tiempo tardio:", pos=(32, 160))
        self.TFTiempoTardio = wx.TextCtrl(panel, id=wx.ID_ANY, value="no disponible", pos=(192, 160), size=(c.ANCHO_A-228, -1))
        wx.StaticText(panel, -1, label="Actividades Predecesoras:", pos=(32, 192))
        self.TFPredecesoras = wx.TextCtrl(panel, id=wx.ID_ANY, value="A", pos=(192, 192), size=(c.ANCHO_A-228, -1))
        
        #BOTONES------------------------------------
        BtnAgregar = wx.Button(panel, label="Agregar", pos=(c.ANCHO_A-128, c.ALTO_A-96), size=(96, 32))
        self.Bind(wx.EVT_BUTTON, self.Agregar, BtnAgregar)
       

        #DIALOGOS-------------------------------------
        self.MDAlerta = wx.MessageDialog(self,"No se pudo agregar la actividad")
    

        

    def Agregar(self,event):

        result = self.proyecto.agregaractividad(self.TFNombre.GetValue(),float(self.TFTiempoProbable.GetValue()),
                self.proyecto.BuscarActividad(self.TFPredecesoras.GetValue()))

        if result==0:
            self.MDAlerta.ShowModal()    

            print("No se pudo agregar la actividad")
        else:
            #self.proyecto.Cpm('m')
            '''
            frame.TAConsola.SetValue("")
            rutacritica = list(reversed(list(self.proyecto.rutacritica)))
            dura = str(self.proyecto.DuracionProyecto())
            for act in self.proyecto.actividades:
                frame.TAConsola.WriteText(str(act)+"\n")
            frame.TAConsola.WriteText("Duracion del proyecto: "+dura+"\n")       
            frame.TAConsola.WriteText("Ruta Critica: "+str(rutacritica)+"\n")
            '''
            frame.TAactualizar()

            print("Actividad Agregada")
        self.Show(False)


        



if __name__=="__main__":
    app = wx.App()
    frame = IndexFrame(None, -1)
    frame.Show()
    app.MainLoop()
