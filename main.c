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
	char num[5];//Contient le numéro du .obj
	int cnum; //Nombre intermédiaire de création
	int pos;

	for(int i = atoi(argv[2]); i < atoi(argv[3]); i++){
		fichier1[0] = '\0';
		fichier2[0] = '\0';
	
		
		pos = 0;
		cnum = i;
	
                strcpy(&fichier1[pos],argv[1]);
                pos = strlen(argv[1])-1;
                strcpy(&fichier1[pos],"caduceus_");
                pos = pos+9;

                for(int y = 4; y>-1 ; y--){
                        num[4-y] = cnum/puiss(10,y) + 48;
                        cnum = cnum - (cnum/puiss(10,y))*puiss(10,y);
                }

                strcpy(&fichier1[pos],num);
                pos = pos+5;
                strcpy(&fichier1[pos],".obj");
		

		pos = 0;
                cnum = i+1;

		printf("%s %d\n",argv[1],strlen(argv[1]));

		strcpy(&fichier2[pos],argv[1]);
		pos = strlen(argv[1])-1;
		strcpy(&fichier2[pos],"caduceus_");
		pos = pos+9;

                for(int y = 4; y>-1 ; y--){
                        num[4-y] = cnum/puiss(10,y) + 48;
                        cnum = cnum - (cnum/puiss(10,y))*puiss(10,y);
                }	

		strcpy(&fichier2[pos],num);	
		pos = pos+5;
		strcpy(&fichier2[pos],".obj");

		printf("%s | %s\n",fichier1,fichier2);

		//FILE * f1 = fopen(fichier1,"r");
		//FILE * f2 = fopen(fichier2,"r"); 
	}
}
