# Virgo cluster gas visualizations - M. SubbaRao May 2011
#
# Box will be: 
# x = from 180 < RA 195 with center at 187.5
# y = 4 deg < dec < 16 with center at 10 deg
# (1 deg/unit for both?)
# z = (v - 1500)/400
#
# Different elements will be separated in layers:
# Layer 1: Lights, Cameras, Coordinate box and labels
# Layer 2: Alfalfa detections cooresponding to galaxies
# Layer 3: Alfalfa detections not cooresponding to galaxies
# Layer 4: Alfalfa binary cube 2.4 deg x 2.4 deg containing 500 kpc tail structure
# Layer 5: QSO sightlines
# Layer 6: HI systems

import bpy
import math

#Model Constants
cylSize=0.1
sphSize=0.0002
absLength=0.5

#Datapath
datapath="/Users/msubbarao/Documents/Visualizations/Virgo/modelData/"
#Other constants
PI=3.1415926
c=299792.
#create materials
matHI=bpy.data.materials.new("matHI")
def makeSightLines():
  #create materials
  matLoS=bpy.data.materials.new("matLoS")
  datafile=datapath+"COSobs.txt"
  for line in open(datafile):
      if line[0]!="#":
         lineElements = line.split()
         if len(lineElements) > 0:
            RA=float(lineElements[2])
            dec=float(lineElements[3])
            x=getx(RA)
            y=gety(dec)
            bpy.ops.mesh.primitive_cylinder_add(radius=cylSize, depth = 6.5, cap_ends=False, location=(x,y,0.5),rotation=(0.,0,0))
            gal = bpy.context.object
            bpy.ops.object.material_slot_add()  
            gal.name = lineElements[0]
            bpy.ops.object.shade_smooth()
            gal.material_slots[0].material=matLoS
            bpy.ops.object.move_to_layer(layers=(False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) 
            #Plot Absorbers
            listName = datapath +  lineElements[len(lineElements)-1] + ".txt"
            plotAbsorbers(RA,dec,listName)

                  
def makeHISpheres():
  #create materials
  matGal=bpy.data.materials.new("matGal")
  matGas=bpy.data.materials.new("matGas")
  #read datafile
  datafile=datapath+"ALFALFA_volume.txt"
  for line in open(datafile):
      if line[0]!="#":
         lineElements = line.split()
         if len(lineElements) > 0:
            v=float(lineElements[6])
            RA=float(lineElements[2])*15.
            dec=float(lineElements[3])
            logMHI=float(lineElements[8])
            MHI=math.pow(10.,logMHI)
            radius=sphSize*math.pow(MHI,0.33333)
            x=getx(RA)
            y=gety(dec)
            z=getz(v)
            if (v>450. and v <4500):
                bpy.ops.mesh.primitive_uv_sphere_add(size=radius,location=(x,y,z))
                bpy.ops.object.material_slot_add()
                gal = bpy.context.object
                gal.name = "alfalfa_" + lineElements[0]
                bpy.ops.object.shade_smooth()
                # Place on layer 2
                if (lineElements[4]=="0.0000"):
                    bpy.ops.object.move_to_layer(layers=(False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) 
                    gal.material_slots[0].material=matGas
                else:
                    bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) 
                    gal.material_slots[0].material=matGal
               
def plotAbsorbers(RA,dec,datafile):
#make cylinder segments at the position of each absorber
    print(datafile)
    for line in open(datafile):
        if line[0]!="#":
            lineElements = line.split()
            if len(lineElements) > 0:
                redshift=float(lineElements[3])
                v=c*redshift
                #only include absorbers in Virgo Cluster
                if (v>450. and v <3500):
                    x=getx(RA)
                    y=gety(dec)
                    z=getz(v)
                    transition=lineElements[1]
                    reference=lineElements[2]
                    print(transition,reference,v)
                    if (transition=="HI" and reference=="1215"):
                        #Place on layer 6
                        print(transition, lineElements[4])
                        print(line)
                        width=float(lineElements[4].lstrip("W="))
                        bpy.ops.mesh.primitive_cylinder_add(radius=cylSize*.95, depth = absLength*width, cap_ends=True, location=(x,y,z),rotation=(0.,0,0))
                        bpy.ops.object.material_slot_add()
                        gal=bpy.context.object
                        gal.name = "absorber_HI"
                        bpy.ops.object.move_to_layer(layers=(False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) 
                        gal.material_slots[0].material=matHI

                    
def getx(RA): 
    x=187.5-RA
    return(x)
def gety(dec):
    y=dec-10.
    return(y)
def getz(v):
    z=(2000-v )/400.
    return(z)



