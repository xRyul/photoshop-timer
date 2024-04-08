import os
import time
import curses

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

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


def main(stdscr):
    # Wait for a while before starting to ensure all images are opened
    # time.sleep(10)

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
                active_doc = current_doc
                start_time = time.time()
                history_count = current_history_count  # Reset history count for the new active document
            else:
                # Update history count for active document
                history_count = current_history_count

            # Display times and history counts for all documents
            for i, (doc, (elapsed_time, doc_history_count)) in enumerate(doc_times.items()):
                stdscr.addstr(i, 0, 'Document {} was active for {} with {} history states'.format(doc, format_time(elapsed_time), doc_history_count))

            # Display timer and history count for active document
            if active_doc:
                elapsed_time = time.time() - start_time
                stdscr.addstr(len(doc_times), 0, 'Document {} has been active for {} with {} history states'.format(active_doc, format_time(elapsed_time), history_count))
            else:
                stdscr.addstr(len(doc_times), 0, 'No active document')


            stdscr.refresh()  # Refresh the screen to update the printed text
            time.sleep(1)

        except Exception as e:
            stdscr.addstr(0, 0, "An error occurred: {}".format(e))
            stdscr.refresh()  # Refresh the screen to update the printed text
            # Continue execution even if an error occurred
            continue

if __name__ == '__main__':
    curses.wrapper(main)

