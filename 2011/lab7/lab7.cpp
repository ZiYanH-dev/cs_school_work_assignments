#include "lab7.h"

// ============================================================
// COMP2011 Lab 7: Potion Brewery Inventory System
// Implementation of all functions (Tasks 1–6)
// ============================================================

// ============================================================
// Task 1 — Initialize an Item
// ============================================================

// Set all fields of the Item pointed to by 'item'.
// - item: pointer to the Item to initialize
// - name: C-string to copy into item->name (use strncpy, null-terminate)
// - quantity: number of units in stock
// - price: price per unit in gold
// - weight: weight per unit in kg
void initItem(Item* item, const char name[], int quantity, double price, double weight) {
    // TODO: Implement this function
    item->quantity = quantity;
    item->price = price;
    item->weight = weight;      
    strcpy(item->name, name); // Copy 

}

// ============================================================
// Task 2 — Display an Item
// ============================================================

// Print the item's information in this exact format:
//   "<name> (qty: X) - Price: Y.Y gold, Weight: Z.Z kg"
// - item: pointer to a const Item (read-only)
// - Use fixed << setprecision(1) for price and weight
void displayItem(const Item* item) {
    // TODO: Implement this function
    // cout << item->name << " (qty: " << item->quantity << ") - Price: " << fixed << setprecision(1) << item->price << " gold, Weight: " << fixed << setprecision(1) << item->weight << " kg" << endl;
    cout << fixed << setprecision(1);
    cout << item->name << " (qty: " << item->quantity
         << ") - Price: " << item->price
         << " gold, Weight: " << item->weight << " kg"<< endl;
}

// ============================================================
// Task 3 — Initialize Inventory
// ============================================================

// Set up an empty inventory.
// - inv: pointer to the Inventory to initialize
// - shopName: C-string to copy into inv->shopName (use strncpy, null-terminate)
// - capacity: maximum number of distinct items this shop can hold
// - itemCount should start at 0
void initInventory(Inventory* inv, const char shopName[], int capacity) {
    // TODO: Implement this function
    inv->itemCount = 0;
    inv->capacity = capacity;
    strcpy(inv->shopName, shopName); // Copy    
}

// ============================================================
// Task 4 — Add an Item (Create)
// ============================================================

// Add a new item to the inventory. Return false if inventory is full.
// - If inv->itemCount >= inv->capacity, print "Inventory full! Cannot add <name>."
// - Otherwise, initialize the next slot in inv->items[] using initItem.
// - Insert the pointer to the new item into inv->itemPtrs[] so that
//   itemPtrs remains sorted by price descending.
// - Increment itemCount and print "<name> added successfully."
// - inv->items[]: stores the actual Item data in insertion order
// - inv->itemPtrs[]: stores pointers into items[], used later for sorting
bool addItem(Inventory* inv, const char name[], int quantity, double price, double weight) {
    // TODO: Implement this function
    if (inv->itemCount >= inv->capacity) {
        cout << "Inventory full! Cannot add " << name << "." << endl;
        return false;
    }
    initItem(&inv->items[inv->itemCount], name, quantity, price, weight);
    inv->itemPtrs[inv->itemCount] = &inv->items[inv->itemCount];
    inv->itemCount++;

    // Sort itemPtrs 
    for (int i = 0; i < inv->itemCount; i++) {
        for (int j = i + 1; j < inv->itemCount; j++) {
            if (inv->itemPtrs[i]->price < inv->itemPtrs[j]->price) {
                Item* temp = inv->itemPtrs[i];
                inv->itemPtrs[i] = inv->itemPtrs[j];
                inv->itemPtrs[j] = temp;
            }
        }
    }

    cout << name << " added successfully." << endl;
    return true;
}

// ============================================================
// Task 5 — Restock an Item (Update)
// ============================================================

