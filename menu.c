#include <stdlib.h>

int main() {
    int choice;
    
    while (1) {
        system("cls");
        printf("1. snake (main.py)\n");
        printf("2. stulkov (linter.py)\n");
        printf("3. exit\n");
        printf("> ");
        scanf("%d", &choice);
        
        if (choice == 1) system("python main.py");
        else if (choice == 2) system("python linter.py");
        else if (choice == 3) break;
        
        if (choice != 3) {
            printf("\npress Enter to continue...");
            while (getchar() != '\n');
            getchar();
        }
    }
    return 0;
}