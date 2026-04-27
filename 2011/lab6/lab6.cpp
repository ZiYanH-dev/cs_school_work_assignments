#include "lab6.h"
#include <cstring>

// Given functions; Please do not edit them
void swapRecord(StudentRecord &record1, StudentRecord &record2) {
    StudentRecord temp = record1;
    record1 = record2;
    record2 = temp;
}

bool isEmpty(const RecordHolder &recordHolder) {
    return !recordHolder.num_records;
}

int compareTo(const Date &date1, const Date &date2) {
    if (date1.year != date2.year) return static_cast<int>(date1.year) - static_cast<int>(date2.year);
    if (date1.month != date2.month) return static_cast<int>(date1.month) - static_cast<int>(date2.month);
    return static_cast<int>(date1.day) - static_cast<int>(date2.day);
}

int compareTo(const StudentRecord &student1, const StudentRecord &student2) {
    int val = compareTo(student1.entry, student2.entry);
    return val ? val : strcmp(student1.itso, student2.itso);
}

const StudentRecord& getEarliestRecord(const RecordHolder &recordHolder) {
    return recordHolder.records[0];
}

bool insertRecord(RecordHolder &recordHolder, StudentRecord &record) {
    if (recordHolder.num_records == MAX_RECORD_LENGTH) return false;

    recordHolder.records[recordHolder.num_records] = record;
    pushUp(recordHolder, static_cast<int>(recordHolder.num_records));
    
    return ++recordHolder.num_records;
}

void pushUp(RecordHolder &recordHolder, int index) {
    if (index <= 0) return;

    int parentIndex = (index - 1) / 2;
    if (compareTo(recordHolder.records[index], recordHolder.records[parentIndex]) < 0) {
        swapRecord(recordHolder.records[index], recordHolder.records[parentIndex]);
        pushUp(recordHolder, parentIndex);
    }
}

void pushDown(RecordHolder &recordHolder, int index) {
    int smallest = index;
    int left = 2 * index + 1;
    int right = 2 * index + 2;
    
    if (left < recordHolder.num_records && compareTo(recordHolder.records[left], recordHolder.records[smallest]) < 0) {
        smallest = left;
    }
    if (right < recordHolder.num_records && compareTo(recordHolder.records[right], recordHolder.records[smallest]) < 0) {
        smallest = right;
    }
    

    if (smallest != index) {
        swapRecord(recordHolder.records[index], recordHolder.records[smallest]);
        pushDown(recordHolder, smallest);
    }
}

StudentRecord& popEarliestRecord(RecordHolder &recordHolder) {
    StudentRecord& earliest = recordHolder.records[0];
    
    swapRecord(recordHolder.records[0], recordHolder.records[recordHolder.num_records - 1]);
    recordHolder.num_records--;
    
    if (recordHolder.num_records > 0) {
        pushDown(recordHolder, 0);
    }
    
    return earliest;
}
