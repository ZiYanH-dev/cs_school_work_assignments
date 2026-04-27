#ifndef LAB6_H
#define LAB6_H

const int MAX_ITSO_LENGTH = 32;
const int MAX_RECORD_LENGTH = 100;

struct Date {
    unsigned int year;
    unsigned int month;
    unsigned int day;
};

struct StudentRecord {
    char itso[MAX_ITSO_LENGTH];
    unsigned int id;
    char gender;
    Date entry;
};

struct RecordHolder {
    StudentRecord records[MAX_RECORD_LENGTH]{};
    unsigned int num_records = 0;
};

/**
 * Swaps two records.
 * @param record1 The first record to swap
 * @param record2 The second record to swap
 */
void swapRecord(StudentRecord &record1, StudentRecord &record2);

/**
 * Checks if a recordHolder is empty.
 * @param recordHolder The recordHolder to check
 * @return True if it is empty; False otherwise.
 */
bool isEmpty(const RecordHolder &recordHolder);

/**
 * Compares two date objects.
 * @param date1 The first date to compare
 * @param date2 THe second date to compare
 * @return A negative value if date1 is earlier than date2; or
 *         zero if date1 is the same date as date2; or
 *         a positive value if date1 is later than date2.
 */
int compareTo(const Date &date1, const Date &date2);

/**
 * Compares two student records.
 * @param student1
 * @param student2
 * @return The value by comparing the two students' date of entry; or
 *         the lexicographical comparison of the students' itso if their dates of entry are the same.
 */
int compareTo(const StudentRecord &student1, const StudentRecord &student2);

/**
 * Gets the student record with the earliest date of entry (and "smallest" itso if there are multiple).
 * Note that this function assumes that the recordHolder is NOT empty.
 * @param recordHolder The recordHolder to retrieve the student record from
 * @return The earliest student record.
 */
const StudentRecord& getEarliestRecord(const RecordHolder &recordHolder);

/**
 * Inserts a student record into the recordHolder if it isn't full.
 * @param recordHolder The recordHolder to insert the record into
 * @param record The record to insert
 * @return True if it is inserted successfully; False otherwise.
 */
bool insertRecord(RecordHolder &recordHolder, StudentRecord &record);

/**
 * Reorders the array in Sunny's ordering leftwards.
 * In particular, after inserting a record at the end of the array, rearrange the order so that Sunny's ordering is maintained.
 * @param recordHolder The recordHolder to rearrange
 * @param index The lowest (largest) index to start rearranging from
 *
 * Hint: This function should be implemented recursively. After (possibly) swapping the record at
 * `index` with its parent, you should recursively call `pushUp` on the parent index to ensure
 * Sunny's ordering is maintained all the way up to the root.
 */
void pushUp(RecordHolder &recordHolder, int index);

/**
 * Reorders the array in Sunny's ordering rightwards.
 * In particular, after removing a record at the start of the array, rearrange the order so that Sunny's ordering is maintained.
 * @param recordHolder The recordHolder to rearrange
 * @param index The highest (smallest) index to start rearranging from
 *
 * Hint: This function should be implemented recursively. After (possibly) swapping the record at
 * `index` with one of its children, you should recursively call `pushDown` on the swapped child's
 * index to ensure Sunny's ordering is maintained all the way down to the leaf level.
 */
void pushDown(RecordHolder &recordHolder, int index);

/**
 * Pops the student record with the earliest date of entry (and "smallest" itso if there are multiple).
 * Note that this function assumes that the recordHolder is NOT empty.
 * @param recordHolder The recordHolder to pop from
 * @return The earliest student record.
 */
StudentRecord& popEarliestRecord(RecordHolder &recordHolder);

#endif