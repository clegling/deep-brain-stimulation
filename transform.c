#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>

void help()
{
   printf ("Software for .obj file transformation\n");
   printf ("Usage:\n");
   printf ("./transform file_name.obj\n");
   printf ("file_name.obj must be created by Brainsuite software and exported as a surface\n");
   printf ("Author: Alexander Ashikhmin, clegling@gmail.com");
}

int main(int argc, char* argv[])
{
   FILE  *fInputFile, *fOutputFile;
   char  cString[256];
   char  cStringForCounting[256];
   char  cFileName[256];
   char  cFullString[512];
   bool  bFirstLineFlag;
   int   iSectionNumber;
   int   iNumberOfVertexes;
   int   iNumberOfFaces;
   int   iNumberOfWords;
   char  *cSeparator = " \t";
   char  *cPointer;
   char  *cWord;
   

   bFirstLineFlag     = false;
   iSectionNumber     = 0;
   iNumberOfVertexes  = 0;
   iNumberOfFaces     = 0;
   strcat(cFileName, "new_");   

   if (argc != 2)
   {
      printf ("Error: no file name was entered as an argument\n");
      help();
      exit (EXIT_FAILURE);
   }
   
   if (strncmp(argv[1], "--help", 6) == 0 || strncmp(argv[1], "-h", 2) == 0 || strncmp(argv[1], "?", 1) == 0)
   {
      help();
      return 0;
   }
   
   if ((fInputFile = fopen(argv[1], "r")) == NULL)
   {
      perror(argv[1]);
      exit(EXIT_FAILURE);
   }

   if ((fOutputFile = fopen(strcat(cFileName, argv[1]), "w")) == NULL)
   {
      perror(cFileName);
      exit(EXIT_FAILURE);
   }
   
   int max = 0;
   int nums[10];
   while(fgets(cString, 256, fInputFile))
   {
      if (!bFirstLineFlag)
      {
         bFirstLineFlag = true;
         iSectionNumber++;
         continue;
      }

      if (strncmp(cString, "\n", 1) == 0)
      {
         iSectionNumber++;
         continue;
      }      

      memset(cFullString, 0, sizeof(cFullString));
      if (iSectionNumber == 1)
      {
         strncat(cFullString, "v", sizeof(cFullString) - strlen(cFullString) - 1);
         strncat(cFullString, cString, sizeof(cFullString) - strlen(cFullString) - 1);
         fprintf(fOutputFile, "%s", cFullString);
         iNumberOfVertexes++;
      }           
      
      if (iSectionNumber == 2)
      {  
         iNumberOfWords = 0;
         for (int i = 0; i < 10; i++) nums[i] = 0;
         strcpy(cStringForCounting, cString);
         for (cWord = strtok_r(cStringForCounting, cSeparator, &cPointer); cWord; cWord = strtok_r(NULL, cSeparator, &cPointer))      
         {  
            nums[iNumberOfWords] = atoi(cWord);    
            iNumberOfWords++;
         }

         if (iNumberOfWords == 3)
         {
            fprintf(fOutputFile, "f ");
            for (int i = 0; i < 3; i++)
               fprintf(fOutputFile, "%d ", nums[i] + 1);
            //strncat(cFullString, "f ", sizeof(cFullString) - strlen(cFullString) - 1);
            //strncat(cFullString, cString, sizeof(cFullString) - strlen(cFullString) - 1);
            //fprintf(fOutputFile, "%s", cFullString);
            fprintf(fOutputFile, "\n");
            iNumberOfFaces++;
         }
      }
   }

   printf ("max = %d\n", max);
      
   printf("Number od vertexes: %d\n", iNumberOfVertexes);
   printf("Number od faces: %d\n", iNumberOfFaces);  

   fclose (fInputFile);
   fclose (fOutputFile);
   return 0;
}
