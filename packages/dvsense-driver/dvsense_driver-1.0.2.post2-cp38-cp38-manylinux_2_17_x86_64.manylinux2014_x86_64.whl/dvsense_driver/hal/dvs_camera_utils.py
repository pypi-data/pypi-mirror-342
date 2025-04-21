import sys
from dvsense_driver.base import Event2D
try:
    from dvsense_hal_py import INTERFACE_TYPE
    from dvsense_hal_py import CAMERA_TYPE
    from dvsense_hal_py import RawEventStreamEncodingType
    from dvsense_hal_py import CameraDescription
    from dvsense_hal_py import RawEventStreamFormat
except ImportError as e:
    print("ImportError: please install dvsense-driver SDK. ")
    sys.exit(1)
