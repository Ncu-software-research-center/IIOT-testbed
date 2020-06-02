/**
 * LOGICAL_NAME:    dds_debug.hpp
 * FUNCTION:        Handle DDS debugging message.
 * VERSION:         Testbed 2.2
 * DATA:            2019 04 15
 * AUTOR:           Rex Lin
 */

#ifndef TESTBED_BACKEND_DDS_DEBUG_
#define TESTBED_BACKEND_DDS_DEBUG_

#include "ccpp_dds_dcps.h"
#include "debug.hpp"

/* Array to hold the names for all ReturnCodes. */
static std::string RetCodeName[13] = {"DDS_RETCODE_OK",
                                      "DDS_RETCODE_ERROR",
                                      "DDS_RETCODE_UNSUPPORTED",
                                      "DDS_RETCODE_BAD_PARAMETER",
                                      "DDS_RETCODE_PRECONDITION_NOT_MET",
                                      "DDS_RETCODE_OUT_OF_RESOURCES",
                                      "DDS_RETCODE_NOT_ENABLED",
                                      "DDS_RETCODE_IMMUTABLE_POLICY",
                                      "DDS_RETCODE_INCONSISTENT_POLICY",
                                      "DDS_RETCODE_ALREADY_DELETED",
                                      "DDS_RETCODE_TIMEOUT",
                                      "DDS_RETCODE_NO_DATA",
                                      "DDS_RETCODE_ILLEGAL_OPERATION"};

/**
 * Check the return status for errors. If there is an error, then terminate.
 **/
static void _check_status(DDS::ReturnCode_t status, std::string info) {
  if (status != DDS::RETCODE_OK && status != DDS::RETCODE_NO_DATA) {
    std::cerr << "Error:  " << RetCodeName[status].c_str() << std::endl;
    std::cerr << "Message: " << info << std::endl;
    exit(1);
  }
}

/**
 * Check whether a valid handle has been returned. If not, then terminate.
 **/
static void _check_handle(void *handle, std::string info) {
  if (!handle) {
    std::cerr << "Error: " << info << std::endl;
    exit(1);
  }
}

#endif