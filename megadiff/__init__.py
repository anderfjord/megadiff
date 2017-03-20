#!/usr/bin/env python

import linecache
import logging
import os

from datetime import datetime

log = logging.getLogger(__name__)

REPORT_INTERVAL = 5000


def compare_files_by_line(filepath_1, filepath_2):
    """ Compares two files based on the contents of each line """

    start_ts = datetime.now()
    counts = {
        'iterations': 0,
        'matches': 0,
        'misses': 0,
    }

    log.info('Starting file comparison at: %s', start_ts)
    log.info('Comparing files:')
    log.info('File 1: %s', filepath_1)
    log.info('File 2: %s', filepath_2)

    def _print_comparison_report():
        """ Outputs a report of comparison results """

        time_diff = datetime.now() - start_ts
        time_diff_in_secs = time_diff.total_seconds()
        time_diff_in_minutes = '%dmins, %dsecs' % (time_diff_in_secs / 60, time_diff_in_secs % 60)

        log.info('--------------------------------------')
        log.info('Elapsed Time In Seconds: %d', time_diff_in_secs)
        log.info('Execution Time: %s', time_diff_in_minutes)
        log.info('Lines Processed: %d', counts['iterations'])
        log.info('Match Count: %d', counts['matches'])
        log.info('Miss Count: %d', counts['misses'])


    def _line_generator(file_handle):
        for line in file_handle:
            yield line

    with open(filepath_1) as f1_handle:
        with open(filepath_2) as f2_handle:

            f2_lines = _line_generator(f2_handle)

            for f1_line in f1_handle:

                try:
                    f2_line = next(f2_lines)
                except StopIteration:
                    _print_comparison_report()
                    log.info('--------------------------------------')
                    log.info('!!! FILE 1 IS LONGER THAN FILE 2 !!!')
                    return False

                counts['iterations'] += 1

                if f1_line == f2_line:
                    counts['matches'] += 1
                else:
                    counts['misses'] += 1
                    log.debug('MISS -------------------')
                    log.debug('F1 Line: %s', f1_line)
                    log.debug('-------')
                    log.debug('F2 Line: %s', f2_line)

                # Print a report every so often
                if counts['iterations'] % REPORT_INTERVAL == 0:
                    _print_comparison_report()

            log.info('--------------------------------------')
            log.info('FINAL REPORT')
            _print_comparison_report()

            """
            At this point we have iterated over all of File 1's lines,
            and need to make sure that File 2 doesn't have additional lines.
            If the call to next() succeeeds without raising an exception,
            then it means that File 2 has at least one additional line,
            meaning that File 1 and File 2 do not match exactly.
            """
            try:
                extra_line = next(f2_lines)
                log.info('--------------------------------------')
                log.info('!!! FILE 2 IS LONGER THAN FILE 1 !!!')
                return False
            except StopIteration:
                pass

    if counts['misses'] == 0:
        log.info('!!! FILES MATCH EXACTLY !!!')
        return True
    else:
        log.info('!!! FILES DO NOT MATCH !!!')
        return False


def compare_files_by_size(filepath_1, filepath_2):
    """ Compares two files based on their size """

    start_ts = datetime.now()
    f1_size = os.stat(filepath_1).st_size
    f2_size = os.stat(filepath_2).st_size
    sizes_are_equal = f1_size == f2_size

    log.info('--------------------------------------')
    log.info('Comparing file "%s" to file "%s"', filepath_1, filepath_2)
    log.info('Size of File 1: %d', f1_size)
    log.info('Size of File 2: %d', f2_size)

    if sizes_are_equal:
        log.info('!!! FILES ARE OF EQUAL SIZE !!!')
    else:
        log.info('!!! FILES ARE DIFFERENT SIZES !!!')

    return sizes_are_equal

