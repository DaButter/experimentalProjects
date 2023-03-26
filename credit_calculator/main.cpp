#include <iostream>
#include "bankUtils.hpp"
#include "logDebug.hpp"

using namespace std;

int main() {
    double creditAmount, totalInterest, totalAmount;
    int creditPeriod, totalAmountEuros, totalInterestEuros, totalAmountCents, totalInterestCents;

    BankUtils bankUtils;

    // USER INPUT
    creditAmount = bankUtils.creditAmountInput();
    creditPeriod = bankUtils.creditPeriodInput();


    // CREDIT CALCULATIONS
    totalAmount = bankUtils.calculateInterestRate(creditAmount, creditPeriod);
    if(totalAmount == -1){
        cerr << "Error: Calculation too big to handle!" << endl;
        return -1;
    }
    totalInterest = bankUtils.calculateInterestAmount(totalAmount, creditAmount);

    totalAmountEuros = bankUtils.getEuros(totalAmount);
    totalInterestEuros = bankUtils.getEuros(totalInterest);

    totalAmountCents = bankUtils.getCents(totalAmount);
    totalInterestCents = bankUtils.getCents(totalInterest);

    // USER OUTPUT
    cout << "\nTOTAL AMOUNT: " << totalAmountEuros << " EUROS AND " << totalAmountCents << " CENTS";
    cout << "\nTOTAL INTEREST: " << totalInterestEuros << " EUROS AND " << totalInterestCents << " CENTS" << endl;

    return 0;
}
