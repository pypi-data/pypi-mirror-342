#ifndef CANCERSOLVER_FRAMEWORK_H
#define CANCERSOLVER_FRAMEWORK_H

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#include "loader.h"

// ------------------------------
// defines
// ------------------------------

#ifdef __cplusplus
#define BEGIN_DECL_C extern "C" {
#define END_DECL_C }
#else
#define BEGIN_DECL_C
#define END_DECL_C
#endif // __cplusplus

BEGIN_DECL_C

typedef struct time_measurement {
    uint64_t time_ns;
    char *name;
    uint32_t retries;
} time_measurement_t;

#define MAX_MEASUREMENTS 32

typedef struct error_log {
    const char *name;
    char *value;
} error_log_t;

#define MAX_ERROR_LOGS 1024

typedef struct test_result {
    char *function_name;

    time_measurement_t measurements[MAX_MEASUREMENTS];
    size_t measurement_counter;

    error_log_t error_logs[MAX_ERROR_LOGS];
    size_t error_logs_counter;
} test_result_t;

#define MAX_RESULTS 257

typedef struct app_state {
    int verbose_flag;
    int detailed_flag;
    int no_errors_flag;
    int num_rep_tests;

    const char **input_files;
    size_t size_files;

    const char *output_file;

    test_result_t results[MAX_RESULTS];
    size_t results_counter;

    test_result_t* current_test;
} app_state_t;

#define FILE_PATH_SEPARATOR "/"

#define MAIN_MEASUREMENT_NAME "Full execution time"

// ------------------------------
// Data functions
// ------------------------------

void StartMeasurement(time_measurement_t *measurement, char *name);

void EndMeasurement(time_measurement_t *measurement);

void AddDataMeasurement(test_result_t *result, time_measurement_t measurement);

#define PREPARE_DATA_MEASUREMENT(data_measurement, ...) \
    do { \
        char* name = (char *) malloc(256); \
        snprintf(name, 256, __VA_ARGS__); \
        StartMeasurement(&data_measurement, name); \
    } while (0)

void AddErrorLog(test_result_t *result, error_log_t log);

#define PREPARE_ERROR_LOG(error_name, ...) \
do { \
error_log_t log; \
log.name = error_name; \
log.value = (char *) malloc(256); \
snprintf(log.value, 256, __VA_ARGS__); \
AddErrorLog(test_result, log); \
} while (0)

void CleanupResults(test_result_t *result);

void DisplayResults(FILE *file, test_result_t *results, size_t results_size);

// ------------------------------
// Core functions
// ------------------------------

void ParseCLI(int argc, const char **argv);

void FailApplication(const char *msg);

int IsVerbose();

void DisplayHelp();

void RunTests();

void FinalizeTesting();

test_result_t *AllocResults();

test_result_t* GetOngoingTest();

#define PREPARE_TEST_RESULT(test_result, ...) \
    do { \
        char *name = (char *) malloc(256); \
        snprintf(name, 256, __VA_ARGS__); \
        test_result->function_name = name; \
    } while (0)

data_ptr_t ParseData(const char *filename);

void CleanupData(data_ptr_t data);

END_DECL_C

#endif // CANCERSOLVER_FRAMEWORK_H
