# Automations

Methods:

- <code title="post /automations">client.automations.<a href="./src/ittybit/resources/automations.py">create</a>(\*\*<a href="src/ittybit/types/automation_create_params.py">params</a>) -> None</code>

# Files

Types:

```python
from ittybit.types import FileCreateResponse, FileListResponse
```

Methods:

- <code title="post /files">client.files.<a href="./src/ittybit/resources/files.py">create</a>(\*\*<a href="src/ittybit/types/file_create_params.py">params</a>) -> <a href="./src/ittybit/types/file_create_response.py">FileCreateResponse</a></code>
- <code title="get /files/{id}">client.files.<a href="./src/ittybit/resources/files.py">retrieve</a>(id) -> None</code>
- <code title="get /files">client.files.<a href="./src/ittybit/resources/files.py">list</a>(\*\*<a href="src/ittybit/types/file_list_params.py">params</a>) -> <a href="./src/ittybit/types/file_list_response.py">FileListResponse</a></code>
- <code title="delete /files/{id}">client.files.<a href="./src/ittybit/resources/files.py">delete</a>(id) -> None</code>

# Media

Methods:

- <code title="post /media">client.media.<a href="./src/ittybit/resources/media.py">create</a>(\*\*<a href="src/ittybit/types/media_create_params.py">params</a>) -> None</code>

# Tasks

Types:

```python
from ittybit.types import TaskCreateResponse
```

Methods:

- <code title="post /tasks">client.tasks.<a href="./src/ittybit/resources/tasks.py">create</a>(\*\*<a href="src/ittybit/types/task_create_params.py">params</a>) -> <a href="./src/ittybit/types/task_create_response.py">object</a></code>

# Upload

Types:

```python
from ittybit.types import UploadUploadResponse
```

Methods:

- <code title="post /uploads">client.upload.<a href="./src/ittybit/resources/upload.py">upload</a>(\*\*<a href="src/ittybit/types/upload_upload_params.py">params</a>) -> <a href="./src/ittybit/types/upload_upload_response.py">UploadUploadResponse</a></code>
