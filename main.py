import os
import time
import curses

def get_active_photoshop_document_and_history_count():
    applescript = """
    tell application "Adobe Photoshop 2024"
        if (count of documents) > 0 then
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

def main(stdscr):
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
                    stdscr.addstr(0, 0, 'Document {} was active for {:.2f} seconds with {} history states'.format(active_doc, elapsed_time, history_count))
                    stdscr.refresh()  # Refresh the screen to update the printed text
                active_doc = current_doc
                history_count = current_history_count
                start_time = time.time()

            # Display times for all documents
            for i, (doc, (elapsed_time, history_count)) in enumerate(doc_times.items()):
                stdscr.addstr(i, 0, 'Document {} was active for {:.2f} seconds with {} history states'.format(doc, elapsed_time, history_count))

            # Display timer for active document
            if active_doc:
                elapsed_time = time.time() - start_time
                stdscr.addstr(len(doc_times), 0, 'Document {} has been active for {:.2f} seconds with {} history states'.format(active_doc, elapsed_time, history_count))
            else:
                stdscr.addstr(len(doc_times), 0, 'No active document')

            stdscr.refresh()  # Refresh the screen to update the printed text
            time.sleep(1)

        except Exception as e:
            stdscr.addstr(0, 0, "An error occurred: {}".format(e))
            stdscr.refresh()  # Refresh the screen to update the printed text
            break

if __name__ == '__main__':
    curses.wrapper(main)
