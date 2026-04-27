#include <iostream>
#include "lab6.h"
using namespace std;

unsigned int idCounter = 0;
const char sep[] = "=====================================\n";

// Given Helper Function
StudentRecord createStudentRecord() {
    char itso[MAX_ITSO_LENGTH]{};
    cout << "Please enter the ITSO username of the student: ";
    cin >> itso;
    cout << itso << endl;

    unsigned int id = idCounter++;

    char gender[2];
    cout << "Please enter the gender of the student (M/F): ";
    cin >> gender;
    cout << gender[0] << endl;

    unsigned int year, month, day;
    cout << "Please enter the year of entry: ";
    cin >> year;
    cout << year << endl;
    cout << "Please enter the month of entry: ";
    cin >> month;
    cout << month << endl;
    cout << "Please enter the day of entry: ";
    cin >> day;
    cout << day << endl;

    StudentRecord record{};
    for (int i = 0; i < MAX_ITSO_LENGTH && itso[i] != '\0'; ++i)
        record.itso[i] = itso[i];
    record.id = id;
    record.gender = gender[0];
    record.entry = {year, month, day};
    return record;
}

void printStudentRecord(const StudentRecord &studentRecord) {
    cout << "Student " << studentRecord.itso << "\n";
    cout << "- ID: " << studentRecord.id << "\n";
    cout << "- Gender: " << studentRecord.gender << "\n";
    cout << "- Date of Entry: " << studentRecord.entry.year << "-" << studentRecord.entry.month << "-" << studentRecord.entry.day << endl;
}

void printAllRecords(const RecordHolder &recordHolder) {
    cout << "All records:\n" << sep;
    for (unsigned int i = 0; i < recordHolder.num_records; i++) {
        printStudentRecord(recordHolder.records[i]);
        cout << sep;
    }
}


int main() {
    RecordHolder h;
    int n;
    cout << "Please enter the number of operations: ";
    cin >> n;
    cout << n << endl;

    for (int i = 0; i < n; i++) {
        char op;
        cout << "Please enter operation (I/P/G/E): ";
        cin >> op;
        cout << op << endl;

        if (op == 'I') {
            StudentRecord r = createStudentRecord();
            bool success = insertRecord(h, r);
            if (success) {
                cout << "Insert successful!" << endl;
            } else {
                cout << "Insert failed (full)." << endl;
            }
            cout << sep;
        } else if (op == 'P') {
            // Save a copy of records[0] before the pop so we can print the removed record.
            // (popEarliestRecord returns a reference to records[0] which gets overwritten
            // internally, so we capture the value here instead of relying on the return.)
            StudentRecord popped = h.records[0];
            popEarliestRecord(h);
            cout << "Popped:" << endl;
            printStudentRecord(popped);
            cout << sep;
        } else if (op == 'G') {
            const StudentRecord &r = getEarliestRecord(h);
            cout << "Earliest:" << endl;
            printStudentRecord(r);
            cout << sep;
        } else if (op == 'E') {
            if (isEmpty(h)) {
                cout << "RecordHolder is empty." << endl;
            } else {
                cout << "RecordHolder is not empty." << endl;
            }
            cout << sep;
        }
    }

    printAllRecords(h);
    return 0;
}
