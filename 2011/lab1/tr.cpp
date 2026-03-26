#include <iostream>
using namespace std;


enum Dept { CSE, ECE, MATH }; /* File: student-record.h */
struct Date
{
unsigned int year;
unsigned int month;
unsigned int day;
};

struct Student_Record{
char name[32];
unsigned int id;
char gender;
Dept dept;
Date entry;
};
void init_student_record(Student_Record& a, const char name[],unsigned int id, char gender,
    Dept dept, const Date& date){
            strcpy(a.name, name);
            a.id = id;
            a.gender = gender;
            a.dept = dept;
            a.entry = date; // struct-struct assignment
}



int main() {
    int arr[5];
    arr[1]=1;
// arr 是 int*
// +1 → 跳 1 个 int

cout << arr  << endl; 
cout << arr + 1 << endl;       // 比 arr 大 4 字节
cout << *(arr + 1 )<< endl;   

// &arr 是 int(*)[5]
// +1 → 跳 1 整个数组！
cout << (&arr) + 1 << endl;    // 比 arr 大 20 字节
    
    return 0;
}
