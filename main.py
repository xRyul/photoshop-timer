import os
import time
import curses
from pyfiglet import Figlet
import csv

def get_active_photoshop_document_and_history_count():
    applescript = """
    tell application "Adobe Photoshop 2024"
        if (count of documents) > 0 then
            # delay 2  -- Wait for 2 seconds to ensure the document is fully loaded
            set docName to the name of the current document
            set historyCount to the count of the history states of the current document
            return docName & "," & historyCount
        else
            return ""
        end if
    end tell
    """
    osa_command = 'osascript -e \'{}\''.format(applescript)
    result = os.popen(osa_command).read().strip()
    if result:
        doc_name, history_count = result.split(',')
        return doc_name, int(history_count)
    else:
        return "", 0

def format_time(seconds, ascii_art=False):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_str = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    
    if ascii_art:
        f = Figlet(font='starwars')
        return f.renderText(time_str)
    else:
        return time_str


def main(stdscr):

    try:

        # Set up logging
        with open('processed_files.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Department", "Filename", "Execution Time", "History Steps"])

        # Enable scrolling
        stdscr.scrollok(True)
        stdscr.idlok(True)

        active_doc, history_count = get_active_photoshop_document_and_history_count()
        start_time = time.time()
        doc_times = {}

        while True:
            try:
                # Clear console output
                stdscr.clear()

                current_doc, current_history_count = get_active_photoshop_document_and_history_count()

                # Start timer for new active document
                if current_doc != active_doc:
                    if active_doc:
                        elapsed_time = time.time() - start_time
                        doc_times[active_doc] = (elapsed_time, history_count)
                        with open('processed_files.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([active_doc[:2], active_doc, format_time(elapsed_time), history_count])
                    active_doc = current_doc
                    start_time = time.time()
                    history_count = current_history_count  # Reset history count for the new active document
                else:
                    # Update history count for active document
                    history_count = current_history_count

                # Display timer and history count for active document
                if active_doc:
                    elapsed_time = time.time() - start_time
                    stdscr.addstr(0, 0, 'Document {} with {} history states, has been active for:'.format(active_doc, history_count))
                    ascii_art_timer = format_time(elapsed_time, ascii_art=True).split('\n')
                    for i, line in enumerate(ascii_art_timer):
                        stdscr.addstr(i+1, 0, line)
                else:
                    stdscr.addstr(0, 0, 'No active document')

                # Display times and history counts for all documents
                max_y, max_x = stdscr.getmaxyx()  # Get the size of the window
                for i, (doc, (elapsed_time, doc_history_count)) in enumerate(doc_times.items()):
                    if i+len(ascii_art_timer)+3 < max_y:  # Ensure we're not trying to print outside the window
                        stdscr.addstr(i+len(ascii_art_timer)+3, 0, 'Document {} was active for: {} with {} history states'.format(doc, format_time(elapsed_time), doc_history_count))

                stdscr.refresh()  # Refresh the screen to update the printed text
                time.sleep(1)

            except Exception as e:
                stdscr.addstr(0, 0, "An error occurred: {}".format(e))
                stdscr.refresh()  # Refresh the screen to update the printed text
                # Continue execution even if an error occurred
                continue

    except KeyboardInterrupt:
        print("Received keyboard interrupt, quitting...")
        exit(0)

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Received keyboard interrupt, quitting...")
        exit(0)