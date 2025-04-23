
# Getting Started with Neutrino API

## Introduction

The general-purpose API

## Install the Package

The package is compatible with Python versions `3.7+`.
Install the package from PyPi using the following pip command:

```bash
pip install neutrino-api-sdk==1.0.0
```

You can also view the package at:
https://pypi.python.org/pypi/neutrino-api-sdk/1.0.0

## Initialize the API Client

**_Note:_** Documentation for the client can be found [here.](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/client.md)

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| environment | `Environment` | The API environment. <br> **Default: `Environment.MULTICLOUD`** |
| http_client_instance | `HttpClient` | The Http Client passed from the sdk user for making requests |
| override_http_client_configuration | `bool` | The value which determines to override properties of the passed Http Client from the sdk user |
| http_call_back | `HttpCallBack` | The callback value that is invoked before and after an HTTP call is made to an endpoint |
| timeout | `float` | The value to use for connection timeout. <br> **Default: 60** |
| max_retries | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| backoff_factor | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| retry_statuses | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| retry_methods | `Array of string` | The http methods on which retry is to be done. <br> **Default: ['GET', 'PUT']** |
| logging_configuration | [`LoggingConfiguration`](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/logging-configuration.md) | The SDK logging configuration for API calls |
| user_id_credentials | [`UserIdCredentials`](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/auth/custom-header-signature.md) | The credential object for Custom Header Signature |
| api_key_credentials | [`ApiKeyCredentials`](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/auth/custom-header-signature-1.md) | The credential object for Custom Header Signature |

The API client can be initialized as follows:

```python
client = NeutrinoapiClient(
    user_id_credentials=UserIdCredentials(
        user_id='user-id'
    ),
    api_key_credentials=ApiKeyCredentials(
        api_key='api-key'
    ),
    environment=Environment.MULTICLOUD,
    logging_configuration=LoggingConfiguration(
        log_level=logging.INFO,
        request_logging_config=RequestLoggingConfiguration(
            log_body=True
        ),
        response_logging_config=ResponseLoggingConfiguration(
            log_headers=True
        )
    )
)
```

## Environments

The SDK can be configured to use a different environment for making API calls. Available environments are:

### Fields

| Name | Description |
|  --- | --- |
| Multicloud | **Default** |
| AWS | - |
| GCP | - |
| Backup | - |
| EU | - |
| AUS | - |
| USA | - |

## Authorization

This API uses the following authentication schemes.

* [`user-id (Custom Header Signature)`](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/auth/custom-header-signature.md)
* [`api-key (Custom Header Signature)`](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/auth/custom-header-signature-1.md)

## List of APIs

* [Data Tools](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/controllers/data-tools.md)
* [Securityand Networking](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/controllers/securityand-networking.md)
* [Imaging](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/controllers/imaging.md)
* [Telephony](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/controllers/telephony.md)
* [Geolocation](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/controllers/geolocation.md)
* [E-Commerce](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/controllers/e-commerce.md)
* [WWW](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/controllers/www.md)

## SDK Infrastructure

### Configuration

* [AbstractLogger](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/abstract-logger.md)
* [LoggingConfiguration](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/logging-configuration.md)
* [RequestLoggingConfiguration](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/request-logging-configuration.md)
* [ResponseLoggingConfiguration](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/response-logging-configuration.md)

### HTTP

* [HttpResponse](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/http-response.md)
* [HttpRequest](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/http-request.md)

### Utilities

* [ApiResponse](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/api-response.md)
* [ApiHelper](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/api-helper.md)
* [HttpDateTime](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/http-date-time.md)
* [RFC3339DateTime](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/rfc3339-date-time.md)
* [UnixDateTime](https://www.github.com/sdks-io/neutrino-api-python-sdk/tree/1.0.0/doc/unix-date-time.md)

