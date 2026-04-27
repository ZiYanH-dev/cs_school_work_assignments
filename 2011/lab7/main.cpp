#include "lab7.h"

int main() {
    cout << "Welcome to the Potion Brewery Inventory System!" << endl;
    cout << "Initializing..." << endl;

    char shopName[MAX_NAME_LENGTH];
    int maxItems;
    cout << "Enter shop name: ";
    cin.getline(shopName, MAX_NAME_LENGTH);
    cout << "Enter max inventory size: ";
    cin >> maxItems;
    cin.ignore();

    Inventory inv;
    initInventory(&inv, shopName, maxItems);

    int option = -1;
    do {
        cout << "======================================" << endl;
        cout << "0. Quit" << endl;
        cout << "1. Add an item" << endl;
        cout << "2. Remove most expensive item" << endl;
        cout << "3. Restock an item" << endl;
        cout << "4. Display inventory" << endl;
        cout << "======================================" << endl;
        cout << "Option: ";
        cin >> option;
        cin.ignore();

        if (option == 1) {  // ===== Add Item =====
            char name[MAX_NAME_LENGTH];
            int qty;
            double price, weight;
            cout << "Enter item name: ";
            cin.getline(name, MAX_NAME_LENGTH);
            cout << "Enter quantity: ";
            cin >> qty;
            cout << "Enter price (gold): ";
            cin >> price;
            cout << "Enter weight (kg): ";
            cin >> weight;
            cin.ignore();
            addItem(&inv, name, qty, price, weight);
        }

        else if (option == 2) { // ===== Remove Most Expensive =====
            removeMostExpensive(&inv);
        }

        else if (option == 3) { // ===== Restock =====
            char name[MAX_NAME_LENGTH];
            int qty;
            cout << "Enter item name: ";
            cin.getline(name, MAX_NAME_LENGTH);
            cout << "Enter additional quantity: ";
            cin >> qty;
            cin.ignore();
            restockItem(&inv, name, qty);
        }

        else if (option == 4) { // ===== Display Inventory =====
            displayInventory(&inv);
        }

        else if (option == 0) {
            cout << "Closing shop..." << endl;
        }

        else {
            cout << "Invalid option. Please try again." << endl;
        }

    } while (option != 0);

    cout << "Shop closed. Goodbye!" << endl;
    return 0;
}
