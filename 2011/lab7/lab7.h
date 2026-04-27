#ifndef LAB7_H
#define LAB7_H

#include <iostream>
#include <iomanip>
#include <cstring>
using namespace std;

// ============================================================
// COMP2011 Lab 7: Potion Brewery Inventory System
// Struct definitions and function declarations
// ============================================================

const int MAX_NAME_LENGTH = 50;
const int MAX_ITEMS = 100;

// ============================================================
// Item Struct
// ============================================================

struct Item {
    char name[MAX_NAME_LENGTH];   // item name (e.g., "Health Potion")
    int quantity;                  // number in stock
    double price;                 // price per unit in gold
    double weight;                // weight per unit in kg
};

// Task 1: Initialize an Item through a pointer
void initItem(Item* item, const char name[], int quantity, double price, double weight);

// Task 2: Display item info through a const pointer
// Format: "Name (qty: X) - Price: Y.Y gold, Weight: Z.Z kg"
void displayItem(const Item* item);

// ============================================================
// Inventory Struct
// ============================================================

struct Inventory {
    char shopName[MAX_NAME_LENGTH];  // name of the shop
    Item items[MAX_ITEMS];           // fixed-size array of Items (insertion order)
    Item* itemPtrs[MAX_ITEMS];       // array of pointers into items[] (used for sorting)
    int itemCount;                   // current number of distinct items
    int capacity;                    // user-chosen limit on distinct items (<= MAX_ITEMS)
};

// Task 3: Initialize inventory through a pointer
void initInventory(Inventory* inv, const char shopName[], int capacity);

// Task 4: Add an item (return true if added, false if full).
//         Keep inv->itemPtrs sorted by unit price (descending) while inserting.
bool addItem(Inventory* inv, const char name[], int quantity, double price, double weight);

// Task 5: Restock an item by name; search items[] for the name, then add
//         additionalQty to its quantity. Return true if found, false otherwise.
//         Note: capacity limits the number of distinct items, NOT total quantity,
//         so restocking an existing item is always allowed.
bool restockItem(Inventory* inv, const char name[], int additionalQty);

// Task 6: Remove the item with the highest TOTAL value (quantity * price).
//         Shift items[] left to fill the gap, then rebuild itemPtrs[] and keep
//         it sorted by unit price descending.
//         Print which item was removed. Return false if inventory is empty.
bool removeMostExpensive(Inventory* inv);

// Helper function: display all items through itemPtrs (highest unit price first).
//                  Compute and print total inventory value
//                  inline — sum of (quantity * price) for each item.
void displayInventory(Inventory* inv);

#endif