// Search inv->items[] for an item matching 'name' (use strcmp).
// If found, add additionalQty to its quantity, print
//   "<name> restocked. New quantity: X", and return true.
// If not found, print "Item not found: <name>" and return false.
// - capacity limits the number of distinct items, NOT total quantity,
//   so restocking is always allowed.
bool restockItem(Inventory* inv, const char name[], int additionalQty) {
    // TODO: Implement this function
    for (int i = 0; i < inv->itemCount; i++) {
        if (strcmp(inv->items[i].name, name) == 0) {
            inv->items[i].quantity += additionalQty;
            cout << name << " restocked. New quantity: " << inv->items[i].quantity << endl;
            return true;
        }
    }
    cout << "Item not found: " << name << endl;
    return false;
}

// ============================================================
// Task 6 — Remove the Most Expensive Item (by total value)
// ============================================================

// Remove the item with the highest total value (quantity * price).
// If inventory is empty, print "Inventory is empty. Nothing to remove."
//   and return false.
// Otherwise:
// - Find the index in items[] with the highest quantity * price
// - Print "Removed: <name> (Total value: X.X gold)"
// - Shift items[] left to fill the gap, decrement itemCount
// - Rebuild itemPtrs[] and keep it sorted by unit price descending
// - Return true
bool removeMostExpensive(Inventory* inv) {
    // TODO: Implement this function
    if (inv->itemCount == 0) {
        cout << "Inventory is empty. Nothing to remove." << endl;
        return false;
    }
    int maxIndex = 0;
    for (int i = 1; i < inv->itemCount; i++) {
        if (inv->items[i].quantity * inv->items[i].price > inv->items[maxIndex].quantity * inv->items[maxIndex].price) {
            maxIndex = i;
        }
    }
    // Item* itemToRemove = &inv->items[maxIndex];
    // cout << "Removed: " << itemToRemove->name << " (Total value: " << fixed << setprecision(1) << itemToRemove->quantity * itemToRemove->price << " gold)" << endl;

    double totalVal = inv->items[maxIndex].quantity * inv->items[maxIndex].price;
    cout << fixed << setprecision(1);
    cout << "Removed: " << inv->items[maxIndex].name
         << " (Total value: " << totalVal << " gold)" << endl;

    for (int i = maxIndex; i < inv->itemCount - 1; i++) {
        inv->items[i] = inv->items[i + 1];
    }
    inv->itemCount--;
    // Rebuild itemPtrs[] 
    for (int i = 0; i < inv->itemCount - 1; i++) {
        for (int j = 0; j < inv->itemCount - i - 1; j++) {
            if (inv->itemPtrs[j]->price < inv->itemPtrs[j+1]->price) {
                Item* temp = inv->itemPtrs[j];
                inv->itemPtrs[j] = inv->itemPtrs[j+1];
                inv->itemPtrs[j+1] = temp;
            }
        }
    }

    return true;
}

// ============================================================
// Provided Function — Display Inventory (Sorted by Unit Price, Descending)
// ============================================================

// Display the full inventory using itemPtrs[] order (highest first).
// - Print "=== Inventory of <shopName> ==="
// - If empty, print "(empty)"; otherwise call displayItem for each
//   entry in itemPtrs[]
// - Compute total inventory value: sum of (quantity * price) for each item
// - Print "Total inventory value: X.X gold"
void displayInventory(Inventory* inv) {
    cout << "=== Inventory of " << inv->shopName << " ===" << endl;
    if (inv->itemCount == 0) {
        cout << "(empty)" << endl;
    } else {
        for (int i = 0; i < inv->itemCount; i++) {
            displayItem(inv->itemPtrs[i]);
        }
    }
    double total = 0.0;
    for (int i = 0; i < inv->itemCount; i++) {
        total += inv->itemPtrs[i]->quantity * inv->itemPtrs[i]->price;
    }
    cout << "Total inventory value: " << fixed << setprecision(1) << total << " gold" << endl;
}
