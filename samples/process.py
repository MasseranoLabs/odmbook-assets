import glob
from pyodm import Node, exceptions

node = Node("localhost", 3000)

try:
    # Get all JPG files in directory
    images = glob.glob("*.JPG") + glob.glob("*.jpg") + glob.glob("*.JPEG") + glob.glob("*.jpeg")

    print("Uploading images...")
    task = node.create_task(images, {'dsm': True, 'orthophoto-resolution': 2})
    print(task.info())

    try:
        def print_status(task_info):
            msecs = task_info.processing_time
            seconds = int((msecs / 1000) % 60)
            minutes = int((msecs / (1000 * 60)) % 60)
            hours = int((msecs / (1000 * 60 * 60)) % 24)
            print("Task is running: %02d:%02d:%02d" % (hours, minutes, seconds), end="\r")
        task.wait_for_completion(status_callback=print_status)

        print("Task completed, downloading results...")

        # Retrieve results
        def print_download(progress):
            print("Download: %s%%" % progress, end="\r")
        task.download_assets("./results", progress_callback=print_download)

        print("Assets saved in ./results")
    except exceptions.TaskFailedError as e:
        print("\n".join(task.output()))

except exceptions.NodeConnectionError as e:
    print("Cannot connect: %s" % e)
except exceptions.OdmError as e:
    print("Error: %s" % e)