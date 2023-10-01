from threading import Thread, Event
from time import sleep
import sys
import os
from contextlib import contextmanager
import tempfile

@contextmanager
def temp_fifo():
    """Context Manager for creating named pipes with temporary names."""
    tmpdir = tempfile.mkdtemp()
    filename = os.path.join(tmpdir, 'fifo')  # Temporary filename
    os.mkfifo(filename)  # Create FIFO
    try:
        yield filename
    finally:
        os.unlink(filename)  # Remove file
        os.rmdir(tmpdir)  # Remove directory

def task(event: Event, id: int) -> None:
    print(f'Thread {id} started. Waiting for the signal....')
    event.wait()

    while True:
        if event.is_set():
            print(f'Received signal. The thread {id} was completed.')
            event.clear()


def main() -> None:
    event = Event()

    t1 = Thread(target=task, args=(event,1))
    t2 = Thread(target=task, args=(event,2))

    t1.start()
    t2.start()

    while True:
        try:
            with temp_fifo() as fifo_file:
                # Pass the fifo_file filename e.g. to some other process to read from.
                # Write something to the pipe 
                with open(fifo_file, 'r') as f:
                    f.read()
                    print('Blocking the main thread for 3 seconds...')
                    sleep(3) 
                    event.set()
        except KeyboardInterrupt:
            sys.exit()



if __name__ == '__main__':
    main()
