#
<div align=center>
    <img src="./azure-iot-device/doc/images/azure_iot_sdk_python_banner.png"></img>
    <h1> V2 - We are now GA! </h1>
</div>

![Build Status](https://azure-iot-sdks.visualstudio.com/azure-iot-sdks/_apis/build/status/Azure.azure-iot-sdk-python)

This repository contains code for the Azure IoT SDKs for Python.  This enables python developers to easily create IoT device solutions that seamlessly
connect to the Azure IoT Hub ecosystem.

*If you're looking for the v1.x.x client library, it is now preserved in the [v1-deprecated](https://github.com/Azure/azure-iot-sdk-python/tree/v1-deprecated) branch.*

## Azure IoT SDK for Python

This repository contains the following libraries:

* [Azure IoT Device library](https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-device/README.md). 
    * [API Reference](https://docs.microsoft.com/en-us/python/api/azure-iot-device)

* [Azure IoT Hub Service library](https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-hub/README.md)
     * [API Reference](https://docs.microsoft.com/en-us/python/api/azure-iot-hub)

* Coming Soon: Azure IoT Device Provisioning Service Library

## Critical Upcoming Changes Notice

### Certificates
All Azure IoT SDK users are advised to be aware of upcoming TLS certificate changes for Azure IoT Hub and Device Provisioning Service 
that will impact the SDK's ability to connect to these services. In October 2022, both services will migrate from the current 
[Baltimore CyberTrust CA Root](https://baltimore-cybertrust-root.chain-demos.digicert.com/info/index.html) to the 
[DigiCert Global G2 CA root](https://global-root-g2.chain-demos.digicert.com/info/index.html). There will be a 
transition period beforehand where your IoT devices must have both the Baltimore and Digicert public certificates 
installed in their certificate store in order to prevent connectivity issues.

**Devices with only the Baltimore public certificate installed will lose the ability to connect to Azure IoT hub and Device Provisioning Service in October 2022.**

To prepare for this change, make sure your device's certificate store has both of these public certificates installed.

For a more in depth explanation as to why the IoT services are doing this, please see
[this article](https://techcommunity.microsoft.com/t5/internet-of-things/azure-iot-tls-critical-changes-are-almost-here-and-why-you/ba-p/2393169).

### Python 2.7 support
All Azure IoT SDK users are advised to be aware that support for Python 2.7 will be dropped in January 2022.
While existing releases will continue to function with Python 2.7 as normal, future releases beyond this point will no longer support Python 2.7

## Installing the libraries

Pip installs are provided for all of the SDK libraries in this repo:

[Device libraries](https://github.com/Azure/azure-iot-sdk-python/tree/main/azure-iot-device#installation)

[IoTHub library](https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-hub/README.md#installation)

## Using the libraries
Want to start off on the right foot? Be sure to learn about [**common pitfalls**](https://github.com/Azure/azure-iot-sdk-python/wiki/pitfalls) of using this Python SDK before starting a project.  

You can also view samples in each library:
- [Device Samples](https://github.com/Azure/azure-iot-sdk-python/tree/main/azure-iot-device/samples) cover device and Edge module scenarios.
- [IoT Hub Samples](https://github.com/Azure/azure-iot-sdk-python/tree/main/azure-iot-hub/samples) cover IoT Hub service side scenarios.


## Features

:heavy_check_mark: feature available  :heavy_multiplication_x: feature planned but not yet supported  :heavy_minus_sign: no support planned*

*Features that are not planned may be prioritized in a future release, but are not currently planned

This SDK only supports the **MQTT protocol**.

### Device Client Library ([azure-iot-device](https://github.com/Azure/azure-iot-sdk-python/tree/main/azure-iot-device))

#### IoTHub Device Client

| Features                                                                                                         | Status                     | Description                                                                                                                                                                                                          |
|------------------------------------------------------------------------------------------------------------------|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Authentication](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-security-deployment)                     | :heavy_check_mark:         | Connect your device to IoT Hub securely with supported authentication, including symmetric key, X-509 Self Signed, Certificate Authority (CA) Signed, and SASToken                                     |
| [Send device-to-cloud message](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-d2c)     | :heavy_check_mark:         | Send device-to-cloud messages (max 256KB) to IoT Hub with the option to add custom properties.                                                                                                                       |
| [Receive cloud-to-device messages](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-c2d) | :heavy_check_mark:         | Receive cloud-to-device messages and read associated custom and system properties from IoT Hub, with the option to complete/reject/abandon C2D messages.                                                        |
| [Device Twins](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-device-twins)                     | :heavy_check_mark:         | IoT Hub persists a device twin for each device that you connect to IoT Hub.  The device can perform operations like get twin tags, subscribe to desired properties.                                                |
| [Direct Methods](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-direct-methods)                 | :heavy_check_mark:         | IoT Hub gives you the ability to invoke direct methods on devices from the cloud.  The SDK supports handler for method specific and generic operation.                                                            |
| [Connection Status and Error reporting](https://docs.microsoft.com/en-us/rest/api/iothub/common-error-codes)     | :heavy_multiplication_x:   | Error reporting for IoT Hub supported error code.  *This SDK supports error reporting on authentication and Device Not Found.                                                                                         |
| Retry policies                                                                                                   | :heavy_check_mark:         | Operations which fail with a transient error and dropped connections will be retried with a fixed 10 second interval by default. This functionality can be disabled if desired, and the interval can be configured   |
| [Upload file to Blob](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-file-upload)               | :heavy_check_mark:         | A device can initiate a file upload and notifies IoT Hub when the upload is complete.  |

#### IoTHub Module Client

**Note:** IoT Edge for Python is scoped to Linux containers & devices only. [Learn more](https://techcommunity.microsoft.com/t5/internet-of-things/linux-modules-with-azure-iot-edge-on-windows-10-iot-enterprise/ba-p/1407066) about using Linux containers for IoT edge on Windows devices. 

| Features                                                                                                         | Status                     | Description                                                                                                                                                                                                          |
|------------------------------------------------------------------------------------------------------------------|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Authentication](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-security-deployment)                     | :heavy_check_mark:         | Connect your device to IoT Hub securely with supported authentication, including symmetric key, X-509 Self Signed, and Certificate Authority (CA) Signed. SASToken authentication is not currently supported.                                                   |
| [Send device-to-cloud message](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-d2c)     | :heavy_check_mark:         | Send device-to-cloud messages (max 256KB) to IoT Hub with the option to add custom properties.                                                                                                                       |
| [Receive cloud-to-device messages](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-c2d) | :heavy_check_mark:         | Receive cloud-to-device messages and read associated custom and system properties from IoT Hub, with the option to complete/reject/abandon C2D messages.                                                        |
| [Device Twins](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-device-twins)                     | :heavy_check_mark:         | IoT Hub persists a device twin for each device that you connect to IoT Hub.  The device can perform operations like get twin tags, subscribe to desired properties.                                                |
| [Direct Methods](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-direct-methods)                 | :heavy_check_mark:         | IoT Hub gives you the ability to invoke direct methods on devices from the cloud.  The SDK supports handler for method specific and generic operation.                                                            |
| [Connection Status and Error reporting](https://docs.microsoft.com/en-us/rest/api/iothub/common-error-codes)     | :heavy_multiplication_x:   | Error reporting for IoT Hub supported error code.  *This SDK supports error reporting on authentication and Device Not Found.                                                                                         |
| Retry policies                                                                                                   | :heavy_check_mark:         | Operations which fail with a transient error and dropped connections will be retried with a fixed 10 second interval.  TThis functionality can be disabled if desired, and the interval can be configured            |
| Direct Invocation of Method on Modules                                                                           | :heavy_check_mark:         | Invoke method calls to another module using using the Edge Gateway.                                                                                                                                        |

#### Provisioning Device Client

| Features                    | Status             | Description                                                                                                                                                                                                                                                                                                                                        |
|-----------------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TPM Individual Enrollment   | :heavy_minus_sign: | Provisioning via [Trusted Platform Module](https://docs.microsoft.com/en-us/azure/iot-dps/concepts-security#trusted-platform-module-tpm).                                                                                                                                                                                                          |
| X.509 Individual Enrollment | :heavy_check_mark: | Provisioning via [X.509 root certificate](https://docs.microsoft.com/en-us/azure/iot-dps/concepts-security#root-certificate).  Please review the [samples](azure-iot-device/samples/async-hub-scenarios/provision_x509.py) folder and this [quickstart](https://docs.microsoft.com/en-us/azure/iot-dps/quick-create-simulated-device-x509-python) on how to create a device client.   |
| X.509 Enrollment Group      | :heavy_check_mark: | Provisioning via [X.509 leaf certificate](https://docs.microsoft.com/en-us/azure/iot-dps/concepts-security#leaf-certificate)).  Please review the [samples](azure-iot-device/samples/async-hub-scenarios/provision_x509.py) folder on how to create a device client.                                                                                                                  |
| Symmetric Key Enrollment    | :heavy_check_mark: | Provisioning via [Symmetric key attestation](https://docs.microsoft.com/en-us/azure/iot-dps/concepts-symmetric-key-attestation)).  Please review the [samples](azure-iot-device/samples/async-hub-scenarios/provision_symmetric_key.py) folder on how to create a device client.                                                                                                               |

### IoTHub Service Library ([azure-iot-hub](https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-hub/azure/iot/hub/iothub_registry_manager.py))

#### Registry Manager

| Features                                                                                                      | Status                   | Description                                        |
|---------------------------------------------------------------------------------------------------------------|--------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| [Identity registry (CRUD)](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-identity-registry) | :heavy_check_mark:       | Use your backend app to perform CRUD operation for individual device or in bulk.                                                   |
| [Cloud-to-device messaging](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-c2d)     | :heavy_check_mark: | Use your backend app to send cloud-to-device messages, and set up cloud-to-device message receivers.                               |
| [Direct Methods operations](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-direct-methods)   | :heavy_check_mark: | Use your backend app to invoke direct method on device.  |
| [Device Twins operations](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-device-twins)       | :heavy_check_mark: | Use your backend app to perform device twin operations.  *Twin reported property update callback and replace twin are in progress. |
| [Query](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-query-language)                       | :heavy_check_mark: | Use your backend app to perform query for information.       |
| [Jobs](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-jobs)                                  | :heavy_multiplication_x: | Use your backend app to perform job operation. |

### IoTHub Provisioning Service Library

Feature is Coming Soon

| Features                                            | Status                   | Description                                                                                                                                    |
|-----------------------------------------------------|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| CRUD Operation with TPM Individual Enrollment       | :heavy_multiplication_x: | Manage device enrollment using TPM with the service SDK.                             |
| Bulk CRUD Operation with TPM Individual Enrollment  | :heavy_multiplication_x: | Bulk manage device enrollment using TPM with the service SDK.                        |
| CRUD Operation with X.509 Individual Enrollment     | :heavy_multiplication_x: | Manages device enrollment using X.509 individual enrollment with the service SDK.    |
| CRUD Operation with X.509 Group Enrollment          | :heavy_multiplication_x: | Manages device enrollment using X.509 group enrollment with the service SDK.         |
| Query enrollments                                   | :heavy_multiplication_x: | Query registration states with the service SDK.                                      |

# Releases

The Pythond SDK offers releases for new features, critical bug fixes, and Long Term Support (LTS). Versioning follows [semantic versioning](https://semver.org/), `x.y.z.` or `major.minor.patch`. Any time the version is updated, it will be tagged `x.y.z`.

## New Features and Critical Bug Fixes

New features and critical bug fixes (including security updates) will be released on the main branch. These releases will be tagged using the date formatted `yyyy-mm-dd`. A feature release will bump the `minor` version and reset the `patch` version to 0. A critical bug fix will bump the `patch` version only.

## Long Term Support (LTS)

The project offers a Long Term Support (LTS) version to allow users that do not need the latest features to be shielded from unwanted changes.

LTS branches receive all bug fixes that fall in one of these categories:

- security bugfixes
- critical bugfixes (crashes, memory leaks, etc.)

No new features or improvements will be picked up in an LTS branch.

LTS branches are named `lts_mm_yyyy`, where *mm* and *yyyy* are the month and year when the branch was created. An example of such a branch is `lts_07_2017`.

### LTS Schedule<sup>1</sup>

*The first LTS version of the Python SDK is scheduled to be available in early 2022*

Below is a table showing the mapping of the LTS branches to the packages released.

  | PIP Package | GitHub Branch | LTS Tag | LTS Start Date | Maintenance End Date |
  | :-----: | :-----------: | :-----: | :------------: | :------------------: |
  | N/A     |               |         |                |                      |  

<sup>1</sup> All scheduled dates are subject to change by the Azure IoT SDK team.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
