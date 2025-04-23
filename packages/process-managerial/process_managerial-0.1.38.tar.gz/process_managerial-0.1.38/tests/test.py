from process_managerial import QueueSystem
import time
from pprint import pprint

# Sample function that succeeds by adding two numbers.
def task_success(x, y):
    time.sleep(2)
    return x + y

# Sample function that fails by raising an exception.
def task_failure():
    time.sleep(1)
    raise ValueError("Intentional error for demonstration.")

# Sample function that prints a message.
def task_print(message):
    time.sleep(1)
    print(message)
    return message

def main():
    # Instantiate the QueueSystem with a process directory and log file.
    qs = QueueSystem(process_dir="processes", log_path="queue_log.txt")
    
    # Start the background worker thread.
    qs.start_queuesystem()
    
    # Queue a task that will successfully complete.
    hex_success = qs.queue_function(task_success, 5, 10)
    print(f"Queued task_success with hex: {hex_success}")
    
    # Queue a task that is designed to fail.
    hex_failure = qs.queue_function(task_failure)
    print(f"Queued task_failure with hex: {hex_failure}")
    
    # Queue a task that prints a message.
    hex_print = qs.queue_function(task_print, "Hello, QueueSystem!")
    print(f"Queued task_print with hex: {hex_print}")
    
    # Wait individually for each task to finish.
    qs.wait_until_hex_finished(hex_success)
    qs.wait_until_hex_finished(hex_failure)
    qs.wait_until_hex_finished(hex_print)
    
    # Wait until the entire queue has been processed.
    qs.wait_until_finished()
    
    # Optionally, requeue the failed task for another attempt.
    print("Requeuing the failed task...")
    qs.requeue_hex(hex_failure)
    qs.wait_until_hex_finished(hex_failure)
    
    # Stop the background worker thread.
    qs.stop_queuesystem()
    
    # Retrieve and display final task statuses.
    print("\nFinal task statuses:")
    for hex_val in qs.get_hexes():
        props = qs.get_properties(hex_val)
        pprint({
            'hex': hex_val,
            'status': props.status.name,
            'result': props.result,
            'output': props.output,
            'start_time': props.start_time,
            'end_time': props.end_time
        })
    
    # Optional: Clear tasks older than a certain datetime.
    # Uncomment the following lines to remove pickle files for tasks with a start time before the cutoff.
    # import datetime
    # cutoff_time = datetime.datetime.now() - datetime.timedelta(seconds=5)
    # qs.clear_hexes(before_date=cutoff_time)
    # print("\nCleared tasks before:", cutoff_time)

if __name__ == "__main__":
    main()
