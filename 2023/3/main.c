#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>

#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_YELLOW  "\x1b[33m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN    "\x1b[36m"
#define ANSI_COLOR_RESET   "\x1b[0m"

typedef struct {
   int rows;
   int columns;

} matrix_description;

int intmax(int a, int b){
   if(a>b){
      return a;
   }
   return b;
}

matrix_description describe_matrix(FILE* fp){
   size_t len;
   size_t linelen;
   char * line = NULL;
   char c;
   int column_length;

   matrix_description description;
   description.rows = 0;
   description.columns = 0;

   while ((linelen = getline(&line, &len, fp)) != -1){
      column_length = 0;
      while ((c = *line) != '\0'){
         if(c != '\n'){
            column_length ++;
         }
         line++;
      }
      description.columns = intmax(description.columns, column_length);
      description.rows ++;
   }
   return description;
}

void read_matrix(FILE* fp, matrix_description description, char matrix[description.rows][description.columns]){
   size_t len;
   char * line = NULL;
   char c;
   int row = 0;
   int col = 0;
   while (getline(&line, &len, fp) != -1){
      col = 0;
      while ((c = *line) != '\0'){
         if(c != '\n') {
            matrix[row][col] = c;
            col++;
         }
         line++;
      }
      row++;
   }
}

int is_number(char c) {
   char numbers[] = "0123456789";
   int i;
   for(i = 0; i < 10; i++){
      if(c == numbers[i]){
         return 1;
      }
   }
   return 0;
}

int is_blank(char c) {
   if(c == '.') {
      return 1;
   }
   return 0;
}

int is_symbol(char c) {
   if(!is_number(c) && !is_blank(c)){ 
      return 1;
   }
   return 0;
}

int coords_out_of_bounds(matrix_description description, int x, int y){
   if(x < 0) {
      return 1;
   }
   if(x >= description.rows){
      return 1;
   }
   if(y < 0){
      return 1;
   }
   if(y >= description.columns){
      return 1;
   }
   return 0;
}

void cell_context(matrix_description description, char matrix[description.rows][description.columns], int x, int y, char context[3][3]){
   char c;
   int i,j,xt,yt;
   for(i = 0; i < 3; i++){
      for(j = 0; j < 3; j++){
         xt = x - (i-1);
         yt = y - (j-1);
         if(coords_out_of_bounds(description, xt, yt) != 0){
            c = '.';
         } else {
            c = matrix[xt][yt];
         }
         context[i][j] = c;
      }
   }
}

void print_context(char context[3][3]){
   int i,j;
   for(i = 0; i < 3; i++){
      for(j = 0; j < 3; j++){
         if(i == 1 && j == 1) {
            printf(ANSI_COLOR_RED);
         }
         printf("%c",context[i][j]);
         if(i == 1 && j == 1) {
            printf(ANSI_COLOR_RESET);
         }
      }
      printf("\n");
   }
}

void flag_context(matrix_description description, int x, int y, int flags[description.rows][description.columns]){
   int xt, yt, i, j;
   for(i = 0; i < 3; i++){
      for(j = 0; j < 3; j++){
         xt = x + i - 1;
         yt = y + j - 1;
         if(!coords_out_of_bounds(description, xt, yt)){
            flags[xt][yt] = 1;
         }
      }
   }
}

void print_char_matrix(matrix_description description, char m[description.rows][description.columns]){
   int x,y;
   for(x=0;x<(sizeof(*m)/sizeof(*m[0]));x++){
      for(y=0;y<sizeof(m[0])/sizeof(m[0][0]);y++){
         printf("%c", m[x][y]);
      }
      printf("\n");
   }
}

void print_bool_matrix(matrix_description description, int m[description.rows][description.columns]){
   int x,y;
   for(x=0;x<(sizeof(*m)/sizeof(*m[0]));x++){
      for(y=0;y<sizeof(m[0])/sizeof(m[0][0]);y++){
         if(m[x][y]!=0){
            printf("o");
         } else {
            printf(".");
         }
      }
      printf("\n");
   }
}

void print_masked(matrix_description description, int mask[description.rows][description.columns], char matrix[description.rows][description.columns]){
   char masked[description.rows][description.columns];
   int x,y;
   for(x=0;x<description.rows;x++){
      for(y=0;y<description.columns;y++){
         if(mask[x][y]!=0){
            masked[x][y]=matrix[x][y];
         } else {
            masked[x][y]='o';
         }
      }
   }
   print_char_matrix(description, masked);
}

void reset_running_sum(int *flag, int *concurrent, int *sum, char buffer[16]){
   int i;
   if(*concurrent > 0){
      if(*flag != 0){
         *sum = *sum + atoi(buffer);
      } else {
      }
      *flag=0;
      *concurrent=0;
      for(i=0;i<16;i++){
         buffer[i]='\0';
      }
   }
}

int part_number_sum(matrix_description description, char matrix[description.rows][description.columns]){
   int x,y,i,j;
   char c;
   char context[3][3];
   int in_symbol_context[description.rows][description.columns];
   for(x = 0; x < description.rows; x++){
      for(y = 0; y < description.columns; y++){
         if(is_symbol(matrix[x][y])){
            flag_context(description, x, y, in_symbol_context);
         }
      }
   }

   int sum = 0;
   int concurrent_numbers = 0;
   int flag = 0;
   char string_int_buffer[16];
   for(x = 0; x < description.rows; x++){
      for(y = 0; y < description.columns; y++){
         if(is_number(matrix[x][y])){
            string_int_buffer[concurrent_numbers] = matrix[x][y];
            concurrent_numbers++;
            flag = flag + in_symbol_context[x][y];
         } else {
            reset_running_sum(&flag, &concurrent_numbers, &sum, string_int_buffer);
         }
      }
      reset_running_sum(&flag, &concurrent_numbers, &sum, string_int_buffer);
   }
   return sum;
}

int main(void) {
   FILE * fp;
   int task_one;
   matrix_description description;
   fp = fopen("./data","r");

   description = describe_matrix(fp);
   fseek(fp, 0, SEEK_SET);

   char matrix[description.rows][description.columns];
   read_matrix(fp, description, matrix);
   fclose(fp);

   task_one = part_number_sum(description, matrix);
   printf("Task one: %i\n", task_one);

   exit(EXIT_SUCCESS);
}
