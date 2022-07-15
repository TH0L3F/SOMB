# SOMB

SOMB (Sofa Obj to MDD for Blender) est un programme python qui permet de traiter des OBJ produits par le logiciel SOFA lors d'une simulation pour en faire un fichier MDD qui peut être traiter par Blender.

> Plus spécifiquement il peut traiter une suite d'objet pour en faire un fichier mdd.

La commande à executer pour cela est :
>  save(addr_folder="",filepath="", frame_start=0, frame_end=300, fps=25.0)
>  * addr_folder l'adresse du dossier dans lequel se trouve les fichiers .OBJ.
>  *  filepath le nom du fichier .MDD que créer le programme.
>  *  frame_start le numéro du premier .OBJ que l'on veut utiliser.
>  *  frame_end le numéro du second .OBJ que l'on veut utiliser.
>  *  fps le nombre d'image par seconde de la simulation.
  
Exemple:
>  On peut prendre une dossier C:\\dossier_objet\ contenant les fichiers:
>  *  cadeuceus_00000.obj
>  *  cadeuceus_00001.obj
>  *  cadeuceus_00002.obj
>  *  cadeuceus_00003.obj
>  *  cadeuceus_00004.obj
>  *  cadeuceus_00005.obj
>  *  cadeuceus_00006.obj
 
> La commande:
>  >  save(addr_folder="C:\\dossier_objet\\",filepath="C:\\", frame_start=1, frame_end=5, fps=25.0)
>  >  Prend les fichiers objets de 1 à 5 pour en faire un fichier MDD à la racine du disque C
