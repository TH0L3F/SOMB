"""
# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8 compliant>

# Contributors: Bill L.Nieuwendorp, Thomas Lefranc
"""
"""
Ce programme permet de convertir un .obj contenant plusieurs objets en objets
individuelles tous liés à leurs propres fichiers .mdd
"""

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
        return som,ex_obj_t    
    else: #Sinon on vérifie que le nombre de sommets n'a pas changé
        if(vp != som):
            raise Exception('Erreur, le nombre de sommets à changer')
    return som,ex_obj_t

#def floattohex(v):
    
#def midendian(tab):

def save(addr_folder="",filepath="", frame_start=0, frame_end=300, fps=25.0):
    
    f = open(filepath, 'wb')  #On créer le fichier en écriture au format binaire
    numframes = frame_end - frame_start +1 #On définit le nombre total de frame à parcourir lors de la conversion en .mdd
    
    #string contenant le nom du premier fichier à ouvrir
    frame_name = addr_folder+"caduceus_"+str5fromint(frame_start)+".obj"       
    
    #On définit pour la première fois le nombre de sommet de l'objet
    vp=0    
    vp,ex_obj_t = check_v(frame_name,vp)
    
    # Ecriture de l'entête du fichier .mdd
    #pack(format,v1,v2,...) permet de convertir les données dans le bon format
    f.write(pack(">2i", numframes,vp)) #On entre dans le fichier le nombre d'image et de sommets
    
    # On écrit le temps d'affichage d'une frame
    f.write(pack(">%df" % (numframes), *[frame / fps for frame in range(numframes)])) # en seconds
            
    #On enregistre désormais chaques objets un a un   
    for frame in range(frame_start, frame_end+1):  # in order to start at desired frame
        
        #On créer le string contenant le nom des fichier à ouvrir correspondant à la frame actuel
        frame_name = addr_folder+"caduceus_"+str5fromint(frame)+".obj"          
        fobj = open(frame_name, 'r')
        print(frame_name)
        
        #On vérifie que le nombre de sommet n'a pas changé et on cherche leurs positions dans le fichier
        vp,ex_obj_t = check_v(frame_name,vp)
        
        #On converti les fichiers en tableaux
        fobj_tab = fobj.readlines()

        for i in ex_obj_t:
            for y in range(i[0],i[1]):             
                coord = fobj_tab[y].split(" ")
                vx = float(coord[1])
                vy = float(coord[2])
                vz = float(coord[3])
                f.write(pack('>3f',vz,vy,vx)) #écriture de la variation en x,y et z
                
        fobj.close()
        
    f.close()#On ferme le fichier maintenant qu'il est remplie
    
    #On écrit un message permettant à l'utilisateur de savoir que le fichier a bien était exporter et où
    #print('MDD Exported: %r frames:%d\n' % (filepath, numframes)) 
