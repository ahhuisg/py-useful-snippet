from alive_progress import alive_bar
import time

tasks = ['downloading', 'processing', 'uploading', 'cleaning up']
with alive_bar(len(tasks), title='Processing Tasks') as bar:
    for task in tasks:
        # Update the text to show the current task
        bar.text = f'Working on {task}...'
        time.sleep(1)
        bar()