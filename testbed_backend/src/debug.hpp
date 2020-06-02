/**
 * LOGICAL_NAME:    debug.hpp
 * FUNCTION:        Handle debugging message.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_DEBUG_
#define TESTBED_BACKEND_DEBUG_

#include <iostream>
#include <string>

#ifdef DEBUG
#define DEBUG_LOG(message)                                         \
  std::cout << "[DEBUG] -- " << __DATE__ << __TIME__               \
            << " in file: " << __FILE__ << " at line " << __LINE__ \
            << " method: " << __func__ << std::endl;               \
  std::cout << "message: " << message << std::endl;
#define DEBUG_MSG(message)                                                     \
  std::string("[DEBUG] -- ") + std::string(__DATE__) + std::string(__TIME__) + \
      std::string(" in file: ") + std::string(__FILE__) +                      \
      string(" at line ") + std::to_string(__LINE__) +                         \
      std::string(" method: ") + std::string(__func__) +                       \
      std::string("\nmessage: ") + std::string(message)
#else
#define DEBUG_LOG(mesage)
#define DEBUG_MSG(message) message
#endif

#endif