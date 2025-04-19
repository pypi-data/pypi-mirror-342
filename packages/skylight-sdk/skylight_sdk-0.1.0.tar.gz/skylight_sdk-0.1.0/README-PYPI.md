# skylight-sdk

Developer-friendly & type-safe Python SDK specifically catered to leverage *skylight-sdk* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=skylight-sdk&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>

 
<!-- Start Summary [summary] -->
## Summary

Skylight API: Skylight API Documentation


        # Skylight API Documentation
        
        This API allows you to interact with Windows instances.
        
        ## Authentication
        
        All endpoints require API key authentication. Include your API key in the `X-API-Key` header.
         
        ## Support
        
        For support, please join our discord.
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [skylight-sdk](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#skylight-sdk)
  * [SDK Installation](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#sdk-installation)
  * [IDE Support](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#ide-support)
  * [SDK Example Usage](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#sdk-example-usage)
  * [Authentication](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#authentication)
  * [Available Resources and Operations](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#available-resources-and-operations)
  * [Retries](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#retries)
  * [Error Handling](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#error-handling)
  * [Server Selection](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#server-selection)
  * [Custom HTTP Client](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#custom-http-client)
  * [Resource Management](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#resource-management)
  * [Debugging](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#debugging)
* [Development](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#development)
  * [Maturity](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#maturity)
  * [Contributions](https://github.com/skylight-ai/skylight-python-sdk/blob/master/#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install skylight-sdk
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add skylight-sdk
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from skylight-sdk python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "skylight-sdk",
# ]
# ///

from skylight_sdk import Skylight

sdk = Skylight(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
import os
from skylight_sdk import Skylight


with Skylight(
    apikey=os.getenv("SKYLIGHT_APIKEY", ""),
) as skylight:

    res = skylight.windows.start()

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import os
from skylight_sdk import Skylight

async def main():

    async with Skylight(
        apikey=os.getenv("SKYLIGHT_APIKEY", ""),
    ) as skylight:

        res = await skylight.windows.start_async()

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name     | Type   | Scheme  | Environment Variable |
| -------- | ------ | ------- | -------------------- |
| `apikey` | apiKey | API key | `SKYLIGHT_APIKEY`    |

To authenticate with the API the `apikey` parameter must be set when initializing the SDK client instance. For example:
```python
import os
from skylight_sdk import Skylight


with Skylight(
    apikey=os.getenv("SKYLIGHT_APIKEY", ""),
) as skylight:

    res = skylight.windows.start()

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [agent](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/agent/README.md)

* [run](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/agent/README.md#run) - Run Agent
* [stop](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/agent/README.md#stop) - Stop Agent
* [answer](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/agent/README.md#answer) - Respond To Agent
* [status](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/agent/README.md#status) - Get Agent State

### [files](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/files/README.md)

* [upload](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/files/README.md#upload) - Upload To Vm
* [download](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/files/README.md#download) - Get File

### [interact](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/interact/README.md)

* [click](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/interact/README.md#click) - Click
* [drag](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/interact/README.md#drag) - Drag
* [screenshot](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/interact/README.md#screenshot) - Take Screenshot
* [move](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/interact/README.md#move) - Move Mouse
* [keypress](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/interact/README.md#keypress) - Keypress
* [type](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/interact/README.md#type) - Type Text
* [scroll](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/interact/README.md#scroll) - Scroll
* [install](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/interact/README.md#install) - Install Applications


### [windows](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/windows/README.md)

* [start](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/windows/README.md#start) - Start Instance
* [pause](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/windows/README.md#pause) - Pause Instance
* [resume](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/windows/README.md#resume) - Resume Instance
* [terminate](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/windows/README.md#terminate) - Terminate Instance
* [state](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/windows/README.md#state) - Get Instance State
* [instances](https://github.com/skylight-ai/skylight-python-sdk/blob/master/docs/sdks/windows/README.md#instances) - Get All Instances

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
import os
from skylight_sdk import Skylight
from skylight_sdk.utils import BackoffStrategy, RetryConfig


with Skylight(
    apikey=os.getenv("SKYLIGHT_APIKEY", ""),
) as skylight:

    res = skylight.windows.start(,
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
import os
from skylight_sdk import Skylight
from skylight_sdk.utils import BackoffStrategy, RetryConfig


with Skylight(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    apikey=os.getenv("SKYLIGHT_APIKEY", ""),
) as skylight:

    res = skylight.windows.start()

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

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

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `start_async` method may raise the following exceptions:

| Error Type                        | Status Code | Content Type     |
| --------------------------------- | ----------- | ---------------- |
| models.ForbiddenErrorResponse     | 403         | application/json |
| models.HTTPValidationError        | 422         | application/json |
| models.WindowsModelsErrorResponse | 500         | application/json |
| models.APIError                   | 4XX, 5XX    | \*/\*            |

### Example

```python
import os
from skylight_sdk import Skylight, models


with Skylight(
    apikey=os.getenv("SKYLIGHT_APIKEY", ""),
) as skylight:
    res = None
    try:

        res = skylight.windows.start()

        # Handle response
        print(res)

    except models.ForbiddenErrorResponse as e:
        # handle e.data: models.ForbiddenErrorResponseData
        raise(e)
    except models.HTTPValidationError as e:
        # handle e.data: models.HTTPValidationErrorData
        raise(e)
    except models.WindowsModelsErrorResponse as e:
        # handle e.data: models.WindowsModelsErrorResponseData
        raise(e)
    except models.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
import os
from skylight_sdk import Skylight


with Skylight(
    server_url="https://api.launchskylight.com",
    apikey=os.getenv("SKYLIGHT_APIKEY", ""),
) as skylight:

    res = skylight.windows.start()

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from skylight_sdk import Skylight
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Skylight(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from skylight_sdk import Skylight
from skylight_sdk.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Skylight(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Skylight` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
import os
from skylight_sdk import Skylight
def main():

    with Skylight(
        apikey=os.getenv("SKYLIGHT_APIKEY", ""),
    ) as skylight:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Skylight(
        apikey=os.getenv("SKYLIGHT_APIKEY", ""),
    ) as skylight:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from skylight_sdk import Skylight
import logging

logging.basicConfig(level=logging.DEBUG)
s = Skylight(debug_logger=logging.getLogger("skylight_sdk"))
```

You can also enable a default debug logger by setting an environment variable `SKYLIGHT_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=skylight-sdk&utm_campaign=python)
