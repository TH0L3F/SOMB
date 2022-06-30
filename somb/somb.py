"""
# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8 compliant>

# Contributors: Bill L.Nieuwendorp
"""
"""
This script Exports Multiple object to Lightwaves MotionDesigner format.

The .mdd format has become quite a popular Pipeline format<br>
for moving animations from package to package.

Be sure not to use modifiers that change the number or order of verts in the mesh
"""

#from bpy import bpy #blender associate to python librairie
#import mathutils
from struct import pack
     
def str5fromint(a):
    
    n5 = int(a/10000)
    n4 = int((a-n5*10000)/1000)
    n3 = int((a-n5*10000-n4*1000)/100)
    n2 = int((a-n5*10000-n4*1000-n3*100)/10)
    n1 = int((a-n5*10000-n4*1000-n3*100-n2*10))
    return str(n5)+str(n4)+str(n3)+str(n2)+str(n1)

def check_v(frame_name,vp):
    
    #On compte le nombre de sommets
    som = 0;
    f = open(frame_name, 'r')
    fobjtab = f.readlines()
    sw = 0 #Permet d'identifier si on fait l'état d'un nouvelle objet
    ex_obj_t = []
    
    for i in range(len(fobjtab)):
        ligne = fobjtab[i]
        if(len(ligne)>2):
            if((ligne[0] == 'v') & (ligne[1] == ' ')):
                if(sw == 0):
                    ex_obj_t.append([i])
                sw = 1 #on le met à 1 pour signifier qu'on passe dans une nouvelle zone de définition des sommets
                som = som+1               
            else:
                if(sw == 1):
                    ex_obj_t[len(ex_obj_t)-1].append(i)
                sw = 0 #on le met à 0 pour signifier qu'on sort d'une zone de défintion des sommet             
                
    f.close()
    
    if(vp == 0): #Si vp = 0 c'est qu'il a pas encore était défini on le défini donc
        #print(som)
        return som       
    else: #Sinon on vérifie que le nombre de sommets n'a pas changé
        if(vp != som):
            raise Exception('Erreur, le nombre de sommets à changer')
    return som,ex_obj_t

def save(addr_folder="",filepath="", frame_start=0, frame_end=300, fps=25.0):
    
    f = open(filepath, 'wb')  #On créer le fichier en écriture au format binaire
    numframes = frame_end - frame_start #On définit le nombre total de frame à parcourir lors de la conversion en .mdd
    
    #string contenant le nom du premier fichier à ouvrir
    frame_name = addr_folder+"caduceus_"+str5fromint(frame_start)+".obj"       
    
    #On définit pour la première fois le nombre de sommet de l'objet
    vp=0    
    vp = check_v(frame_name,vp)
    
    # Ecriture de l'entête du fichier .mdd
    #pack(format,v1,v2,...) permet de convertir les données dans le bon format
    f.write(pack(">2i", numframes,vp)) #On entre dans le fichier le nombre d'image et de sommets
    
    # On écrit le temps d'affichage d'une frame
    f.write(pack(">%df" % (numframes), *[frame / fps for frame in range(numframes)])) # en seconds
    
    #On enregistre désormais chaques objets un a un   
    for frame in range(frame_start, frame_end):  # in order to start at desired frame
        
        #On créer le string contenant le nom des fichier à ouvrir correspondant à la frame actuel
        frame_name_1 = addr_folder+"caduceus_"+str5fromint(frame)+".obj"       
        frame_name_2 = addr_folder+"caduceus_"+str5fromint(frame+1)+".obj"      
        fobj_1 = open(frame_name_1, 'r')
        fobj_2 = open(frame_name_2, 'r')
        print(frame_name_1 + " : " + frame_name_2)
        
        #On vérifie que le nombre de sommet n'a pas changé et on cherche leurs positions dans le fichier
        vp,ex_obj_t = check_v(frame_name_2,vp)
        
        #On converti les fichiers en tableaux
        fobj_1_tab = fobj_1.readlines()
        fobj_2_tab = fobj_2.readlines()

        sum = 0
        for i in ex_obj_t:
            for y in range(i[0],i[1]):
                sum = sum +1
                #On écrit le résultat sous le bon format dans le fichier
                #le > pour big endian
                #le d pour double float (8 octets)
                #le f pour float (4 octets)
                coord_1 = fobj_1_tab[y].split(" ")
                coord_2 = fobj_2_tab[y].split(" ")
                
                vx = float(coord_2[1]) - float(coord_1[1])
                vy = float(coord_2[2]) - float(coord_1[2])
                vz = float(coord_2[3]) - float(coord_1[3])             
                
                """if(y < 50):
                    print(vx,pack('>f',vx))
                """
                    
                f.write(pack('>3f',vz,vy,vx)) #écriture de la variation en x,y et z
                
        fobj_1.close()
        fobj_2.close()
        
    f.close()#On ferme le fichier maintenant qu'il est remplie
    
    #On écrit un message permettant à l'utilisateur de savoir que le fichier a bien était exporter et où
    print('MDD Exported: %r frames:%d\n' % (filepath, numframes)) 
