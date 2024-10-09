import sys
import task


if __name__ == '__main__':
    if len(sys.argv) < 2: 
        task.notify_job();
    else :
        notify_thread = task.getTaskJobThread()
        notify_thread.start()

