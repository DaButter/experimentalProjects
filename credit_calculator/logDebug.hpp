#ifndef PRAKSES_TESTS_ADVANCED_LOGDEBUG_HPP
#define PRAKSES_TESTS_ADVANCED_LOGDEBUG_HPP

#include <iostream>
#include <fstream>

#define LOGDEBUG "log_debug.txt"
using namespace std;

class logDebug {

public:
    logDebug(){
        // read OS type
        // write OS type and time of start of program
        // close file
    }

    void debug_msg(string msg){
        // open file for writing
        // read time
        // write msg
        // close file
    }
};

#endif //PRAKSES_TESTS_ADVANCED_LOGDEBUG_HPP
