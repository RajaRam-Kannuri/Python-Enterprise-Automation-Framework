from enum import StrEnum


class SupportedImages(StrEnum):
    UBUNTU_20_SELENIUM = "ubuntu20-selenium"
    UBUNTU_22 = "ubuntu-22-pkr-v1-4"
    WINDOWS_19_SELENIUM = "windows2019-selenium"
    DEBIAN_CHROMIUM = "eu.gcr.io/dev-alemira/chromium-vnc:latest"
