import io

from fastapi.testclient import TestClient

from square_file_store.main import (
    app,
)

client = TestClient(app)


def upload_document():
    file_content = b"Hello, this is the content of the file."
    file_name = "example.txt"

    # Create an in-memory byte stream
    file = io.BytesIO(file_content)

    files = {"file": (file_name, file, "multipart/form-data")}

    # Make the request
    response = client.post("/upload_file/v0", files=files)

    return response.json()


def test_read_main():
    #################################
    # delete file test case
    #################################

    upload_result = upload_document()
    uploaded_file_storage_token = upload_result["data"]["main"]
    params = {"file_storage_tokens": [uploaded_file_storage_token]}

    # Make the request
    response = client.delete("/delete_files/v0", params=params)

    # Assert the response status code
    assert response.status_code == 200
    delete_response = response.json()
    assert "data" in delete_response
    assert "main" in delete_response["data"]
    assert delete_response["data"]["main"] == [uploaded_file_storage_token]
