#!/usr/bin/env python

import linecache
import logging
import os

from datetime import datetime

log = logging.getLogger(__name__)

UPDATE_AFTER_PROCESSED_LINES = 5000


def _print_comparison_report(start_ts, end_ts, counts):
    time_diff = end_ts - start_ts
    time_diff_in_secs = time_diff.total_seconds()
    time_diff_in_minutes = '%dmins, %dsecs' % (time_diff_in_secs / 60, time_diff_in_secs % 60)

    log.info('--------------------------------------')
    log.info('Ending file comparison at: %s', end_ts)
    log.info('Elapsed Time In Seconds: %d', time_diff_in_secs)
    log.info('Execution Time: %s', time_diff_in_minutes)
    log.info('Total Lines Compared: %d', counts['iterations'])
    log.info('Match Count: %d', counts['matches'])
    log.info('Miss Count: %d', counts['misses'])
    log.info('--------------------------------------')

    if counts['misses'] == 0 and counts['f1_lines'] == counts['f2_lines']:
        log.info('!!! FILES PROBABLY MATCH !!!')
    else:
        log.warning('!!! FILES DEFINITELY DO NOT MATCH !!!')

def _finalize(main_file, start_ts, end_ts, counts):
    main_file.close()
    _print_comparison_report(
        start_ts=start_ts,
        end_ts=end_ts,
        counts=counts,
    )

def file_sizes_are_equal(filepath_1, filepath_2):
    return os.stat(filepath_1).st_size == os.stat(filepath_2).st_size

def compare_files(filepath_1, filepath_2, allow_size_disparity=False):

    start_ts = datetime.now()
    end_ts = None
    file_sizes_are_not_equal = False
    counts = {
        'iterations': 0,
        'f1_lines': 0,
        'f2_lines': 0,
        'matches': 0,
        'misses': 0,
    }

    log.info('Starting file comparison at: %s', start_ts)
    log.info('Comparing file "%s" to file "%s"', filepath_1, filepath_2)

    """
    It would be ideal if we could strip whitespace from each line of both files prior
    to comparing them, but this is not feasible. Consequently file size ends up being
    somewhat of a crude comparison.
    """
    if not file_sizes_are_equal(filepath_1, filepath_2):
        log.warning('!!! FILE SIZES ARE NOT EQUAL !!!')

        if allow_size_disparity:
            file_sizes_are_not_equal = True
        else:
            return
    else:
        log.info('File sizes are equal.')

    with open(filepath_1) as f1_handle:
        
        for f1_line in f1_handle:

            counts['iterations'] += 1
            counts['f1_lines'] += 1
            counts['f2_lines'] += 1

            if counts['iterations'] % UPDATE_AFTER_PROCESSED_LINES == 0:
                log.info('%d lines processed...', counts['iterations'])

            f1_line = f1_line.strip()

            # TODO - potential alternative
            # Instead of using linecache...
            # For every line from F1, take note of line length.
            # Use F1's line length in conjunction with `F2.seek()` to extract the corresponding line from F2.
            # If at any point comparisons don't match, then there are differences in the file.
            f2_line = linecache.getline(filepath_2, counts['iterations']).strip()

            if f1_line == f2_line:
                counts['matches'] += 1
            else:
                counts['misses'] += 1

                """
                File sizes do not match but we're allowing comparison in any case.
                That's all well and good, but don't print out the lines for this scenario,
                since it's likely that most of the lines don't match, which would result
                in most of the lines of potentially YUGE files being printed to stdout.
                """
                if not file_sizes_are_not_equal:
                    log.debug('-------------------')
                    log.debug('F1 Line: %s', f1_line)
                    log.debug('-------')
                    log.debug('F2 Line: %s', f2_line)

    return _finalize(
        main_file=f1_handle,
        start_ts=start_ts,
        end_ts=datetime.now(),
        counts=counts,
    )
