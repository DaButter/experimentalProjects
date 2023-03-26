#ifndef CREDIT_CALCULATOR_BANKUTILS_HPP
#define CREDIT_CALCULATOR_BANKUTILS_HPP

#include <iostream>
#include <cmath>
#include <climits>
#include <fstream>
//#include "logDebug.hpp"

#define INTERESTRATE_INPUT "../interest_rate.txt"
using namespace std;

class BankUtils {
    double interestRate;
    double interestRateConfig;

public:
    BankUtils() {
        interestRate = 10.0;

        cout << "Press 0 to configure Interest Rate to use default value\n"
             << "Press 1 to configure Interest Rate to be read from file\n"
             << "Configuration choice: ";
        cin >> interestRateConfig;
        while (cin.fail() || interestRateConfig > 1.0 || interestRateConfig < 0.0) {
            cin.clear();
            cin.ignore(INT_MAX, '\n');
            cout << "Error: Wrong input!" << endl;
            cout << "Configuration choice: ";
            cin >> interestRateConfig;
        }

        if(interestRateConfig == 1) {
            ifstream input_file(INTERESTRATE_INPUT);
            if (!input_file.is_open()) {
                cout << "Could not find " << INTERESTRATE_INPUT << " file, proceeding with default value: "
                     << interestRate << endl;
            }
            while (input_file >> interestRate) {
                cout << "Interest rate read from file " << INTERESTRATE_INPUT << " successfully, value is: "
                     << interestRate << endl;
            }
            input_file.close();
        }
        else if(interestRateConfig == 0) {
            cout << "Proceeding with default value: " << interestRate << endl;
        }
    }

    // handles creditAmount user input
    double creditAmountInput() {
        double creditAmount;

        cout << "Credit amount: ";
        cin >> creditAmount;
        while (cin.fail() || creditAmount < 0 || creditAmount >= INT_MAX) {
            cin.clear();                            // clear input buffer to restore cin to a usable state
            cin.ignore(INT_MAX, '\n');     // ignore last input
            cout << "Error: Credit amount should be a positive decimal value/value input too long!\n"
                 << "Credit amount: ";
            cin >> creditAmount;
        }
        return creditAmount;
    }

    // handles creditPeriod user input
    int creditPeriodInput() {
        int creditPeriod;

        cout << "Credit period: ";
        cin >> creditPeriod;
        while (cin.fail() || creditPeriod < 0 || creditPeriod >= INT_MAX) {
            cin.clear();                            // clear input buffer to restore cin to a usable state
            cin.ignore(INT_MAX, '\n');     // ignore last input
            cout << "Error: Credit period should be a positive integer value/value input too long!"
                 << "Credit period: ";
            cin >> creditPeriod;
        }
        return creditPeriod;
    }

    int getCents(double amount) {
        amount = ceil((amount - static_cast<int>(amount)) * 100);
        return amount;
    }

    int getEuros(double amount) {
        return amount;
    }

    double calculateInterestRate(double creditAmount, unsigned int creditPeriod) {
        while(creditPeriod!=0){
            creditAmount = creditAmount + creditAmount*interestRate/100;
            if (creditAmount >= INT_MAX){
                cout << "Error: Credit period or Credit value too big!" << endl;
                return -1;
            }
            creditPeriod--;
        }
        return creditAmount;
    }

    double calculateInterestAmount(double totalAmount, double creditAmount) {
        return totalAmount - creditAmount;
    }
};

#endif //CREDIT_CALCULATOR_BANKUTILS_HPP
