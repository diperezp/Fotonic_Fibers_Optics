from OMS.wave.simetric_slab import SimetricSlabWave
import numpy as np
import matplotlib.pyplot as plt


class field_wave_guide:
    def __init__(self, Slab_wave: SimetricSlabWave):
        self.slab_wave = Slab_wave


        #Constantes
        self.miu_0 = 4 * np.pi * 1e-7 #Permeabilidad del vacío
        self.omega = 2 * np.pi * 3e8 / self.slab_wave.wavelength #Frecuencia angular de la luz
        #calculamos los modos guiados
        self.modes = self.slab_wave.find_modes_wave()
        self.x = np.linspace(-5*self.slab_wave.h, 5*self.slab_wave.h, 1000)
        self.z = np.linspace(0, 10*self.slab_wave.h, 1000)
        mesh_x, mesh_z = np.meshgrid(self.x, self.z)
        self.E = np.array([None] * len(self.modes))
        self.H = np.array([None] * len(self.modes))

        #evaluamos cual es el



    def calculate_fields_1D(self):
        #evaluamos si es TE o TM
        if self.slab_wave.polarization == "TE":
            i=0
            for mode in self.modes:
                if(i%2==0):
                    self.E[i] = np.piecewise(self.x, [np.abs(self.x)<=self.slab_wave.h/2,np.abs(self.x)>self.slab_wave.h/2],[lambda x: np.cos(mode*x*self.slab_wave.h/2), lambda x: np.exp(-self.slab_wave.ecuation_characteristic_even(mode)*self.slab_wave.h/2(np.abs(x)-self.slab_wave.h/2))])
                else:
                    self.E[i] = np.piecewise(self.x,[self.x<-self.slab_wave.h/2,np.abs(self.x)<=self.slab_wave.h/2,self.x>self.slab_wave.h/2],[lambda x: -np.exp(self.slab_wave.ecuation_characteristic_odd(mode)*self.slab_wave.h/2*(x+self.slab_wave.h/2)), lambda x: np.sin(mode*x*self.slab_wave.h/2), lambda x: np.exp(-self.slab_wave.ecuation_characteristic_odd(mode)*self.slab_wave.h/2*(x-self.slab_wave.h/2))])
                i+=1
        elif self.slab_wave.polarization == "TM":
            i=0
            for mode in self.modes:
                if(i%2==0):
                    self.H[i] = np.piecewise(self.x, [np.abs(self.x)<=self.slab_wave.h/2,np.abs(self.x)>self.slab_wave.h/2],[lambda x: np.cos(mode*x*self.slab_wave.h/2), lambda x: np.exp(-self.slab_wave.ecuation_characteristic_even(mode)*self.slab_wave.h/2(np.abs(x)-self.slab_wave.h/2))])
                else:
                    self.H[i] = np.piecewise(self.x,[self.x<-self.slab_wave.h/2,np.abs(self.x)<=self.slab_wave.h/2,self.x>self.slab_wave.h/2],[lambda x: -np.exp(self.slab_wave.ecuation_characteristic_odd(mode)*self.slab_wave.h/2*(x+self.slab_wave.h/2)), lambda x: np.sin(mode*x*self.slab_wave.h/2), lambda x: np.exp(-self.slab_wave.ecuation_characteristic_odd(mode)*self.slab_wave.h/2*(x-self.slab_wave.h/2))])
                i+=1

        

