# UAI Annotation Requests
<!-- Start Summary [summary] -->
## Summary

UAI Annotation Requests: The API lets a client request annotations from UAI, track the progress of the work and fetch the result annotations.
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [UAI Annotation Requests](#uai-annotation-requests)
  * [Example Usage](#example-usage)
  * [Authentication](#authentication)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Error Handling](#error-handling)

<!-- End Table of Contents [toc] -->

<!-- No SDK Installation [installation] -->

<!-- No IDE Support [idesupport] -->

## Example Usage

### Example

Below is an example of how an annotation request with data can be submitted to UAI for annotation.

```python
from uai_annotation_requests import UaiAnnotationRequests
from uai_annotation_requests_util import uai_oauth2, uai_upload_data

with UaiAnnotationRequests(
    uai_oauth2=uai_oauth2("<client_id>", "<client_secret>"),
) as uar_client:

    res = uar_client.annotation_request.create(project_id="<id>", clips=[
        {
            "clip_reference_id": "clip_reference_01",
            "display_name": "my first clip",
        },
    ], request_reference_id="request_reference_01", priority=0, display_name="my annotation request")

    # Handle response
    print(res)

    # Upload data directory for each defined clip
    # The upload step here is only relevant for projects
    # That are uploading archived data to UAI where no
    # bucket integration is configured.
    for clip in res.clips:
        uai_upload_data(res, clip, path_to_data)

```
<!-- No SDK Example Usage [usage] -->

## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name         | Type   | Scheme       |
| ------------ | ------ | ------------ |
| `uai_oauth2` | oauth2 | uai_oauth2 helper or OAuth2 token |

To authenticate with the API the `uai_oauth2` parameter must be set when initializing the SDK client instance.
The `uai_oauth2` parameter accepts either the `uai_oauth2` helper login function or an OAuth2 token. For example:
```python
from uai_annotation_requests import UaiAnnotationRequests
from uai_annotation_requests_util import uai_oauth2

with UaiAnnotationRequests(
    uai_oauth2=uai_oauth2(client_id="<UAI_CLIENT_ID>", client_secret="<UAI_CLIENT_SECRET>"),
) as uar_client:

    res = uar_client.annotation_request.create(project_id="<id>", clips=[
        {
            "clip_reference_id": "clip_reference_01",
            "display_name": "my first clip",
        },
    ], request_reference_id="request_reference_01", priority=0, display_name="my annotation request")

    # Handle response
    print(res)

```
<!-- No Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [annotation_request](docs/sdks/annotationrequest/README.md)

* [create](docs/sdks/annotationrequest/README.md#create) - Create a new annotation request
* [get](docs/sdks/annotationrequest/README.md#get) - Get annotation request
* [get_filtered](docs/sdks/annotationrequest/README.md#get_filtered) - Get annotation requests filtered by projectId and phase.
* [get_by_annotation_request_id](docs/sdks/annotationrequest/README.md#get_by_annotation_request_id) - Get annotation request by the annotation request ID
* [get_exported_annotations](docs/sdks/annotationrequest/README.md#get_exported_annotations) - Request the download URLs for the result annotations.


</details>
<!-- End Available Resources and Operations [operations] -->

<!-- No Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.APIError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `get_async` method may raise the following exceptions:

| Error Type                          | Status Code | Content Type     |
| ----------------------------------- | ----------- | ---------------- |
| models.AnnotationRequestNotFoundDTO | 404         | application/json |
| models.APIError                     | 4XX, 5XX    | \*/\*            |

### Example

```python
import uai_annotation_requests
from uai_annotation_requests import UaiAnnotationRequests, models


with UaiAnnotationRequests(
    uai_oauth2="<YOUR_UAI_OAUTH2_HERE>",
) as uar_client:
    res = None
    try:

        res = uar_client.annotation_request.get(project_id="<id>", field=uai_annotation_requests.FilterField.REQUEST_REFERENCE_ID, value="<value>")

        # Handle response
        print(res)

    except models.AnnotationRequestNotFoundDTO as e:
        # handle e.data: models.AnnotationRequestNotFoundDTOData
        raise(e)
    except models.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- No Server Selection [server] -->

<!-- No Custom HTTP Client [http-client] -->

<!-- No Resource Management [resource-management] -->

<!-- No Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->
