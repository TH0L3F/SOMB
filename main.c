#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int puiss(int a, int b){
	int i = 1;
	if(b > 0){
		for(int y = 0; y<b; y++){
			i = i*a;
		}
		return i;
	}
	else{
		return i;
	}
}

int main(int argc,char * argv[]){
	if(argc != 4){
		printf("Erreur dans l'entrée de la commande\n");
		return -1;
	}
	//if(atoi(argv[2]) == 1 && atoi(argv[3])==1){
	//Dans le cas ou il y a une seule image
	//}
	
	//On ouvre les fichiers 2 à 2 pour les comparer
	char fichier1[512];//Contient le nom d'acces au fichier 1
	char fichier2[512];//Contient le nom d'acces au fichier 2
	int cnum; //Nombre intermédiaire de création
	int pos = 0;//position actuel lors de la création du nom du fichier puis position du premier numéro le reste du temps
	char header[10] = "caduceus_\0";
	char footer[5] = ".obj\0";
	char buffer[256];

	//On créer ici la trame principale 
	//route/../../caduceus_xxxxx.obj
	
	while(argv[1][pos] != '\0'){
		fichier1[pos] = argv[1][pos];
		fichier2[pos] = argv[1][pos];
		//printf("%c %d\n",fichier1[pos],pos);
		pos++;
	}
	for(unsigned int i=0; i<strlen(header);i++){
		fichier1[pos] = header[i];
		fichier2[pos] = header[i];
		//printf("%c %d\n",fichier1[pos],pos);
		pos++;
	}
	for(unsigned int i=0; i<5; i++){
		fichier1[pos] = '0';
		fichier2[pos] = '0';
		//printf("%c %d\n",fichier1[pos],pos);
		pos++;
	}
	for(unsigned int i=0; i<strlen(footer);i++){
		fichier1[pos] = footer[i];
		fichier2[pos] = footer[i];
		//printf("%c %d\n",fichier1[pos],pos);
		pos++;
	}
	fichier1[pos+1] = '\0';
	fichier2[pos+1] = '\0';

	pos = pos - 5 - strlen(footer);//Pour retrouver la position du premier numéro

	for(int i = atoi(argv[2]); i < atoi(argv[3]); i++){

                cnum = i;
		for(int y = 4; y>-1 ; y--){
                        fichier1[pos+4-y] = cnum/puiss(10,y) + 48;
                        cnum = cnum - (cnum/puiss(10,y))*puiss(10,y);
                }
		
                cnum = i+1;
                for(int y = 4; y>-1 ; y--){
                        fichier2[pos+4-y] = cnum/puiss(10,y) + 48;
                        cnum = cnum - (cnum/puiss(10,y))*puiss(10,y);
                }	
		
		printf("%s : %s\n",fichier1,fichier2);

		FILE * f1 = fopen(fichier1,"r");
		fgets(buffer,256,f1);
		printf("%s\n",buffer);
		FILE * f2 = fopen(fichier2,"r");
	       	fgets(buffer,256,f2);
		printf("%s\n",buffer);	
	}
}
