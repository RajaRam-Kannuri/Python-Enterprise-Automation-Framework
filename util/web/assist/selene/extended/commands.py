import base64

from selene.core.command import *
from selene.core.wait import Command


def scroll_by_offset(x: int = 0, y: int = 0) -> Command:
    return Command(f"scroll page by x={x} y={y}", lambda element: element.execute_script(f"window.scrollBy({x}, {y});"))


scroll_to_top = Command("scroll up the page", lambda element: element.execute_script("window.scrollTo(0, 0);"))


def upload_file_with_drag_and_drop(file_content: bytes, file_name: str, file_type: str) -> Command:
    # Convert the bytes object file_data to a string before serializing it to JSON
    file_data = base64.b64encode(file_content).decode("utf-8")
    drag_and_drop_script = """
            const file_data = arguments[0];
            const file_name= arguments[1];
            const file_type= arguments[2];

            // Create a new Event
            const dropEvent = new Event('drop', {
                bubbles: true,
                cancelable: true
            });

            // Create a DataTransfer object
            const dataTransfer = new DataTransfer();

            // Create a new File object with the file data

            const binaryData = new Uint8Array(atob(file_data).split('').map(char => char.charCodeAt(0)));

            const newFile = new File([binaryData], file_name, { type: file_type });

            // Add the file to the DataTransfer object
            dataTransfer.items.add(newFile);

            // Attach the DataTransfer object to the drop event
            dropEvent.dataTransfer = dataTransfer;

            // Dispatch the drop event on the drop area element
            self.dispatchEvent(dropEvent);
    """

    return Command(
        f"Upload file {file_name} via drag and drop",
        lambda element: element.execute_script(drag_and_drop_script, file_data, file_name, file_type),
    )
