    #include <iostream>
    #include <fstream>
    using namespace std;

    const int MAX_PATH_LENGTH = 100; // maximum length of a file path

    // Helper function for comparison
    bool greater_or_equal(double a, double b) {
        return ((a > b) || (((a>b)? (a-b):(b-a)) < 1e-12));
    }

    bool degree_classification(double cga, double mcga, int &first_honor, int &second_honor_div1, int &second_honor_div2, int &third_honor, int &pass) {
        cout << "Student with CGA = " << cga << " and MCGA = " << mcga << " graduated with: ";
        // TODO: Task 1 - Implement Degree Classification Logic
          // Use the helper function to compare floating-point numbers (avoid precision issues)
        bool graduated = true;

        // First Class Honors (3.500 - 4.300)
        if (greater_or_equal(cga, 3.4) && greater_or_equal(mcga, 3.6) ) {
            cout << "First Class Honors" << endl;
            first_honor++;
            
        }
        // Second Class Honors, Division I (2.850 - 3.499)
        else if (greater_or_equal(cga, 2.70) && greater_or_equal(mcga, 2.850) ) {
            cout << "Second Class Honors, Division I" << endl;
            second_honor_div1++;
        }
        // Second Class Honors, Division II (2.150 - 2.849)
        else if (greater_or_equal(cga, 2.0) && greater_or_equal(mcga, 2.15) ) {
            cout << "Second Class Honors, Division II" << endl;
            second_honor_div2++;
        }
        // Third Class Honors (1.500 - 2.149)
        else if (greater_or_equal(cga, 1.7) && greater_or_equal(mcga, 1.70) ) {
            cout << "Third Class Honors" << endl;
            third_honor++;
        }

        // Pass (0.850 - 1.499)
        else if (greater_or_equal(cga, 0.85) && greater_or_equal(mcga, 0.85)) {
            cout << "Pass" << endl;
            pass++;      
        }
        // Cannot graduate
        else {
            cout << "None" << endl;
            graduated = false;

        }

    return graduated;
    // TODO: End of Task 1
    }

    void update_averages(bool graduated, double cga, double mcga, int &num_of_students, double &avg_cga, double &avg_mcga) {
        // TODO: Task 2 - Update number of graduates and average values
        if (graduated)
        {
            // new_avg = (old_avg * old_count + new_value) / new_count
            double total_cga = avg_cga * num_of_students + cga;
            double total_mcga = avg_mcga * num_of_students + mcga;
            num_of_students++; 
            avg_cga = total_cga / num_of_students;
            avg_mcga = total_mcga / num_of_students;
        }

        // TODO: End of Task 2
    }

    int main() {
        char file_path[MAX_PATH_LENGTH];
        cout << "Please enter the input file path: ";
        cin >> file_path;

        fstream fin(file_path);

        // Check if the file can be opened
        if (!fin) {
            cout << "Error: Can not open " << file_path << endl;
            return -1;
        }

        double cga, mcga;
        int num_of_students = 0;
        // Average values
        double avg_cga = 0, avg_mcga = 0;
        // Number of students in classification
        int first_honor = 0, second_honor_div1 = 0, second_honor_div2 = 0, third_honor = 0, pass = 0;

        // TODO: Task 3a: Read a line from the input file to the variables
        while (fin >> cga >> mcga) {
        // TODO: End of Task 3a
            bool graduated = degree_classification(cga, mcga, first_honor, second_honor_div1, second_honor_div2, third_honor, pass);
            update_averages(graduated, cga, mcga, num_of_students, avg_cga, avg_mcga);
        }

        // TODO: Task 3b: Close the file stream
        fin.close();

        // TODO: End of Task 3b

        cout << "Statistics:" << endl
        << "Number of graduates: " << num_of_students << endl
        << "Number of graduates with First Class Honors: " << first_honor << endl
        << "Number of graduates with Second Class Honors, Division I: " << second_honor_div1 << endl
        << "Number of graduates with Second Class Honors, Division II: " << second_honor_div2 << endl
        << "Number of graduates with Third Class Honors: " << third_honor  << endl
        << "Number of graduates with Pass: " << pass << endl
        << "--------------------------------------------------------------------" << endl
        << "Average graduate CGA: " << avg_cga << endl
        << "Average graduate MCGA: " << avg_mcga << endl;

        return 0;
    }
