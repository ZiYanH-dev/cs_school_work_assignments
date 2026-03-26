#include <iostream>
using namespace std;

int main() {
    int a = 100;
int* p = &a;

// 下面三个完全一样！
// cout<<*p<<endl;
// cout<<p[0]<<endl;
// cout<<0[p];  // 甚至能这么写，因为等价于 *(0 + p)

cout<<'1'+1<<endl<<'1'+'1';
    return 0;
}
