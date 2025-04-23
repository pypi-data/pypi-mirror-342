#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import requests
import struct # For packing/unpacking binary data
import subprocess
import time
from enum import Enum

class ParameterType(Enum):
    STRING = 0
    INT = 1
    FLOAT = 2
    BOOL = 3
# we need to use this to get around the rc issues
class PM_Response:
    def __init__(self, rc, status_code, content):
        self.rc = rc
        self.status_code = status_code
        self.content = content

class PM:
    _lock = threading.Lock()
    _command_queue = None
    _sta_thread = None
    _pma = None
    _initialized = False

    _url = "http://localhost:8080"

    @classmethod
    def Init(cls, photometrica_path=None, port=8080, useGui=False, autoRespond=True):
        print("Entering Init method...")
        with cls._lock:
            if cls._initialized:
                print("PM already initialized.")
                return

            if photometrica_path is None:
                photometrica_path = r"C:\Program Files\Westboro Photonics\Photometrica82"

            executable_path = photometrica_path + r"\Photometrica.exe"
            try:
                print(f"Launching executable: {executable_path}")
                # Build the argument list dynamically
                args = [executable_path, f"-port={port}"]
                if not useGui:
                    args.append("-nogui")
                if not autoRespond:
                    args.append("-autorespond=false")

                # Pass the argument list to Popen
                cls._process = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                if port != 8080:
                    cls.SetPort(port)

                # cls._initialized = True
                timeout = 45  # Maximum time to wait (in seconds)
                interval = 1  # Time between checks (in seconds)
                start_time = time.time()

                while time.time() - start_time < timeout:
                    try:
                        # Send a simple GET request to check if the server is running
                        response = requests.get(cls._url)
                        if response.status_code == 200:
                            print("Server is ready.")
                            cls._initialized = True
                            return
                    except requests.ConnectionError:
                        # Server is not ready yet, wait and retry
                        pass
                    time.sleep(interval)

                # If the timeout is reached, raise an exception
                raise TimeoutError("Server did not start within the expected time.")        
            except Exception as e:
                print(f"Failed to launch executable: {e}")
                raise e

    @classmethod
    def Shutdown(cls):
        print("Entering Shutdown method...")
        with cls._lock:
            if cls._initialized:
                # Safely terminate the process created during Init()
                if hasattr(cls, "_process") and cls._process is not None:
                    print("Terminating the process...")
                    cls._process.terminate()  # Gracefully terminate the process
                    cls._process.wait()  # Wait for the process to terminate
                    cls._process = None  # Clear the process reference
                    print("Process terminated.")

                # Clean up other resources
                if cls._command_queue is not None:
                    cls._command_queue.CompleteAdding()
                    cls._sta_thread.Join()
                    cls._command_queue.Dispose()
                    cls._command_queue = None
                    cls._sta_thread = None
                    cls._pma = None

                cls._initialized = False
                print("Shutdown method completed.")
            else:
                print("PM is not initialized. Nothing to shut down.")

    @classmethod
    def SetPort(cls, port):
        PM._url = f"http://localhost:{port}" # we need to update the url to the new port
        return PM._url
    
    @classmethod
    def SendApiRequest(cls, payload, methodName):
        # Send an HTTP request to the URL defined by PM
        request_url = f"{PM._url}/api"
        request_url += f"?method={methodName}"

        headers = {'Content-Type': 'application/octet-stream'}
        response = requests.post(request_url, data=payload, headers=headers)

        # we are prepending the return_code before any of the data

        # we need a custom response which has the status code and the content, but the content is shifted by 4 bytes

        # it should also have our rc
        rc = SDK_Helper.DecodeInt(response.content[:4])
        content = response.content[4:]
        status_code = response.status_code

        return PM_Response(rc, status_code, content)

    
class SDK_Helper:
    @staticmethod
    def encode_7bit_int(value):
        """Encodes an integer using 7-bit encoding."""
        result = bytearray()
        while value >= 0x80:
            result.append((value & 0x7F) | 0x80)  # Add the lower 7 bits and set the MSB
            value >>= 7
        result.append(value & 0x7F)  # Add the last 7 bits
        return bytes(result)

    @staticmethod
    def EncodeString(string):
        """Encodes a string with a 7-bit encoded length prefix."""
        encoded_string = string.encode('utf-8')  # Encode the string as UTF-8
        length_prefix = SDK_Helper.encode_7bit_int(len(encoded_string))  # Encode the length using 7-bit encoding
        return length_prefix + encoded_string
    
    @staticmethod
    def decode_7bit_int(binary):
        """Decodes an integer using 7-bit encoding."""
        result = 0
        shift = 0
        for byte in binary:
            result |= (byte & 0x7F) << shift
            if (byte & 0x80) == 0:  # If MSB is not set, this is the last byte
                break
            shift += 7
        return result

    @staticmethod
    def DecodeString(binary):
        """Decodes a string with a 7-bit encoded length prefix."""
        # Decode the length prefix
        length = SDK_Helper.decode_7bit_int(binary)
        
        # Find the number of bytes used for the length prefix
        length_prefix_size = 0
        for byte in binary:
            length_prefix_size += 1
            if (byte & 0x80) == 0:  # Stop when MSB is not set
                break
        
        # Extract and decode the string
        string_data = binary[length_prefix_size:length_prefix_size + length]
        return string_data.decode('utf-8')
        
    @staticmethod
    def EncodeFloat(float_value):
        return struct.pack('f', float_value)
    
    @staticmethod
    def DecodeFloat(binary):
        if (len(binary) < 4):
            return
        return struct.unpack('f', binary)[0]
    
    @staticmethod
    def EncodeInt(int_value):
        return struct.pack('i', int_value)
    
    @staticmethod
    def DecodeInt(binary):
        if (len(binary) < 4):
            return
        return struct.unpack('i', binary)[0]
    
    @staticmethod
    def EncodeBool(bool_value):
        return struct.pack('?', bool_value)
    
    @staticmethod
    def DecodeBool(binary):
        print(binary)
        if (len(binary) < 1):
            return False
        return struct.unpack('?', binary)[0]
    
    @staticmethod
    def EncodeDouble(double_value):
        return struct.pack('d', double_value)
    
    @staticmethod
    def DecodeDouble(binary):
        if (len(binary) < 8):
            return
        return struct.unpack('d', binary)[0]
    
    @staticmethod
    def EncodeByte(byte_value):
        return struct.pack('b', byte_value)
    
    @staticmethod
    def DecodeByte(binary):
        if (len(binary) < 1):
            return
        return struct.unpack('b', binary)[0]

    @staticmethod
    def DecodeFloatArray(binary):
        if (len(binary) < 4): # there should at least be 4 bytes for the length
            return []
        length = struct.unpack('i', binary[:4])[0]
        if (len(binary) < 4 + length * 4): # content length should be 4 + length * 4
            return []
        return struct.unpack('f'*length, binary[4:])
    
    @staticmethod
    def EncodeFloatArray(float_array):
        binary = struct.pack('i', len(float_array))
        for f in float_array:
            binary += struct.pack('f', f)
        return binary
    
    
    @staticmethod
    def EncodeIntArray(int_array):
        binary = struct.pack('i', len(int_array))  # Pack the length of the array
        for i in int_array:
            binary += struct.pack('i', i)  # Pack each integer
        return binary
    
    @staticmethod
    def DecodeIntArray(binary):
        if (len(binary) < 4): # there should at least be 4 bytes for the length
            return []
        length = struct.unpack('i', binary[:4])[0]
        if (len(binary) < 4 + length * 4): # content length should be 4 + length * 4
            return []
        return struct.unpack('i'*length, binary[4:])
    

    @staticmethod
    def EncodeBoolArray(bool_array):
        binary = struct.pack('i', len(bool_array))  # Pack the length of the array
        for b in bool_array:
            binary += struct.pack('?', b)  # Pack each boolean
        return binary
    
    @staticmethod
    def DecodeBoolArray(binary):
        if (len(binary) < 4):
            return []
        length = struct.unpack('i', binary[:4])[0]
        if (len(binary) < 4 + length): # content length should be 4 + length
            return []
        return struct.unpack('?'*length, binary[4:])

    @staticmethod
    def EncodeDoubleArray(double_array):
        binary = struct.pack('i', len(double_array))  # Pack the length of the array
        for d in double_array:
            binary += struct.pack('d', d)  # Pack each double
        return binary
    
    @staticmethod
    def DecodeDoubleArray(binary):
        if (len(binary) < 4):
            return []
        length = struct.unpack('i', binary[:4])[0]
        if (len(binary) < 4 + length * 8): # content length should be 4 + length * 8
            return []
        return struct.unpack('d'*length, binary[4:])

    @staticmethod
    def EncodeByteArray(byte_array):
        binary = struct.pack('i', len(byte_array))  # Pack the length of the array
        for b in byte_array:
            binary += struct.pack('b', b)  # Pack each byte
        return binary
    
    @staticmethod
    def DecodeByteArray(binary):
        if (len(binary) < 4):
            return []
        length = struct.unpack('i', binary[:4])[0]
        if (len(binary) < 4 + length): # content length should be 4 + length
            return []
        return struct.unpack('b'*length, binary[4:])

    @staticmethod
    def EncodeStringArray(string_array):
        binary = struct.pack('i', len(string_array))  # Pack the length of the array
        for s in string_array:
            binary += SDK_Helper.EncodeString(s)  # Use EncodeString for each string
        return binary
    
    @staticmethod
    def DecodeStringArray(binary):
        if (len(binary) < 4):
            return []
        length = struct.unpack('i', binary[:4])[0]
        strings = []
        start = 4
        for i in range(length):
            string_length = struct.unpack('i', binary[start:start+4])[0]
            start += 4
            strings.append(binary[start:start+string_length].decode('utf-8'))
            start += string_length
        return strings
    

class SDK:
    @staticmethod
    def ActivateEllipseApertureSelectTool(aperture_size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(aperture_size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateEllipseApertureSelectTool')
        
        if response.status_code == 200:
            print(f"ActivateEllipseApertureSelectTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateEllipseSelectTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateEllipseSelectTool')
        
        if response.status_code == 200:
            print(f"ActivateEllipseSelectTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateEraserTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateEraserTool')
        
        if response.status_code == 200:
            print(f"ActivateEraserTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateLassoSelectTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateLassoSelectTool')
        
        if response.status_code == 200:
            print(f"ActivateLassoSelectTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateLineSelectTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateLineSelectTool')
        
        if response.status_code == 200:
            print(f"ActivateLineSelectTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateMagicWandTool(threshold_min, threshold_max):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(threshold_min)
        binary_payload += SDK_Helper.EncodeFloat(threshold_max)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateMagicWandTool')
        
        if response.status_code == 200:
            print(f"ActivateMagicWandTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateMoveAoiTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateMoveAoiTool')
        
        if response.status_code == 200:
            print(f"ActivateMoveAoiTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateMoveTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateMoveTool')
        
        if response.status_code == 200:
            print(f"ActivateMoveTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivatePanTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivatePanTool')
        
        if response.status_code == 200:
            print(f"ActivatePanTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivatePencilTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivatePencilTool')
        
        if response.status_code == 200:
            print(f"ActivatePencilTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivatePolygonSelectTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivatePolygonSelectTool')
        
        if response.status_code == 200:
            print(f"ActivatePolygonSelectTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateRectangleApertureSelectTool(apSize):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(apSize)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateRectangleApertureSelectTool')
        
        if response.status_code == 200:
            print(f"ActivateRectangleApertureSelectTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateRectangleSelectTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateRectangleSelectTool')
        
        if response.status_code == 200:
            print(f"ActivateRectangleSelectTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateRectangleTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateRectangleTool')
        
        if response.status_code == 200:
            print(f"ActivateRectangleTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateTextTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateTextTool')
        
        if response.status_code == 200:
            print(f"ActivateTextTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateTool(tool_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(tool_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateTool')
        
        if response.status_code == 200:
            print(f"ActivateTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ActivateZoomTool():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ActivateZoomTool')
        
        if response.status_code == 200:
            print(f"ActivateZoomTool: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiFromAoi(new_name, action, source_AOI_name, action_parameter):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(action)
        binary_payload += SDK_Helper.EncodeString(source_AOI_name)
        binary_payload += SDK_Helper.EncodeString(action_parameter)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiFromAoi')
        
        if response.status_code == 200:
            print(f"AddAoiFromAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiFromDataTable(data_table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiFromDataTable')
        
        if response.status_code == 200:
            print(f"AddAoiFromDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiFromFile(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiFromFile')
        
        if response.status_code == 200:
            print(f"AddAoiFromFile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiFromMagicWand(new_name, x, y, measurement_name, threshold_min, threshold_max):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeInt(x)
        binary_payload += SDK_Helper.EncodeInt(y)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeFloat(threshold_min)
        binary_payload += SDK_Helper.EncodeFloat(threshold_max)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiFromMagicWand')
        
        if response.status_code == 200:
            print(f"AddAoiFromMagicWand: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiFromMask(new_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiFromMask')
        
        if response.status_code == 200:
            print(f"AddAoiFromMask: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiFromPolygon(new_name, point_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeFloatArray(point_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiFromPolygon')
        
        if response.status_code == 200:
            print(f"AddAoiFromPolygon: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiFromSelection(new_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiFromSelection')
        
        if response.status_code == 200:
            print(f"AddAoiFromSelection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiFromShape(new_name, shape, x, y, width, height):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(shape)
        binary_payload += SDK_Helper.EncodeInt(x)
        binary_payload += SDK_Helper.EncodeInt(y)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiFromShape')
        
        if response.status_code == 200:
            print(f"AddAoiFromShape: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiInPolar(name, shape, theta, phi, size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(name)
        binary_payload += SDK_Helper.EncodeString(shape)
        binary_payload += SDK_Helper.EncodeFloat(theta)
        binary_payload += SDK_Helper.EncodeFloat(phi)
        binary_payload += SDK_Helper.EncodeFloat(size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiInPolar')
        
        if response.status_code == 200:
            print(f"AddAoiInPolar: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiMetaField(name, type):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(name)
        binary_payload += SDK_Helper.EncodeString(type)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiMetaField')
        
        if response.status_code == 200:
            print(f"AddAoiMetaField: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoisInGrid(shape, size, size_units, rows, columns, top, bottom, left, right, slope, prefix):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(shape)
        binary_payload += SDK_Helper.EncodeString(size)
        binary_payload += SDK_Helper.EncodeString(size_units)
        binary_payload += SDK_Helper.EncodeInt(rows)
        binary_payload += SDK_Helper.EncodeInt(columns)
        binary_payload += SDK_Helper.EncodeInt(top)
        binary_payload += SDK_Helper.EncodeInt(bottom)
        binary_payload += SDK_Helper.EncodeInt(left)
        binary_payload += SDK_Helper.EncodeInt(right)
        binary_payload += SDK_Helper.EncodeFloat(slope)
        binary_payload += SDK_Helper.EncodeString(prefix)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoisInGrid')
        
        if response.status_code == 200:
            print(f"AddAoisInGrid: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoisInPolar(theta_start, theta_step, theta_end, phi_start, phi_step, phi_end, size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(theta_start)
        binary_payload += SDK_Helper.EncodeFloat(theta_step)
        binary_payload += SDK_Helper.EncodeFloat(theta_end)
        binary_payload += SDK_Helper.EncodeFloat(phi_start)
        binary_payload += SDK_Helper.EncodeFloat(phi_step)
        binary_payload += SDK_Helper.EncodeFloat(phi_end)
        binary_payload += SDK_Helper.EncodeFloat(size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoisInPolar')
        
        if response.status_code == 200:
            print(f"AddAoisInPolar: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiTableColumn(new_name, formula, type, heading, width, visible):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(formula)
        binary_payload += SDK_Helper.EncodeString(type)
        binary_payload += SDK_Helper.EncodeString(heading)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(visible)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiTableColumn')
        
        if response.status_code == 200:
            print(f"AddAoiTableColumn: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiTableScheme(new_name, active_scheme, visible_column_names):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeBool(active_scheme)
        binary_payload += SDK_Helper.EncodeString(visible_column_names)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiTableScheme')
        
        if response.status_code == 200:
            print(f"AddAoiTableScheme: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddAoiToMask(AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddAoiToMask')
        
        if response.status_code == 200:
            print(f"AddAoiToMask: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddCapture(new_name, lens_ID, fov_ID, iris_ID, overlap, nd, min, max, use_min, use_max, averaging_count, scalar, measurement_name, data_type_name, replace, presentation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeInt(lens_ID)
        binary_payload += SDK_Helper.EncodeInt(fov_ID)
        binary_payload += SDK_Helper.EncodeInt(iris_ID)
        binary_payload += SDK_Helper.EncodeInt(overlap)
        binary_payload += SDK_Helper.EncodeInt(nd)
        binary_payload += SDK_Helper.EncodeFloat(min)
        binary_payload += SDK_Helper.EncodeFloat(max)
        binary_payload += SDK_Helper.EncodeBool(use_min)
        binary_payload += SDK_Helper.EncodeBool(use_max)
        binary_payload += SDK_Helper.EncodeInt(averaging_count)
        binary_payload += SDK_Helper.EncodeFloat(scalar)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(data_type_name)
        binary_payload += SDK_Helper.EncodeBool(replace)
        binary_payload += SDK_Helper.EncodeString(presentation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddCapture')
        
        if response.status_code == 200:
            print(f"AddCapture: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddCaptureFromFile(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddCaptureFromFile')
        
        if response.status_code == 200:
            print(f"AddCaptureFromFile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddCaptureFromMeasurement(measurement_name, capture_scheme, exposure_step, show_editor):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(capture_scheme)
        binary_payload += SDK_Helper.EncodeInt(exposure_step)
        binary_payload += SDK_Helper.EncodeBool(show_editor)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddCaptureFromMeasurement')
        
        if response.status_code == 200:
            print(f"AddCaptureFromMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddCaptureScheme(new_name, tab_delimited_parameters):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_parameters)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddCaptureScheme')
        
        if response.status_code == 200:
            print(f"AddCaptureScheme: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddColorCaptureScheme(new_name, iris_ID, mode, bracketing, longest, measurement_name, TSV_components, presentation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeInt(iris_ID)
        binary_payload += SDK_Helper.EncodeString(mode)
        binary_payload += SDK_Helper.EncodeString(bracketing)
        binary_payload += SDK_Helper.EncodeDouble(longest)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(TSV_components)
        binary_payload += SDK_Helper.EncodeString(presentation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddColorCaptureScheme')
        
        if response.status_code == 200:
            print(f"AddColorCaptureScheme: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddColorCorrection(tab_delimited_names):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(tab_delimited_names)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddColorCorrection')
        
        if response.status_code == 200:
            print(f"AddColorCorrection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddColorGroupFiles(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddColorGroupFiles')
        
        if response.status_code == 200:
            print(f"AddColorGroupFiles: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddColorRegionFromEllipse(color_space, new_name, line_style_name, r, g, b, center_x, center_y, major_axis, minor_axis, rotation_degrees):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(color_space)
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(line_style_name)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        binary_payload += SDK_Helper.EncodeFloat(center_x)
        binary_payload += SDK_Helper.EncodeFloat(center_y)
        binary_payload += SDK_Helper.EncodeFloat(major_axis)
        binary_payload += SDK_Helper.EncodeFloat(minor_axis)
        binary_payload += SDK_Helper.EncodeFloat(rotation_degrees)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddColorRegionFromEllipse')
        
        if response.status_code == 200:
            print(f"AddColorRegionFromEllipse: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddColorRegionFromPolygon(color_space, new_name, line_style_name, r, g, b, point_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(color_space)
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(line_style_name)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        binary_payload += SDK_Helper.EncodeFloatArray(point_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddColorRegionFromPolygon')
        
        if response.status_code == 200:
            print(f"AddColorRegionFromPolygon: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddColorRegionMacAdam(color_space, new_name, line_style_name, r, g, b, center_x, center_y, step):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(color_space)
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(line_style_name)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        binary_payload += SDK_Helper.EncodeFloat(center_x)
        binary_payload += SDK_Helper.EncodeFloat(center_y)
        binary_payload += SDK_Helper.EncodeFloat(step)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddColorRegionMacAdam')
        
        if response.status_code == 200:
            print(f"AddColorRegionMacAdam: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddColorRegionsToGroup(group_name, file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(group_name)
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddColorRegionsToGroup')
        
        if response.status_code == 200:
            print(f"AddColorRegionsToGroup: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddCompoundFilter(new_name, filter_name_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(filter_name_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddCompoundFilter')
        
        if response.status_code == 200:
            print(f"AddCompoundFilter: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddCompoundPresentation(new_name, presentation_name_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(presentation_name_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddCompoundPresentation')
        
        if response.status_code == 200:
            print(f"AddCompoundPresentation: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddComputation(new_name, formula, measurement_name, presentation_name, data_type_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(formula)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(presentation_name)
        binary_payload += SDK_Helper.EncodeString(data_type_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddComputation')
        
        if response.status_code == 200:
            print(f"AddComputation: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddComputationFromFile(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddComputationFromFile')
        
        if response.status_code == 200:
            print(f"AddComputationFromFile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddCustomFilterRegistrationDataTable(data_table_name, option):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(option)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddCustomFilterRegistrationDataTable')
        
        if response.status_code == 200:
            print(f"AddCustomFilterRegistrationDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddCustomPresentation(new_name, color_list, value_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeIntArray(color_list)
        binary_payload += SDK_Helper.EncodeFloatArray(value_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddCustomPresentation')
        
        if response.status_code == 200:
            print(f"AddCustomPresentation: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddDataTable(new_name, columns, rows, descriptive_text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeInt(columns)
        binary_payload += SDK_Helper.EncodeInt(rows)
        binary_payload += SDK_Helper.EncodeString(descriptive_text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddDataTable')
        
        if response.status_code == 200:
            print(f"AddDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddDataTableFromDictionary(new_name, dictionary_name, options):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(dictionary_name)
        binary_payload += SDK_Helper.EncodeString(options)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddDataTableFromDictionary')
        
        if response.status_code == 200:
            print(f"AddDataTableFromDictionary: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddDataTableFromGraph(new_name, graph_window):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(graph_window)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddDataTableFromGraph')
        
        if response.status_code == 200:
            print(f"AddDataTableFromGraph: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddDataTableFromHistogram(new_name, measurement_name, AOI_name, bin_count, options):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeInt(bin_count)
        binary_payload += SDK_Helper.EncodeString(options)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddDataTableFromHistogram')
        
        if response.status_code == 200:
            print(f"AddDataTableFromHistogram: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddDataTableFromObjectTable(new_name, object_type,  options):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(object_type)
        binary_payload += SDK_Helper.EncodeString(options)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddDataTableFromObjectTable')
        
        if response.status_code == 200:
            print(f"AddDataTableFromObjectTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddDataTableFromSpectrum(new_name, measurement_name, increment):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeFloat(increment)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddDataTableFromSpectrum')
        
        if response.status_code == 200:
            print(f"AddDataTableFromSpectrum: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddDataTableFromSurface(new_name, UDW_name, UDW_control_name, shape, x0, y0, x1, y1, options):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        binary_payload += SDK_Helper.EncodeString(shape)
        binary_payload += SDK_Helper.EncodeInt(x0)
        binary_payload += SDK_Helper.EncodeInt(y0)
        binary_payload += SDK_Helper.EncodeInt(x1)
        binary_payload += SDK_Helper.EncodeInt(y1)
        binary_payload += SDK_Helper.EncodeString(options)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddDataTableFromSurface')
        
        if response.status_code == 200:
            print(f"AddDataTableFromSurface: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddDictionary(new_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddDictionary')
        
        if response.status_code == 200:
            print(f"AddDictionary: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddDictionaryFromDataTable(new_name, data_table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddDictionaryFromDataTable')
        
        if response.status_code == 200:
            print(f"AddDictionaryFromDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddEvaluationEntry(new_name, formula, data_type_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(formula)
        binary_payload += SDK_Helper.EncodeString(data_type_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddEvaluationEntry')
        
        if response.status_code == 200:
            print(f"AddEvaluationEntry: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddEvaluationFromDataTable(data_table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddEvaluationFromDataTable')
        
        if response.status_code == 200:
            print(f"AddEvaluationFromDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddFilter(new_name, shape, width, height, stat_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(shape)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(stat_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddFilter')
        
        if response.status_code == 200:
            print(f"AddFilter: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddFilterFromFile(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddFilterFromFile')
        
        if response.status_code == 200:
            print(f"AddFilterFromFile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddImageFromDataTable(new_name, data_table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddImageFromDataTable')
        
        if response.status_code == 200:
            print(f"AddImageFromDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddImageFromWindow(new_name, window_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(window_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddImageFromWindow')
        
        if response.status_code == 200:
            print(f"AddImageFromWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddInstrumentDataTable(content_type, new_name, parameters):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(content_type)
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(parameters)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddInstrumentDataTable')
        
        if response.status_code == 200:
            print(f"AddInstrumentDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddInstrumentLogDataTable(data_table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddInstrumentLogDataTable')
        
        if response.status_code == 200:
            print(f"AddInstrumentLogDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddIsoline(value, r, g, b, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(value)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddIsoline')
        
        if response.status_code == 200:
            print(f"AddIsoline: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddMeasurement(new_name, presentation_name, types, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(presentation_name)
        binary_payload += SDK_Helper.EncodeString(types)
        binary_payload += SDK_Helper.EncodeFloat(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddMeasurement')
        
        if response.status_code == 200:
            print(f"AddMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddMeasurementFromDataTable(new_name, presentation_name, data_table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(presentation_name)
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddMeasurementFromDataTable')
        
        if response.status_code == 200:
            print(f"AddMeasurementFromDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddMeasurementFromPattern(pattern_name, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(pattern_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddMeasurementFromPattern')
        
        if response.status_code == 200:
            print(f"AddMeasurementFromPattern: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddMeasurementMetaField(new_name, type):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(type)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddMeasurementMetaField')
        
        if response.status_code == 200:
            print(f"AddMeasurementMetaField: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddMetaPlot(new_name, MMF_name, measurement_name, x_log, y_heading, y_formula, y_axis_log, y_axis_normalized, smoothing_factor):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(MMF_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(x_log)
        binary_payload += SDK_Helper.EncodeString(y_heading)
        binary_payload += SDK_Helper.EncodeString(y_formula)
        binary_payload += SDK_Helper.EncodeBool(y_axis_log)
        binary_payload += SDK_Helper.EncodeBool(y_axis_normalized)
        binary_payload += SDK_Helper.EncodeInt(smoothing_factor)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddMetaPlot')
        
        if response.status_code == 200:
            print(f"AddMetaPlot: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddObjectFromFile(object_type, file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type)
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddObjectFromFile')
        
        if response.status_code == 200:
            print(f"AddObjectFromFile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddPattern(new_name, content, comments):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(content)
        binary_payload += SDK_Helper.EncodeString(comments)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddPattern')
        
        if response.status_code == 200:
            print(f"AddPattern: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddPresentation(new_name, bin_count, palette_type, color_list, range_source, min, max, mapping_type):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeInt(bin_count)
        binary_payload += SDK_Helper.EncodeString(palette_type)
        binary_payload += SDK_Helper.EncodeInt(color_list)
        binary_payload += SDK_Helper.EncodeString(range_source)
        binary_payload += SDK_Helper.EncodeFloat(min)
        binary_payload += SDK_Helper.EncodeFloat(max)
        binary_payload += SDK_Helper.EncodeString(mapping_type)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddPresentation')
        
        if response.status_code == 200:
            print(f"AddPresentation: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddPresentationFromFile(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddPresentationFromFile')
        
        if response.status_code == 200:
            print(f"AddPresentationFromFile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddProfile(new_name, x0, y0, x1, y1):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeInt(x0)
        binary_payload += SDK_Helper.EncodeInt(y0)
        binary_payload += SDK_Helper.EncodeInt(x1)
        binary_payload += SDK_Helper.EncodeInt(y1)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddProfile')
        
        if response.status_code == 200:
            print(f"AddProfile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddProfileFromSelection(new_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddProfileFromSelection')
        
        if response.status_code == 200:
            print(f"AddProfileFromSelection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddProfileInPolar(new_name, theta0, phi0, theta1, phi1):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeFloat(theta0)
        binary_payload += SDK_Helper.EncodeFloat(phi0)
        binary_payload += SDK_Helper.EncodeFloat(theta1)
        binary_payload += SDK_Helper.EncodeFloat(phi1)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddProfileInPolar')
        
        if response.status_code == 200:
            print(f"AddProfileInPolar: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddProfilePlotScheme(new_name, active_scheme, smoothing, y_axis_logarithmic, full_width_percent_max, polar_plot_mode):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeBool(active_scheme)
        binary_payload += SDK_Helper.EncodeBool(smoothing)
        binary_payload += SDK_Helper.EncodeBool(y_axis_logarithmic)
        binary_payload += SDK_Helper.EncodeBool(full_width_percent_max)
        binary_payload += SDK_Helper.EncodeBool(polar_plot_mode)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddProfilePlotScheme')
        
        if response.status_code == 200:
            print(f"AddProfilePlotScheme: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddRefinementScheme(name, doMinThreshold, doMaxThreshold, minThreshold, maxThreshold, erosion, minArea, combine):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(name)
        binary_payload += SDK_Helper.EncodeBool(doMinThreshold)
        binary_payload += SDK_Helper.EncodeBool(doMaxThreshold)
        binary_payload += SDK_Helper.EncodeFloat(minThreshold)
        binary_payload += SDK_Helper.EncodeFloat(maxThreshold)
        binary_payload += SDK_Helper.EncodeInt(erosion)
        binary_payload += SDK_Helper.EncodeInt(minArea)
        binary_payload += SDK_Helper.EncodeBool(combine)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddRefinementScheme')
        
        if response.status_code == 200:
            print(f"AddRefinementScheme: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReport(new_name, header_text, font_size, image, img_size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(header_text)
        binary_payload += SDK_Helper.EncodeInt(font_size)
        binary_payload += SDK_Helper.EncodeString(image)
        binary_payload += SDK_Helper.EncodeInt(img_size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReport')
        
        if response.status_code == 200:
            print(f"AddReport: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportAoiTable(report_name, width, horizontal_stacking, font_size, swap_rows_columns):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(font_size)
        binary_payload += SDK_Helper.EncodeBool(swap_rows_columns)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportAoiTable')
        
        if response.status_code == 200:
            print(f"AddReportAoiTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportCiePlot(report_name, width, horizontal_stacking, height, scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportCiePlot')
        
        if response.status_code == 200:
            print(f"AddReportCiePlot: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportDataTable(report_name, width, horizontal_stacking, font_size, data_table_name, columns, rows, parameters):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(font_size)
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(columns)
        binary_payload += SDK_Helper.EncodeString(rows)
        binary_payload += SDK_Helper.EncodeString(parameters)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportDataTable')
        
        if response.status_code == 200:
            print(f"AddReportDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportDataTableGraph(report_name, width, horizontal_stacking, height, data_table_name, xtext, ytext, parameters):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(xtext)
        binary_payload += SDK_Helper.EncodeString(ytext)
        binary_payload += SDK_Helper.EncodeString(parameters)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportDataTableGraph')
        
        if response.status_code == 200:
            print(f"AddReportDataTableGraph: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportDivider(report_name, width, horizontal_stacking, height):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportDivider')
        
        if response.status_code == 200:
            print(f"AddReportDivider: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportDocumentText(report_name, width, horizontal_stacking, font_size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(font_size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportDocumentText')
        
        if response.status_code == 200:
            print(f"AddReportDocumentText: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportEvaluationsTable(report_name, width, horizontal_stacking, font_size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(font_size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportEvaluationsTable')
        
        if response.status_code == 200:
            print(f"AddReportEvaluationsTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportFileName(report_name, width, horizontal_stacking, font_size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(font_size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportFileName')
        
        if response.status_code == 200:
            print(f"AddReportFileName: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportIsolinesLegend(report_name, width, horizontal_stacking, height, meas):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(meas)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportIsolinesLegend')
        
        if response.status_code == 200:
            print(f"AddReportIsolinesLegend: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportMeasurement(report_name, width, horizontal_stacking, height, measurement_name, show_isolines, show_AOIs, show_AOI_highlighting, show_AOI_labels, show_annotation):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(show_isolines)
        binary_payload += SDK_Helper.EncodeBool(show_AOIs)
        binary_payload += SDK_Helper.EncodeBool(show_AOI_highlighting)
        binary_payload += SDK_Helper.EncodeBool(show_AOI_labels)
        binary_payload += SDK_Helper.EncodeBool(show_annotation)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportMeasurement')
        
        if response.status_code == 200:
            print(f"AddReportMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportMeasurementHistogram(report_name, width, horizontal_stacking, height, measurement_name, xlog, ylog, hzoom):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(xlog)
        binary_payload += SDK_Helper.EncodeBool(ylog)
        binary_payload += SDK_Helper.EncodeBool(hzoom)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportMeasurementHistogram')
        
        if response.status_code == 200:
            print(f"AddReportMeasurementHistogram: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportMeasurementInThetaHV(report_name, width, stack, height, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(stack)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportMeasurementInThetaHV')
        
        if response.status_code == 200:
            print(f"AddReportMeasurementInThetaHV: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportMeasurementSurfacePlot(report_name, width, horizontal_stacking, height, measurement_name, AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportMeasurementSurfacePlot')
        
        if response.status_code == 200:
            print(f"AddReportMeasurementSurfacePlot: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportMeasurementThermometer(report_name, width, horizontal_stacking, height, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportMeasurementThermometer')
        
        if response.status_code == 200:
            print(f"AddReportMeasurementThermometer: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportMetaInfoTable(report_name, width, horizontal_stacking, font_size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(font_size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportMetaInfoTable')
        
        if response.status_code == 200:
            print(f"AddReportMetaInfoTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportMetaPlot(report_name, width, horizontal_stacking, height, meta_plot_scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(meta_plot_scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportMetaPlot')
        
        if response.status_code == 200:
            print(f"AddReportMetaPlot: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportMetaPlotLegend(report_name, width, horizontal_stacking, height):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportMetaPlotLegend')
        
        if response.status_code == 200:
            print(f"AddReportMetaPlotLegend: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportPageBreak(report_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportPageBreak')
        
        if response.status_code == 200:
            print(f"AddReportPageBreak: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportProfileLegend(report_name, width, horizontal_stacking, height):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportProfileLegend')
        
        if response.status_code == 200:
            print(f"AddReportProfileLegend: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportProfilePlot(report_name, width, horizontal_stacking, height, profile, y_axis_is_log, filtering):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(profile)
        binary_payload += SDK_Helper.EncodeBool(y_axis_is_log)
        binary_payload += SDK_Helper.EncodeInt(filtering)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportProfilePlot')
        
        if response.status_code == 200:
            print(f"AddReportProfilePlot: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportProfilePolarPlot(report_name, width, horizontal_stacking, height, profile_name, y_axis_log, smoothing_factor):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(profile_name)
        binary_payload += SDK_Helper.EncodeBool(y_axis_log)
        binary_payload += SDK_Helper.EncodeInt(smoothing_factor)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportProfilePolarPlot')
        
        if response.status_code == 200:
            print(f"AddReportProfilePolarPlot: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportStaticImage(report_name, width, horizontal_stacking, height, image_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(image_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportStaticImage')
        
        if response.status_code == 200:
            print(f"AddReportStaticImage: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportStaticText(report_name, width, horizontal_stacking, font_size, text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(font_size)
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportStaticText')
        
        if response.status_code == 200:
            print(f"AddReportStaticText: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddReportWorkingFolder(report_name, width, horizontal_stacking, font_size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeBool(horizontal_stacking)
        binary_payload += SDK_Helper.EncodeInt(font_size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddReportWorkingFolder')
        
        if response.status_code == 200:
            print(f"AddReportWorkingFolder: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddScript(new_name, script_text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(script_text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddScript')
        
        if response.status_code == 200:
            print(f"AddScript: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddScriptFromFile(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddScriptFromFile')
        
        if response.status_code == 200:
            print(f"AddScriptFromFile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddSelectionToMask():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddSelectionToMask')
        
        if response.status_code == 200:
            print(f"AddSelectionToMask: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddToSelection(shape_name, x, y, width, height):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(shape_name)
        binary_payload += SDK_Helper.EncodeInt(x)
        binary_payload += SDK_Helper.EncodeInt(y)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddToSelection')
        
        if response.status_code == 200:
            print(f"AddToSelection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddUdwControl(UDW_name, UDW_control_name, new_name, text, image, script, width, height, position_keyword, parent_UDW_control_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeString(text)
        binary_payload += SDK_Helper.EncodeString(image)
        binary_payload += SDK_Helper.EncodeString(script)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(position_keyword)
        binary_payload += SDK_Helper.EncodeString(parent_UDW_control_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddUdwControl')
        
        if response.status_code == 200:
            print(f"AddUdwControl: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddUserDefinedDataType(formula_text, unit_suffix, description, options):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(formula_text)
        binary_payload += SDK_Helper.EncodeString(unit_suffix)
        binary_payload += SDK_Helper.EncodeString(description)
        binary_payload += SDK_Helper.EncodeString(options)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddUserDefinedDataType')
        
        if response.status_code == 200:
            print(f"AddUserDefinedDataType: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AddVectorAoiPolygon(new_name, point_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(new_name)
        binary_payload += SDK_Helper.EncodeFloatArray(point_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AddVectorAoiPolygon')
        
        if response.status_code == 200:
            print(f"AddVectorAoiPolygon: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AnnoClear(top_left_x, top_left_y, width, height):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(top_left_x)
        binary_payload += SDK_Helper.EncodeInt(top_left_y)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AnnoClear')
        
        if response.status_code == 200:
            print(f"AnnoClear: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AnnoDrawEllipse(center_x, center_y, x_axis, y_axis, thickness, r, g, b):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(center_x)
        binary_payload += SDK_Helper.EncodeInt(center_y)
        binary_payload += SDK_Helper.EncodeInt(x_axis)
        binary_payload += SDK_Helper.EncodeInt(y_axis)
        binary_payload += SDK_Helper.EncodeInt(thickness)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AnnoDrawEllipse')
        
        if response.status_code == 200:
            print(f"AnnoDrawEllipse: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AnnoDrawImage(image_name, top_left_x, top_left_y, draw_under):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(image_name)
        binary_payload += SDK_Helper.EncodeInt(top_left_x)
        binary_payload += SDK_Helper.EncodeString(top_left_y)
        binary_payload += SDK_Helper.EncodeBool(draw_under)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AnnoDrawImage')
        
        if response.status_code == 200:
            print(f"AnnoDrawImage: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AnnoDrawLine(start_x, start_y, end_x, end_y, thickness, r, g, b):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(start_x)
        binary_payload += SDK_Helper.EncodeInt(start_y)
        binary_payload += SDK_Helper.EncodeInt(end_x)
        binary_payload += SDK_Helper.EncodeInt(end_y)
        binary_payload += SDK_Helper.EncodeInt(thickness)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AnnoDrawLine')
        
        if response.status_code == 200:
            print(f"AnnoDrawLine: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AnnoDrawRectangle(top_left_x, top_left_y, width, height, thickness, r, g, b):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(top_left_x)
        binary_payload += SDK_Helper.EncodeInt(top_left_y)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeInt(thickness)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AnnoDrawRectangle')
        
        if response.status_code == 200:
            print(f"AnnoDrawRectangle: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AnnoDrawText(text, top_left_x, top_left_y, font_size, r, g, b, options):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(text)
        binary_payload += SDK_Helper.EncodeInt(top_left_x)
        binary_payload += SDK_Helper.EncodeInt(top_left_y)
        binary_payload += SDK_Helper.EncodeFloat(font_size)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        binary_payload += SDK_Helper.EncodeBool(options)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AnnoDrawText')
        
        if response.status_code == 200:
            print(f"AnnoDrawText: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AnnoSaveImage(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AnnoSaveImage')
        
        if response.status_code == 200:
            print(f"AnnoSaveImage: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AnnoSaveImageAs(dialog_title):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(dialog_title)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AnnoSaveImageAs')
        
        if response.status_code == 200:
            print(f"AnnoSaveImageAs: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AnnoSetVisible(visible):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(visible)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AnnoSetVisible')
        
        if response.status_code == 200:
            print(f"AnnoSetVisible: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AoiExists(AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AoiExists')
        
        if response.status_code == 200:
            print(f"AoiExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AppendSelectionToInstrumentMask():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AppendSelectionToInstrumentMask')
        
        if response.status_code == 200:
            print(f"AppendSelectionToInstrumentMask: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ApplyHighlightToAoi(highlight_scheme_name, AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(highlight_scheme_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ApplyHighlightToAoi')
        
        if response.status_code == 200:
            print(f"ApplyHighlightToAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ApplyMetaValueToAoi(amf, value, aoi):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(amf)
        binary_payload += SDK_Helper.EncodeString(value)
        binary_payload += SDK_Helper.EncodeString(aoi)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ApplyMetaValueToAoi')
        
        if response.status_code == 200:
            print(f"ApplyMetaValueToAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ApplyRefinementToAoi(measurement_name, refinement_name, AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(refinement_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ApplyRefinementToAoi')
        
        if response.status_code == 200:
            print(f"ApplyRefinementToAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ApplyToDataTableRange(data_table_name, start_column, end_column, start_row, end_row, action, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeInt(start_column)
        binary_payload += SDK_Helper.EncodeInt(end_column)
        binary_payload += SDK_Helper.EncodeInt(start_row)
        binary_payload += SDK_Helper.EncodeInt(end_row)
        binary_payload += SDK_Helper.EncodeString(action)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ApplyToDataTableRange')
        
        if response.status_code == 200:
            print(f"ApplyToDataTableRange: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ApplyToUdwTable(udw, table, action, params):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(udw)
        binary_payload += SDK_Helper.EncodeString(table)
        binary_payload += SDK_Helper.EncodeString(action)
        binary_payload += SDK_Helper.EncodeString(params)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ApplyToUdwTable')
        
        if response.status_code == 200:
            print(f"ApplyToUdwTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ApplyUdwChanges(UDW_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ApplyUdwChanges')
        
        if response.status_code == 200:
            print(f"ApplyUdwChanges: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AppropriatePackageContents(package, objecttype):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(package)
        binary_payload += SDK_Helper.EncodeString(objecttype)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AppropriatePackageContents')
        
        if response.status_code == 200:
            print(f"AppropriatePackageContents: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def Ask(text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'Ask')
        
        if response.status_code == 200:
            print(f"Ask: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AskCustomQuestion(text, popup_ID):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(text)
        binary_payload += SDK_Helper.EncodeInt(popup_ID)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AskCustomQuestion')
        
        if response.status_code == 200:
            print(f"AskCustomQuestion: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AskForFile(dialog_title, initial_folder_path, initial_file_name, filespec_pattern, must_exist, multiple):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(dialog_title)
        binary_payload += SDK_Helper.EncodeString(initial_folder_path)
        binary_payload += SDK_Helper.EncodeString(initial_file_name)
        binary_payload += SDK_Helper.EncodeString(filespec_pattern)
        binary_payload += SDK_Helper.EncodeBool(must_exist)
        binary_payload += SDK_Helper.EncodeBool(multiple)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AskForFile')
        
        if response.status_code == 200:
            print(f"AskForFile: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AskForFolder(caption, initial_folder_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(caption)
        binary_payload += SDK_Helper.EncodeString(initial_folder_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AskForFolder')
        
        if response.status_code == 200:
            print(f"AskForFolder: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def AssignNVISWeightingTable(tableName):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(tableName)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'AssignNVISWeightingTable')
        
        if response.status_code == 200:
            print(f"AssignNVISWeightingTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def BatchCapture(capture_scheme_name_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(capture_scheme_name_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'BatchCapture')
        
        if response.status_code == 200:
            print(f"BatchCapture: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def Calculate(formula, AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(formula)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'Calculate')
        
        if response.status_code == 200:
            print(f"Calculate: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CalculateCustomAoiStat(AOI_name, formula, stat_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeString(formula)
        binary_payload += SDK_Helper.EncodeString(stat_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CalculateCustomAoiStat')
        
        if response.status_code == 200:
            print(f"CalculateCustomAoiStat: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CalculateLineLength(start_x, start_y, end_x, end_y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(start_x)
        binary_payload += SDK_Helper.EncodeDouble(start_y)
        binary_payload += SDK_Helper.EncodeDouble(end_x)
        binary_payload += SDK_Helper.EncodeDouble(end_y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CalculateLineLength')
        
        if response.status_code == 200:
            print(f"CalculateLineLength: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CalculateSpectrumProperty(datatable_name, property):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(datatable_name)
        binary_payload += SDK_Helper.EncodeString(property)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CalculateSpectrumProperty')
        
        if response.status_code == 200:
            print(f"CalculateSpectrumProperty: Success")

            # Decode the first double (8 bytes)
            value1 = SDK_Helper.DecodeDouble(response.content[:8])

            # Decode the second double (next 8 bytes)
            value2 = SDK_Helper.DecodeDouble(response.content[8:16])
            return (value1, value2)

        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CalculateTristimulusProperty(X, Y, Z, property):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(X)
        binary_payload += SDK_Helper.EncodeDouble(Y)
        binary_payload += SDK_Helper.EncodeDouble(Z)
        binary_payload += SDK_Helper.EncodeString(property)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CalculateTristimulusProperty')
        
        if response.status_code == 200:
            print(f"CalculateTristimulusProperty: Success")

            # Decode the first double (8 bytes)
            value1 = SDK_Helper.DecodeDouble(response.content[:8])

            # Decode the second double (next 8 bytes)
            value2 = SDK_Helper.DecodeDouble(response.content[8:16])

            return (value1, value2)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CallDllDataTableIo(DLL_handle, method_name, data_table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(DLL_handle)
        binary_payload += SDK_Helper.EncodeString(method_name)
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CallDllDataTableIo')
        
        if response.status_code == 200:
            print(f"CallDllDataTableIo: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CallDllIntStr(DLL_handle, method_name, parameter):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(DLL_handle)
        binary_payload += SDK_Helper.EncodeString(method_name)
        binary_payload += SDK_Helper.EncodeString(parameter)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CallDllIntStr')
        
        if response.status_code == 200:
            print(f"CallDllIntStr: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CallDllMeasurementDataIo(DLL_handle, method_name, measurement_component):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(DLL_handle)
        binary_payload += SDK_Helper.EncodeString(method_name)
        binary_payload += SDK_Helper.EncodeString(measurement_component)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CallDllMeasurementDataIo')
        
        if response.status_code == 200:
            print(f"CallDllMeasurementDataIo: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CallDllStrStr(DLL_handle, method_name, parameter, buffer_size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(DLL_handle)
        binary_payload += SDK_Helper.EncodeString(method_name)
        binary_payload += SDK_Helper.EncodeString(parameter)
        binary_payload += SDK_Helper.EncodeInt(buffer_size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CallDllStrStr')
        
        if response.status_code == 200:
            print(f"CallDllStrStr: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CancelAllBackgroundTasks():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CancelAllBackgroundTasks')
        
        if response.status_code == 200:
            print(f"CancelAllBackgroundTasks: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CancelBackgroundTask(global_var_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(global_var_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CancelBackgroundTask')
        
        if response.status_code == 200:
            print(f"CancelBackgroundTask: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def Capture(capture_scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(capture_scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'Capture')
        
        if response.status_code == 200:
            print(f"Capture: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CaptureDarkCurrent():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CaptureDarkCurrent')
        
        if response.status_code == 200:
            print(f"CaptureDarkCurrent: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CaptureDarkCurrentAveraged(averaging_count, spectrometer_averaging_count):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(averaging_count)
        binary_payload += SDK_Helper.EncodeInt(spectrometer_averaging_count)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CaptureDarkCurrentAveraged')
        
        if response.status_code == 200:
            print(f"CaptureDarkCurrentAveraged: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CaptureExists(capture_scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(capture_scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CaptureExists')
        
        if response.status_code == 200:
            print(f"CaptureExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CaptureFfc(lens_ID, FoV_ID, iris_ID, exposure_time, averaging_count, filter_wheel_index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(lens_ID)
        binary_payload += SDK_Helper.EncodeInt(FoV_ID)
        binary_payload += SDK_Helper.EncodeInt(iris_ID)
        binary_payload += SDK_Helper.EncodeInt(exposure_time)
        binary_payload += SDK_Helper.EncodeInt(averaging_count)
        binary_payload += SDK_Helper.EncodeInt(filter_wheel_index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CaptureFfc')
        
        if response.status_code == 200:
            print(f"CaptureFfc: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CaptureSpectrumToDataTable(dtName, gvPercentName, gvStatusName, scriptOnEnd, irisIdentifierCode, autoExpo, exposureInMs, averaging, autoMinSignalLevel, densityFilterPosition, specIndex):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(dtName)
        binary_payload += SDK_Helper.EncodeString(gvPercentName)
        binary_payload += SDK_Helper.EncodeString(gvStatusName)
        binary_payload += SDK_Helper.EncodeString(scriptOnEnd)
        binary_payload += SDK_Helper.EncodeInt(irisIdentifierCode)
        binary_payload += SDK_Helper.EncodeBool(autoExpo)
        binary_payload += SDK_Helper.EncodeDouble(exposureInMs)
        binary_payload += SDK_Helper.EncodeInt(averaging)
        binary_payload += SDK_Helper.EncodeDouble(autoMinSignalLevel)
        binary_payload += SDK_Helper.EncodeInt(densityFilterPosition)
        binary_payload += SDK_Helper.EncodeInt(specIndex)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CaptureSpectrumToDataTable')
        
        if response.status_code == 200:
            print(f"CaptureSpectrumToDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ChangeLensConfig(lens_configuration_name, action, param):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(lens_configuration_name)
        binary_payload += SDK_Helper.EncodeString(action)
        binary_payload += SDK_Helper.EncodeString(param)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ChangeLensConfig')
        
        if response.status_code == 200:
            print(f"ChangeLensConfig: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ChangeMaskWithShape(shape_name, x, y, width, height, add_shape, clear_first):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(shape_name)
        binary_payload += SDK_Helper.EncodeInt(x)
        binary_payload += SDK_Helper.EncodeInt(y)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeBool(add_shape)
        binary_payload += SDK_Helper.EncodeBool(clear_first)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ChangeMaskWithShape')
        
        if response.status_code == 200:
            print(f"ChangeMaskWithShape: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ChangeMeasurementComponents(measurement_name, tab_delimited_component_names):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_component_names)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ChangeMeasurementComponents')
        
        if response.status_code == 200:
            print(f"ChangeMeasurementComponents: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ClearDictionary(dictionary_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(dictionary_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ClearDictionary')
        
        if response.status_code == 200:
            print(f"ClearDictionary: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ClearMask():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ClearMask')
        
        if response.status_code == 200:
            print(f"ClearMask: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ClearSelection():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ClearSelection')
        
        if response.status_code == 200:
            print(f"ClearSelection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ClipAois(clipping_AOI_name, AOI_list, min_area):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(clipping_AOI_name)
        binary_payload += SDK_Helper.EncodeString(AOI_list)
        binary_payload += SDK_Helper.EncodeInt(min_area)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ClipAois')
        
        if response.status_code == 200:
            print(f"ClipAois: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ClosePhotometrica(save_dirty_PMM):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(save_dirty_PMM)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ClosePhotometrica')
        
        if response.status_code == 200:
            print(f"ClosePhotometrica: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CloseSerialPort(serial_port_handle):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(serial_port_handle)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CloseSerialPort')
        
        if response.status_code == 200:
            print(f"CloseSerialPort: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ColorCorrectMeasurement(color_correction_name, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(color_correction_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ColorCorrectMeasurement')
        
        if response.status_code == 200:
            print(f"ColorCorrectMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CombineAoi(AOI_name_tab_delimited_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name_tab_delimited_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CombineAoi')
        
        if response.status_code == 200:
            print(f"CombineAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CombinePath(file_path_1, file_path_2):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path_1)
        binary_payload += SDK_Helper.EncodeString(file_path_2)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CombinePath')
        
        if response.status_code == 200:
            print(f"CombinePath: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ComputationExists(computation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(computation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ComputationExists')
        
        if response.status_code == 200:
            print(f"ComputationExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def Compute(computation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(computation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'Compute')
        
        if response.status_code == 200:
            print(f"Compute: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ConvertUnits(number, original_unit_name, new_unit_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(number)
        binary_payload += SDK_Helper.EncodeString(original_unit_name)
        binary_payload += SDK_Helper.EncodeString(new_unit_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ConvertUnits')
        
        if response.status_code == 200:
            print(f"ConvertUnits: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CopyDataTableRange(src_name, start_row, row_count, start_column, col_count, dest_table, dest_start_row, dest_start_col):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(src_name)
        binary_payload += SDK_Helper.EncodeInt(start_row)
        binary_payload += SDK_Helper.EncodeInt(row_count)
        binary_payload += SDK_Helper.EncodeInt(start_column)
        binary_payload += SDK_Helper.EncodeInt(col_count)
        binary_payload += SDK_Helper.EncodeString(dest_table)
        binary_payload += SDK_Helper.EncodeInt(dest_start_row)
        binary_payload += SDK_Helper.EncodeInt(dest_start_col)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CopyDataTableRange')
        
        if response.status_code == 200:
            print(f"CopyDataTableRange: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def Correl(x_list, y_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDoubleArray(x_list)
        binary_payload += SDK_Helper.EncodeDoubleArray(y_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'Correl')
        
        if response.status_code == 200:
            print(f"Correl: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CreateColorGroup(color_group_name, color_space, comments):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(color_group_name)
        binary_payload += SDK_Helper.EncodeString(color_space)
        binary_payload += SDK_Helper.EncodeString(comments)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CreateColorGroup')
        
        if response.status_code == 200:
            print(f"CreateColorGroup: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CropToDut(threshold, exposure_time_microseconds):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(threshold)
        binary_payload += SDK_Helper.EncodeInt(exposure_time_microseconds)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CropToDut')
        
        if response.status_code == 200:
            print(f"CropToDut: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CropToSelection():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CropToSelection')
        
        if response.status_code == 200:
            print(f"CropToSelection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CropToTheta(theta):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(theta)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CropToTheta')
        
        if response.status_code == 200:
            print(f"CropToTheta: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CxToX(cx):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(cx)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CxToX')
        
        if response.status_code == 200:
            print(f"CxToX: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def CyToY(cy):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(cy)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'CyToY')
        
        if response.status_code == 200:
            print(f"CyToY: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteAllAoi():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteAllAoi')
        
        if response.status_code == 200:
            print(f"DeleteAllAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteAllIsolines(measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteAllIsolines')
        
        if response.status_code == 200:
            print(f"DeleteAllIsolines: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteAllObjects(object_type_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteAllObjects')
        
        if response.status_code == 200:
            print(f"DeleteAllObjects: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteAllProfiles():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteAllProfiles')
        
        if response.status_code == 200:
            print(f"DeleteAllProfiles: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteAoi(AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteAoi')
        
        if response.status_code == 200:
            print(f"DeleteAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteCapture(capture_scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(capture_scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteCapture')
        
        if response.status_code == 200:
            print(f"DeleteCapture: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteColorGroups(color_group_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(color_group_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteColorGroups')
        
        if response.status_code == 200:
            print(f"DeleteColorGroups: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteComputation(computation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(computation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteComputation')
        
        if response.status_code == 200:
            print(f"DeleteComputation: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteCustomFilterRegistration(filter_registration_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(filter_registration_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteCustomFilterRegistration')
        
        if response.status_code == 200:
            print(f"DeleteCustomFilterRegistration: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteDictionary(dictionary_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(dictionary_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteDictionary')
        
        if response.status_code == 200:
            print(f"DeleteDictionary: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteFile(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteFile')
        
        if response.status_code == 200:
            print(f"DeleteFile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteHighlightRule(highlight_scheme_name, rule_index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(highlight_scheme_name)
        binary_payload += SDK_Helper.EncodeInt(rule_index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteHighlightRule')
        
        if response.status_code == 200:
            print(f"DeleteHighlightRule: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteHighlightScheme(highlight_scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(highlight_scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteHighlightScheme')
        
        if response.status_code == 200:
            print(f"DeleteHighlightScheme: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteIsoline(value, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(value)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteIsoline')
        
        if response.status_code == 200:
            print(f"DeleteIsoline: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteMeasurement(measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteMeasurement')
        
        if response.status_code == 200:
            print(f"DeleteMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteObject(object_type_name, object_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        binary_payload += SDK_Helper.EncodeString(object_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteObject')
        
        if response.status_code == 200:
            print(f"DeleteObject: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteRefinementScheme(refinement):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(refinement)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteRefinementScheme')
        
        if response.status_code == 200:
            print(f"DeleteRefinementScheme: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteReport(report_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteReport')
        
        if response.status_code == 200:
            print(f"DeleteReport: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DeleteUdwControls(UDW_name, UDW_panel_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_panel_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DeleteUdwControls')
        
        if response.status_code == 200:
            print(f"DeleteUdwControls: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DocumentHeight():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DocumentHeight')
        
        if response.status_code == 200:
            print(f"DocumentHeight: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DocumentWidth():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DocumentWidth')
        
        if response.status_code == 200:
            print(f"DocumentWidth: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DriverTransaction(DLL_name, request, input_dictionary_name, output_dictionary_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(DLL_name)
        binary_payload += SDK_Helper.EncodeString(request)
        binary_payload += SDK_Helper.EncodeString(input_dictionary_name)
        binary_payload += SDK_Helper.EncodeString(output_dictionary_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DriverTransaction')
        
        if response.status_code == 200:
            print(f"DriverTransaction: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DuplicateAoi(source_AOI_name, new_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(source_AOI_name)
        binary_payload += SDK_Helper.EncodeString(new_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DuplicateAoi')
        
        if response.status_code == 200:
            print(f"DuplicateAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DuplicateMeasurement(source_measurement_name, new_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(source_measurement_name)
        binary_payload += SDK_Helper.EncodeString(new_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DuplicateMeasurement')
        
        if response.status_code == 200:
            print(f"DuplicateMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def DuplicatePresentation(source_presentation_name, new_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(source_presentation_name)
        binary_payload += SDK_Helper.EncodeString(new_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'DuplicatePresentation')
        
        if response.status_code == 200:
            print(f"DuplicatePresentation: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def EnsureColorComponent(measurement_name, tab_delimited_type_names):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_type_names)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'EnsureColorComponent')
        
        if response.status_code == 200:
            print(f"EnsureColorComponent: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportAoi(AOI_name, measurement_name, reverse_rows, output_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(reverse_rows)
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportAoi')
        
        if response.status_code == 200:
            print(f"ExportAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportAoiStats(AOI_name, measurement_name, output_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportAoiStats')
        
        if response.status_code == 200:
            print(f"ExportAoiStats: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportAoiTable(output_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportAoiTable')
        
        if response.status_code == 200:
            print(f"ExportAoiTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportCameraProperties():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportCameraProperties')
        
        if response.status_code == 200:
            print(f"ExportCameraProperties: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportDataTable(data_table_name, output_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportDataTable')
        
        if response.status_code == 200:
            print(f"ExportDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportEvaluationsTable(output_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportEvaluationsTable')
        
        if response.status_code == 200:
            print(f"ExportEvaluationsTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportMeasurement(measurement_name, increment, output_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeInt(increment)
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportMeasurement')
        
        if response.status_code == 200:
            print(f"ExportMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportMeasurementBitmap(output_file_path, measurement_name, show_measurement, show_iso, show_AOIs, show_AOI_highlights, show_AOI_labels, show_annotation, bounding_AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(show_measurement)
        binary_payload += SDK_Helper.EncodeBool(show_iso)
        binary_payload += SDK_Helper.EncodeBool(show_AOIs)
        binary_payload += SDK_Helper.EncodeBool(show_AOI_highlights)
        binary_payload += SDK_Helper.EncodeBool(show_AOI_labels)
        binary_payload += SDK_Helper.EncodeBool(show_annotation)
        binary_payload += SDK_Helper.EncodeString(bounding_AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportMeasurementBitmap')
        
        if response.status_code == 200:
            print(f"ExportMeasurementBitmap: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportMeasurementToFile(measurement_name, output_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportMeasurementToFile')
        
        if response.status_code == 200:
            print(f"ExportMeasurementToFile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportObjectTable(object_type_name, output_file_path, TDP_options):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        binary_payload += SDK_Helper.EncodeString(TDP_options)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportObjectTable')
        
        if response.status_code == 200:
            print(f"ExportObjectTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportProfile(profile_name, polar, increment, output_file_path, options):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(profile_name)
        binary_payload += SDK_Helper.EncodeBool(polar)
        binary_payload += SDK_Helper.EncodeFloat(increment)
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        binary_payload += SDK_Helper.EncodeString(options)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportProfile')
        
        if response.status_code == 200:
            print(f"ExportProfile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportSpectrum(measurement_name, increment, output_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeFloat(increment)
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportSpectrum')
        
        if response.status_code == 200:
            print(f"ExportSpectrum: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportSpectrumStats(measurement_name, output_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportSpectrumStats')
        
        if response.status_code == 200:
            print(f"ExportSpectrumStats: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ExportText(output_file_path, text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(output_file_path)
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ExportText')
        
        if response.status_code == 200:
            print(f"ExportText: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FillAoiHoles(AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FillAoiHoles')
        
        if response.status_code == 200:
            print(f"FillAoiHoles: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FillDataTableRange(data_table_name, start_column, end_column, start_row, end_row, column_factor, row_factor, const_factor):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeInt(start_column)
        binary_payload += SDK_Helper.EncodeInt(end_column)
        binary_payload += SDK_Helper.EncodeInt(start_row)
        binary_payload += SDK_Helper.EncodeInt(end_row)
        binary_payload += SDK_Helper.EncodeDouble(column_factor)
        binary_payload += SDK_Helper.EncodeDouble(row_factor)
        binary_payload += SDK_Helper.EncodeDouble(const_factor)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FillDataTableRange')
        
        if response.status_code == 200:
            print(f"FillDataTableRange: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FilterExists(spatial_filter_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(spatial_filter_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FilterExists')
        
        if response.status_code == 200:
            print(f"FilterExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FilterMeasurementAoi(source_measurement_name, new_measurement_name, bounding_AOI_name, spatial_filter_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(source_measurement_name)
        binary_payload += SDK_Helper.EncodeString(new_measurement_name)
        binary_payload += SDK_Helper.EncodeString(bounding_AOI_name)
        binary_payload += SDK_Helper.EncodeString(spatial_filter_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FilterMeasurementAoi')
        
        if response.status_code == 200:
            print(f"FilterMeasurementAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FilterMeasurements(spatial_filter_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(spatial_filter_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FilterMeasurements')
        
        if response.status_code == 200:
            print(f"FilterMeasurements: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FindCell(data_table_name, row, column):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(row)
        binary_payload += SDK_Helper.EncodeString(column)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FindCell')
        
        if response.status_code == 200:
            print(f"FindCell: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FindColumn(data_table_name, text_to_match, row_to_search):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(text_to_match)
        binary_payload += SDK_Helper.EncodeInt(row_to_search)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FindColumn')
        
        if response.status_code == 200:
            print(f"FindColumn: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FindGridAois(object_name, use_datatable):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_name)
        binary_payload += SDK_Helper.EncodeBool(use_datatable)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FindGridAois')
        
        if response.status_code == 200:
            print(f"FindGridAois: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FindIntersectionOfLines(x1, y1, x2, y2, x3, y3, x4, y4):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(x1)
        binary_payload += SDK_Helper.EncodeDouble(y1)
        binary_payload += SDK_Helper.EncodeDouble(x2)
        binary_payload += SDK_Helper.EncodeDouble(y2)
        binary_payload += SDK_Helper.EncodeDouble(x3)
        binary_payload += SDK_Helper.EncodeDouble(y3)
        binary_payload += SDK_Helper.EncodeDouble(x4)
        binary_payload += SDK_Helper.EncodeDouble(y4)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FindIntersectionOfLines')
        
        if response.status_code == 200:
            print(f"FindIntersectionOfLines: Success")

            # Decode the response
            value1 = SDK_Helper.DecodeDouble(response.content[:8])

            value2 = SDK_Helper.DecodeDouble(response.content[8:16])
            return (value1, value2)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FindNearestRow(data_table_name, value, column_to_search):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeDouble(value)
        binary_payload += SDK_Helper.EncodeInt(column_to_search)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FindNearestRow')
        
        if response.status_code == 200:
            print(f"FindNearestRow: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FindPointOnLine(x0, y0, x1, y1, x):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(x0)
        binary_payload += SDK_Helper.EncodeDouble(y0)
        binary_payload += SDK_Helper.EncodeDouble(x1)
        binary_payload += SDK_Helper.EncodeDouble(y1)
        binary_payload += SDK_Helper.EncodeDouble(x)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FindPointOnLine')
        
        if response.status_code == 200:
            print(f"FindPointOnLine: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FindPolygon(measurement_component, threshold, max_edge_angle, min_edge_length, expected_edge_count, start_x, start_y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_component)
        binary_payload += SDK_Helper.EncodeDouble(threshold)
        binary_payload += SDK_Helper.EncodeDouble(max_edge_angle)
        binary_payload += SDK_Helper.EncodeInt(min_edge_length)
        binary_payload += SDK_Helper.EncodeInt(expected_edge_count)
        binary_payload += SDK_Helper.EncodeInt(start_x)
        binary_payload += SDK_Helper.EncodeInt(start_y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FindPolygon')
        
        if response.status_code == 200:
            print(f"FindPolygon: Success")

            # Decode the response

            # Read the size of the pointslist array as an int
            pointslist_size = SDK_Helper.DecodeInt(response.content[:4])

            # The array is written as x1,y1,x2,y2,x3,y3,...,xn,yn (each value is a float)
            pointslist = []
            for i in range(pointslist_size):
                x = SDK_Helper.DecodeFloat(response.content[4 + i * 8: 8 + i * 8])
                y = SDK_Helper.DecodeFloat(response.content[8 + i * 8: 12 + i * 8])
                
                pointslist.append((x, y))
            
            return pointslist
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FindRow(data_table_name, text_to_match, search_column):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(text_to_match)
        binary_payload += SDK_Helper.EncodeInt(search_column)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FindRow')
        
        if response.status_code == 200:
            print(f"FindRow: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FreeDll(DLL_handle):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(DLL_handle)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FreeDll')
        
        if response.status_code == 200:
            print(f"FreeDll: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FtpDownload(FTP_URL, destpath, username, password):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(FTP_URL)
        binary_payload += SDK_Helper.EncodeString(destpath)
        binary_payload += SDK_Helper.EncodeString(username)
        binary_payload += SDK_Helper.EncodeString(password)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FtpDownload')
        
        if response.status_code == 200:
            print(f"FtpDownload: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FtpGetDirectory(FTP_URL, username, password):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(FTP_URL)
        binary_payload += SDK_Helper.EncodeString(username)
        binary_payload += SDK_Helper.EncodeString(password)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FtpGetDirectory')
        
        if response.status_code == 200:
            print(f"FtpGetDirectory: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def FtpUpload(FTP_URL, srcpath, username, password):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(FTP_URL)
        binary_payload += SDK_Helper.EncodeString(srcpath)
        binary_payload += SDK_Helper.EncodeString(username)
        binary_payload += SDK_Helper.EncodeString(password)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'FtpUpload')
        
        if response.status_code == 200:
            print(f"FtpUpload: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result

        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GamutArea(color_space_name, AOI_name, tab_delmited_measurement_names):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(color_space_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeString(tab_delmited_measurement_names)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GamutArea')
        
        if response.status_code == 200:
            print(f"GamutArea: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetActiveInstrument():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetActiveInstrument')
        
        if response.status_code == 200:
            print(f"GetActiveInstrument: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetActiveMeasurement():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetActiveMeasurement')
        
        if response.status_code == 200:
            print(f"GetActiveMeasurement: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiCount(root_AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(root_AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiCount')
        
        if response.status_code == 200:
            print(f"GetAoiCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiCountInColorRegion(color_region_name, measurement_name, AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(color_region_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiCountInColorRegion')
        
        if response.status_code == 200:
            print(f"GetAoiCountInColorRegion: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiData(aoiName, measurement_name, outside_value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(aoiName)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeFloat(outside_value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiData')
        
        if response.status_code == 200:
            print(f"GetAoiData: Success")

            # Decode the response
            result = SDK_Helper.DecodeFloatArray(response.content)

            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiDimensions(AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiDimensions')
        
        if response.status_code == 200:
            print(f"GetAoiDimensions: Success")

            # Decode the response
            result1 = SDK_Helper.DecodeInt(response.content[:4])
            result2 = SDK_Helper.DecodeInt(response.content[4:8])
            return (result1, result2)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiIntersectionStat(AOI_1_name, AOI_2_name, property_name, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_1_name)
        binary_payload += SDK_Helper.EncodeString(AOI_2_name)
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiIntersectionStat')
        
        if response.status_code == 200:
            print(f"GetAoiIntersectionStat: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiName(root_index, child_index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(root_index)
        binary_payload += SDK_Helper.EncodeInt(child_index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiName')
        
        if response.status_code == 200:
            print(f"GetAoiName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiProperty(property_name, AOI_name, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiProperty')
        
        if response.status_code == 200:
            print(f"GetAoiProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeFloat(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiSummaryCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiSummaryCount')
        
        if response.status_code == 200:
            print(f"GetAoiSummaryCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiSummaryName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiSummaryName')
        
        if response.status_code == 200:
            print(f"GetAoiSummaryName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiSummaryProperty(aoi_name, property_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(aoi_name)
        binary_payload += SDK_Helper.EncodeString(property_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiSummaryProperty')
        
        if response.status_code == 200:
            print(f"GetAoiSummaryProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiTableCellValue(AOI_name, column):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeString(column)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiTableCellValue')
        
        if response.status_code == 200:
            print(f"GetAoiTableCellValue: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiTableData(delimter, linefeed):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(delimter)
        binary_payload += SDK_Helper.EncodeString(linefeed)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiTableData')
        
        if response.status_code == 200:
            print(f"GetAoiTableData: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiTableStat(column, stat_name, MMF_name, MMF_value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(column)
        binary_payload += SDK_Helper.EncodeString(stat_name)
        binary_payload += SDK_Helper.EncodeString(MMF_name)
        binary_payload += SDK_Helper.EncodeString(MMF_value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiTableStat')
        
        if response.status_code == 200:
            print(f"GetAoiTableStat: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAoiTextProperty(property_name, AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAoiTextProperty')
        
        if response.status_code == 200:
            print(f"GetAoiTextProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetAutoResponse(popup_ID):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(popup_ID)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetAutoResponse')
        
        if response.status_code == 200:
            print(f"GetAutoResponse: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetCaptureCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetCaptureCount')
        
        if response.status_code == 200:
            print(f"GetCaptureCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetCaptureName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetCaptureName')
        
        if response.status_code == 200:
            print(f"GetCaptureName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetCaptureProperty(property_name, capture_scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(capture_scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetCaptureProperty')
        
        if response.status_code == 200:
            print(f"GetCaptureProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetCaptureSetting(property_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetCaptureSetting')
        
        if response.status_code == 200:
            print(f"GetCaptureSetting: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetCell(data_table_name, row, column):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeInt(row)
        binary_payload += SDK_Helper.EncodeInt(column)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetCell')
        
        if response.status_code == 200:
            print(f"GetCell: Success")

            
            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetColorSpaceBitmap(color_space_scheme_name, width, height):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(color_space_scheme_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeString(height)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetColorSpaceBitmap')
        
        if response.status_code == 200:
            print(f"GetColorSpaceBitmap: Success")

            # Decode the response
            result = SDK_Helper.DecodeByteArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetComputationCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetComputationCount')
        
        if response.status_code == 200:
            print(f"GetComputationCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetComputationName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetComputationName')
        
        if response.status_code == 200:
            print(f"GetComputationName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetComputationProperty(property_name, computation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(computation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetComputationProperty')
        
        if response.status_code == 200:
            print(f"GetComputationProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetCountsFromLuminance(iris_ID, exposure_time, luminance):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(iris_ID)
        binary_payload += SDK_Helper.EncodeDouble(exposure_time)
        binary_payload += SDK_Helper.EncodeDouble(luminance)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetCountsFromLuminance')
        
        if response.status_code == 200:
            print(f"GetCountsFromLuminance: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetDataTableProperty(property_name, data_table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetDataTableProperty')
        
        if response.status_code == 200:
            print(f"GetDataTableProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetDataTableRange(data_table_name, start_column, end_column, start_row, end_row, param):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(data_table_name)
        binary_payload += SDK_Helper.EncodeString(start_column)
        binary_payload += SDK_Helper.EncodeInt(end_column)
        binary_payload += SDK_Helper.EncodeInt(start_row)
        binary_payload += SDK_Helper.EncodeInt(end_row)
        binary_payload += SDK_Helper.EncodeInt(param)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetDataTableRange')
        
        if response.status_code == 200:
            print(f"GetDataTableRange: Success")

            # Decode the response
            result = SDK_Helper.DecodeDoubleArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetDataTableStat(data_table_name, stat_name, start_col, end_col, start_row, end_row):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(stat_name)
        binary_payload += SDK_Helper.EncodeInt(start_col)
        binary_payload += SDK_Helper.EncodeInt(end_col)
        binary_payload += SDK_Helper.EncodeInt(start_row)
        binary_payload += SDK_Helper.EncodeInt(end_row)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetDataTableStat')
        
        if response.status_code == 200:
            print(f"GetDataTableStat: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetDictionaryValue(dictionary_name, key):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(dictionary_name)
        binary_payload += SDK_Helper.EncodeString(key)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetDictionaryValue')
        
        if response.status_code == 200:
            print(f"GetDictionaryValue: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetDocumentProperty(property_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetDocumentProperty')
        
        if response.status_code == 200:
            print(f"GetDocumentProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetDocumentVariable(name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetDocumentVariable')
        
        if response.status_code == 200:
            print(f"GetDocumentVariable: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetEvaluationCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetEvaluationCount')
        
        if response.status_code == 200:
            print(f"GetEvaluationCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetEvaluationName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetEvaluationName')
        
        if response.status_code == 200:
            print(f"GetEvaluationName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetEvaluationProperty(property_name, evaluation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(evaluation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetEvaluationProperty')
        
        if response.status_code == 200:
            print(f"GetEvaluationProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetEvaluationTableCellValue(evaluation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(evaluation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetEvaluationTableCellValue')
        
        if response.status_code == 200:
            print(f"GetEvaluationTableCellValue: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetFilterCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetFilterCount')
        
        if response.status_code == 200:
            print(f"GetFilterCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetFilterName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetFilterName')
        
        if response.status_code == 200:
            print(f"GetFilterName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetFilterProperty(property_name, spatial_filter_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(spatial_filter_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetFilterProperty')
        
        if response.status_code == 200:
            print(f"GetFilterProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetFocusPercent():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetFocusPercent')
        
        if response.status_code == 200:
            print(f"GetFocusPercent: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetFolderPath(special_folder_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(special_folder_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetFolderPath')
        
        if response.status_code == 200:
            print(f"GetFolderPath: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetGlobal(global_variable_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(global_variable_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetGlobal')
        
        if response.status_code == 200:
            print(f"GetGlobal: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetHighlightRuleCount(highlight_scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(highlight_scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetHighlightRuleCount')
        
        if response.status_code == 200:
            print(f"GetHighlightRuleCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetHighlightRuleProperty(property_name, highlight_scheme_name, rule_index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(highlight_scheme_name)
        binary_payload += SDK_Helper.EncodeInt(rule_index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetHighlightRuleProperty')
        
        if response.status_code == 200:
            print(f"GetHighlightRuleProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetHighlightSchemeCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetHighlightSchemeCount')
        
        if response.status_code == 200:
            print(f"GetHighlightSchemeCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetHighlightSchemeName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetHighlightSchemeName')
        
        if response.status_code == 200:
            print(f"GetHighlightSchemeName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetHistogramData(measurement, aoi, bins, log):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement)
        binary_payload += SDK_Helper.EncodeString(aoi)
        binary_payload += SDK_Helper.EncodeInt(bins)
        binary_payload += SDK_Helper.EncodeBool(log)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetHistogramData')
        
        if response.status_code == 200:
            print(f"GetHistogramData: Success")

            # Decode the response
            result = SDK_Helper.DecodeFloatArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetHistogramProperty(property_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetHistogramProperty')
        
        if response.status_code == 200:
            print(f"GetHistogramProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetLastError():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetLastError')
        
        if response.status_code == 200:
            print(f"GetLastError: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetLastFormResult():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetLastFormResult')
        
        if response.status_code == 200:
            print(f"GetLastFormResult: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetLongestExposureForLuminanceMax(iris_ID, max_luminance, FoV_ID, lens_ID):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(iris_ID)
        binary_payload += SDK_Helper.EncodeInt(max_luminance)
        binary_payload += SDK_Helper.EncodeInt(FoV_ID)
        binary_payload += SDK_Helper.EncodeDouble(lens_ID)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetLongestExposureForLuminanceMax')
        
        if response.status_code == 200:
            print(f"GetLongestExposureForLuminanceMax: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMeasurementBitmap(name, show_isolines, show_AOIs, show_AOI_highlights, show_AOI_labels, show_annotation):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(name)
        binary_payload += SDK_Helper.EncodeBool(show_isolines)
        binary_payload += SDK_Helper.EncodeBool(show_AOIs)
        binary_payload += SDK_Helper.EncodeBool(show_AOI_highlights)
        binary_payload += SDK_Helper.EncodeBool(show_AOI_labels)
        binary_payload += SDK_Helper.EncodeBool(show_annotation)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMeasurementBitmap')
        
        if response.status_code == 200:
            print(f"GetMeasurementBitmap: Success")

            # Decode the response
            result = SDK_Helper.DecodeByteArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMeasurementBitmapEx(measurement_name, show_measurement, show_isolines, show_AOIs, show_highlights, show_AOI_labels, show_annotation, bounding_AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(show_measurement)
        binary_payload += SDK_Helper.EncodeBool(show_isolines)
        binary_payload += SDK_Helper.EncodeBool(show_AOIs)
        binary_payload += SDK_Helper.EncodeBool(show_highlights)
        binary_payload += SDK_Helper.EncodeBool(show_AOI_labels)
        binary_payload += SDK_Helper.EncodeBool(show_annotation)
        binary_payload += SDK_Helper.EncodeString(bounding_AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMeasurementBitmapEx')
        
        if response.status_code == 200:
            print(f"GetMeasurementBitmapEx: Success")

            # Decode the response
            result = SDK_Helper.DecodeByteArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMeasurementCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMeasurementCount')
        
        if response.status_code == 200:
            print(f"GetMeasurementCount: Success")

            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMeasurementData(measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMeasurementData')
        
        if response.status_code == 200:
            print(f"GetMeasurementData: Success")

            # Decode the response
            result = SDK_Helper.DecodeFloatArray(response.content)
            return result
        
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMeasurementHistogramBitmap(measurement_name, width, height, y_axis_log, x_axis_log, zoom_horizontal):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeBool(y_axis_log)
        binary_payload += SDK_Helper.EncodeBool(x_axis_log)
        binary_payload += SDK_Helper.EncodeBool(zoom_horizontal)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMeasurementHistogramBitmap')
        
        if response.status_code == 200:
            print(f"GetMeasurementHistogramBitmap: Success")

            # Decode the response
            result = SDK_Helper.DecodeByteArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMeasurementLineData(measurement_component_name, x0, y0, x1, y1):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_component_name)
        binary_payload += SDK_Helper.EncodeInt(x0)
        binary_payload += SDK_Helper.EncodeInt(y0)
        binary_payload += SDK_Helper.EncodeInt(x1)
        binary_payload += SDK_Helper.EncodeInt(y1)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMeasurementLineData')
        
        if response.status_code == 200:
            print(f"GetMeasurementLineData: Success")

            # Decode the response
            result = SDK_Helper.DecodeFloatArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMeasurementLogData(measurement_name, log_section_name, log_subsection_name, item_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(log_section_name)
        binary_payload += SDK_Helper.EncodeString(log_subsection_name)
        binary_payload += SDK_Helper.EncodeString(item_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMeasurementLogData')
        
        if response.status_code == 200:
            print(f"GetMeasurementLogData: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMeasurementName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMeasurementName')
        
        if response.status_code == 200:
            print(f"GetMeasurementName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMeasurementProperty(property_name, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMeasurementProperty')
        
        if response.status_code == 200:
            print(f"GetMeasurementProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMeasurementThetaHVBitmap(measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMeasurementThetaHVBitmap')
        
        if response.status_code == 200:
            print(f"GetMeasurementThetaHVBitmap: Success")

            # Decode the response
            result = SDK_Helper.DecodeByteArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMetaInfo(variable_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(variable_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMetaInfo')
        
        if response.status_code == 200:
            print(f"GetMetaInfo: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMetaPlotBitmap(meta_plot_scheme_name, width, height, stat_name, y_axis_log, x_axis_log, normalize, first_datum_as_baseline):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(meta_plot_scheme_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeInt(stat_name)
        binary_payload += SDK_Helper.EncodeBool(y_axis_log)
        binary_payload += SDK_Helper.EncodeBool(x_axis_log)
        binary_payload += SDK_Helper.EncodeBool(normalize)
        binary_payload += SDK_Helper.EncodeBool(first_datum_as_baseline)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMetaPlotBitmap')
        
        if response.status_code == 200:
            print(f"GetMetaPlotBitmap: Success")

            # Decode the response
            result = SDK_Helper.DecodeByteArray(response.content)
            return result
        
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMetaPlotData(meta_field_name, aoi_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(meta_field_name)
        binary_payload += SDK_Helper.EncodeString(aoi_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMetaPlotData')
        
        if response.status_code == 200:
            print(f"GetMetaPlotData: Success")

            # Decode the response
            result = SDK_Helper.DecodeFloatArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetMmfProperty(MMF_property, MMF_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(MMF_property)
        binary_payload += SDK_Helper.EncodeString(MMF_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetMmfProperty')
        
        if response.status_code == 200:
            print(f"GetMmfProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetObjectCount(object_type_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetObjectCount')
        
        if response.status_code == 200:
            print(f"GetObjectCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetObjectName(object_type, index, child_index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type)
        binary_payload += SDK_Helper.EncodeInt(index)
        binary_payload += SDK_Helper.EncodeInt(child_index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetObjectName')
        
        if response.status_code == 200:
            print(f"GetObjectName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetObjectProperty(object_type_name, property_name, object_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(object_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetObjectProperty')
        
        if response.status_code == 200:
            print(f"GetObjectProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetPerspectiveTransform(source_quad_point_list, target_quad_point_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloatArray(source_quad_point_list)
        binary_payload += SDK_Helper.EncodeFloatArray(target_quad_point_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetPerspectiveTransform')
        
        if response.status_code == 200:
            print(f"GetPerspectiveTransform: Success")

            # Decode the response
            result = SDK_Helper.DecodeDoubleArray(response.content)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetPhotometricaSetting(setting_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(setting_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetPhotometricaSetting')
        
        if response.status_code == 200:
            print(f"GetPhotometricaSetting: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetPresentationCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetPresentationCount')
        
        if response.status_code == 200:
            print(f"GetPresentationCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetPresentationName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetPresentationName')
        
        if response.status_code == 200:
            print(f"GetPresentationName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetPresentationProperty(property_name, presentation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(presentation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetPresentationProperty')
        
        if response.status_code == 200:
            print(f"GetPresentationProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetProfileCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetProfileCount')
        
        if response.status_code == 200:
            print(f"GetProfileCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetProfileData(profile_name, measurement_name, polar, increment):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(profile_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(polar)
        binary_payload += SDK_Helper.EncodeFloat(increment)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetProfileData')
        
        if response.status_code == 200:
            print(f"GetProfileData: Success")

            # Decode the response
            result = SDK_Helper.DecodeFloatArray(response.content)
            return result

        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetProfileDataSize(profile_name, polar, increment):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(profile_name)
        binary_payload += SDK_Helper.EncodeBool(polar)
        binary_payload += SDK_Helper.EncodeFloat(increment)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetProfileDataSize')
        
        if response.status_code == 200:
            print(f"GetProfileDataSize: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetProfileName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetProfileName')
        
        if response.status_code == 200:
            print(f"GetProfileName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetProfilePlotBitmap(profile_name, width, height, measurement_name, y_axis_log, x_axis_log, smoothing_factor, polar):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(profile_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(y_axis_log)
        binary_payload += SDK_Helper.EncodeBool(x_axis_log)
        binary_payload += SDK_Helper.EncodeInt(smoothing_factor)
        binary_payload += SDK_Helper.EncodeBool(polar)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetProfilePlotBitmap')
        
        if response.status_code == 200:
            print(f"GetProfilePlotBitmap: Success")

            # Decode the response
            result = SDK_Helper.DecodeByteArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetProfileProperty(property_name, profile_name, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(profile_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetProfileProperty')
        
        if response.status_code == 200:
            print(f"GetProfileProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetReferenceSlope():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetReferenceSlope')
        
        if response.status_code == 200:
            print(f"GetReferenceSlope: Success")

            # Decode the response
            result = SDK_Helper.DecodeFloat(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetRefinementProperty(property_name, refinement_scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(refinement_scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetRefinementProperty')
        
        if response.status_code == 200:
            print(f"GetRefinementProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetRefinementSchemeCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetRefinementSchemeCount')
        
        if response.status_code == 200:
            print(f"GetRefinementSchemeCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetRefinementSchemeName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetRefinementSchemeName')
        
        if response.status_code == 200:
            print(f"GetRefinementSchemeName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetReportCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetReportCount')
        
        if response.status_code == 200:
            print(f"GetReportCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetReportName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetReportName')
        
        if response.status_code == 200:
            print(f"GetReportName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetScriptCode(script_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(script_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetScriptCode')
        
        if response.status_code == 200:
            print(f"GetScriptCode: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetScriptCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetScriptCount')
        
        if response.status_code == 200:
            print(f"GetScriptCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetScriptName(index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetScriptName')
        
        if response.status_code == 200:
            print(f"GetScriptName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetSelectedAoiName():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetSelectedAoiName')
        
        if response.status_code == 200:
            print(f"GetSelectedAoiName: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetSelectedPixelCount():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetSelectedPixelCount')
        
        if response.status_code == 200:
            print(f"GetSelectedPixelCount: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetShortestExposureForMidLuminance(iris_ID, luminance):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(iris_ID)
        binary_payload += SDK_Helper.EncodeDouble(luminance)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetShortestExposureForMidLuminance')
        
        if response.status_code == 200:
            print(f"GetShortestExposureForMidLuminance: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetSoftwareInfo():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetSoftwareInfo')
        
        if response.status_code == 200:
            print(f"GetSoftwareInfo: Success")

            # Decode the response
            versionMajor = SDK_Helper.DecodeInt(response.content[:4])
            versionMinor = SDK_Helper.DecodeInt(response.content[4:8])
            versionBuild = SDK_Helper.DecodeInt(response.content[8:12])
            return (versionMajor, versionMinor, versionBuild)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetSurfacePlotBitmap(measurement_name, width, height, AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetSurfacePlotBitmap')
        
        if response.status_code == 200:
            print(f"GetSurfacePlotBitmap: Success")

            # Decode the response
            result = SDK_Helper.DecodeByteArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetThermometerBitmap(measurement_name, width, height):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetThermometerBitmap')
        
        if response.status_code == 200:
            print(f"GetThermometerBitmap: Success")

            # Decode the response
            result = SDK_Helper.DecodeByteArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetTimePlotData(measurement_name, aoi_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(aoi_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetTimePlotData')
        
        if response.status_code == 200:
            print(f"GetTimePlotData: Success")

            # Decode the response
            result = SDK_Helper.DecodeFloatArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetTranslatedText(row, table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(row)
        binary_payload += SDK_Helper.EncodeString(table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetTranslatedText')
        
        if response.status_code == 200:
            print(f"GetTranslatedText: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetTypeUnits(data_type_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_type_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetTypeUnits')
        
        if response.status_code == 200:
            print(f"GetTypeUnits: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetUdwCtrlProperty(UDW_name, UDW_control_name, property_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        binary_payload += SDK_Helper.EncodeString(property_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetUdwCtrlProperty')
        
        if response.status_code == 200:
            print(f"GetUdwCtrlProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetUdwCtrlText(UDW_name, UDW_control_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetUdwCtrlText')
        
        if response.status_code == 200:
            print(f"GetUdwCtrlText: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetWindowProperty(window_name, property_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(window_name)
        binary_payload += SDK_Helper.EncodeString(property_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetWindowProperty')
        
        if response.status_code == 200:
            print(f"GetWindowProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetWorkingFolder(get_name_only):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(get_name_only)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetWorkingFolder')
        
        if response.status_code == 200:
            print(f"GetWorkingFolder: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GetWorkspaceProperty(property_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GetWorkspaceProperty')
        
        if response.status_code == 200:
            print(f"GetWorkspaceProperty: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GIArea(color_region_name, AOI_name, tab_delimited_measurement_names):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(color_region_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_measurement_names)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GIArea')
        
        if response.status_code == 200:
            print(f"GIArea: Success")

            # Decode the response
            result = SDK_Helper.DecodeDouble(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def GroupAoiByMetaField(AMF_name, reverse):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AMF_name)
        binary_payload += SDK_Helper.EncodeBool(reverse)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'GroupAoiByMetaField')
        
        if response.status_code == 200:
            print(f"GroupAoiByMetaField: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def HasDictionaryKey(dictionary_name, key):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(dictionary_name)
        binary_payload += SDK_Helper.EncodeString(key)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'HasDictionaryKey')
        
        if response.status_code == 200:
            print(f"HasDictionaryKey: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def HighlightSchemeExists(highlight_scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(highlight_scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'HighlightSchemeExists')
        
        if response.status_code == 200:
            print(f"HighlightSchemeExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def HttpRequest(URL):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(URL)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'HttpRequest')
        
        if response.status_code == 200:
            print(f"HttpRequest: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ImportDocument(file_path, tab_delimited_measurement_names, measurements_only):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_measurement_names)
        binary_payload += SDK_Helper.EncodeBool(measurements_only)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ImportDocument')
        
        if response.status_code == 200:
            print(f"ImportDocument: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ImportIntoDataTable(data_table_name, file_path, append):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(file_path)
        binary_payload += SDK_Helper.EncodeBool(append)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ImportIntoDataTable')
        
        if response.status_code == 200:
            print(f"ImportIntoDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def InvertSelection():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'InvertSelection')
        
        if response.status_code == 200:
            print(f"InvertSelection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def IsAoiVisibleInWorkspace(aoi, measurement):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(aoi)
        binary_payload += SDK_Helper.EncodeString(measurement)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'IsAoiVisibleInWorkspace')
        
        if response.status_code == 200:
            print(f"IsAoiVisibleInWorkspace: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def IsContinuousMeasuringRunning():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'IsContinuousMeasuringRunning')
        
        if response.status_code == 200:
            print(f"IsContinuousMeasuringRunning: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def IsFile(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'IsFile')
        
        if response.status_code == 200:
            print(f"IsFile: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def IsFilterRegistrationIdentityMatrix(spectral_filter_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(spectral_filter_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'IsFilterRegistrationIdentityMatrix')
        
        if response.status_code == 200:
            print(f"IsFilterRegistrationIdentityMatrix: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def IsFolder(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'IsFolder')
        
        if response.status_code == 200:
            print(f"IsFolder: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def IsObjectNameLegal(name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'IsObjectNameLegal')
        
        if response.status_code == 200:
            print(f"IsObjectNameLegal: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def IsPreviewRunning():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'IsPreviewRunning')
        
        if response.status_code == 200:
            print(f"IsPreviewRunning: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def LoadDll(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'LoadDll')
        
        if response.status_code == 200:
            print(f"LoadDll: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def LoadDriverDll(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'LoadDriverDll')
        
        if response.status_code == 200:
            print(f"LoadDriverDll: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def LoadLayout(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'LoadLayout')
        
        if response.status_code == 200:
            print(f"LoadLayout: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def LoadPackage(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'LoadPackage')
        
        if response.status_code == 200:
            print(f"LoadPackage: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def LoadWorkspaceScheme(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'LoadWorkspaceScheme')
        
        if response.status_code == 200:
            print(f"LoadWorkspaceScheme: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def MakeChildAoi(parent_AOI_name, visible_in_table, tab_delimited_AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(parent_AOI_name)
        binary_payload += SDK_Helper.EncodeBool(visible_in_table)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'MakeChildAoi')
        
        if response.status_code == 200:
            print(f"MakeChildAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def MakeFolder(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'MakeFolder')
        
        if response.status_code == 200:
            print(f"MakeFolder: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def MakeGridFromScatteredPoints(target_dt_name, input_dt_name, x0, y0, width, height, columns, rows, max_points, max_distance):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(target_dt_name)
        binary_payload += SDK_Helper.EncodeString(input_dt_name)
        binary_payload += SDK_Helper.EncodeInt(x0)
        binary_payload += SDK_Helper.EncodeInt(y0)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeInt(columns)
        binary_payload += SDK_Helper.EncodeInt(rows)
        binary_payload += SDK_Helper.EncodeInt(max_points)
        binary_payload += SDK_Helper.EncodeInt(max_distance)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'MakeGridFromScatteredPoints')
        
        if response.status_code == 200:
            print(f"MakeGridFromScatteredPoints: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def MakeNameSafe(text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'MakeNameSafe')
        
        if response.status_code == 200:
            print(f"MakeNameSafe: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def MakeNameUnique(object_type_name, proposed_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        binary_payload += SDK_Helper.EncodeString(proposed_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'MakeNameUnique')
        
        if response.status_code == 200:
            print(f"MakeNameUnique: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def MaskDrawImage(image_name, x, y, opacity_threshold):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(image_name)
        binary_payload += SDK_Helper.EncodeInt(x)
        binary_payload += SDK_Helper.EncodeInt(y)
        binary_payload += SDK_Helper.EncodeInt(opacity_threshold)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'MaskDrawImage')
        
        if response.status_code == 200:
            print(f"MaskDrawImage: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def MeasurementCommit(name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'MeasurementCommit')
        
        if response.status_code == 200:
            print(f"MeasurementCommit: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def MeasurementExists(name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'MeasurementExists')
        
        if response.status_code == 200:
            print(f"MeasurementExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def MoveAllAoi(delta_x, delta_y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(delta_x)
        binary_payload += SDK_Helper.EncodeInt(delta_y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'MoveAllAoi')
        
        if response.status_code == 200:
            print(f"MoveAllAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def MoveAoi(delta_x, delta_y, AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(delta_x)
        binary_payload += SDK_Helper.EncodeInt(delta_y)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'MoveAoi')
        
        if response.status_code == 200:
            print(f"MoveAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def NewForInstrument(parameters):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(parameters)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'NewForInstrument')
        
        if response.status_code == 200:
            print(f"NewForInstrument: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def NewFromTemplate(file_path, save_dirty):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        binary_payload += SDK_Helper.EncodeInt(save_dirty)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'NewFromTemplate')
        
        if response.status_code == 200:
            print(f"NewFromTemplate: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def NewPMM(save_dirty):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(save_dirty)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'NewPMM')
        
        if response.status_code == 200:
            print(f"NewPMM: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ObjectExists(object_type_name, object_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        binary_payload += SDK_Helper.EncodeString(object_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ObjectExists')
        
        if response.status_code == 200:
            print(f"ObjectExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def OpenDocument(file_path, save_dirty, only_measurements):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        binary_payload += SDK_Helper.EncodeInt(save_dirty)
        binary_payload += SDK_Helper.EncodeBool(only_measurements)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'OpenDocument')
        
        if response.status_code == 200:
            print(f"OpenDocument: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def OpenFileInDefaultProgram(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'OpenFileInDefaultProgram')
        
        if response.status_code == 200:
            print(f"OpenFileInDefaultProgram: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def OpenPMM(file_path, save_dirty, measurements_only):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        binary_payload += SDK_Helper.EncodeInt(save_dirty)
        binary_payload += SDK_Helper.EncodeBool(measurements_only)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'OpenPMM')
        
        if response.status_code == 200:
            print(f"OpenPMM: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def OpenSerialPort(port_name, bit_rate, data_bits, stop_bits, parity):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(port_name)
        binary_payload += SDK_Helper.EncodeInt(bit_rate)
        binary_payload += SDK_Helper.EncodeInt(data_bits)
        binary_payload += SDK_Helper.EncodeString(stop_bits)
        binary_payload += SDK_Helper.EncodeString(parity)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'OpenSerialPort')
        
        if response.status_code == 200:
            print(f"OpenSerialPort: Success")

            # Decode the response
            result = SDK_Helper.DecodeInt(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def PolarToXY(theta, phi):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(theta)
        binary_payload += SDK_Helper.EncodeDouble(phi)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'PolarToXY')
        
        if response.status_code == 200:
            print(f"PolarToXY: Success")

            # Decode the response
            result1 = SDK_Helper.DecodeDouble(response.content[:8])
            result2 = SDK_Helper.DecodeDouble(response.content[8:])

            return (result1, result2)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def PolynomialFit(x_list, y_list, degree):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDoubleArray(x_list)
        binary_payload += SDK_Helper.EncodeDoubleArray(y_list)
        binary_payload += SDK_Helper.EncodeInt(degree)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'PolynomialFit')
        
        if response.status_code == 200:
            print(f"PolynomialFit: Success")

            # Decode the response
            result = SDK_Helper.DecodeDoubleArray(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def PresentationExists(presentation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(presentation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'PresentationExists')
        
        if response.status_code == 200:
            print(f"PresentationExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def PrintReport(report_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'PrintReport')
        
        if response.status_code == 200:
            print(f"PrintReport: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ProfileExists(profile_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(profile_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ProfileExists')
        
        if response.status_code == 200:
            print(f"ProfileExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def PromoteAoi(child_AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(child_AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'PromoteAoi')
        
        if response.status_code == 200:
            print(f"PromoteAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ReadFromSerialPort(serial_port_handle, delimiter):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(serial_port_handle)
        binary_payload += SDK_Helper.EncodeString(delimiter)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ReadFromSerialPort')
        
        if response.status_code == 200:
            print(f"ReadFromSerialPort: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RedoRefinement(tab_delimited_AOI_names):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(tab_delimited_AOI_names)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RedoRefinement')
        
        if response.status_code == 200:
            print(f"RedoRefinement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RefineAoi(AOI_name, measurement_name, use_min_value, use_max_value, min_value, max_value, erosion_amount, min_area, options_string):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(use_min_value)
        binary_payload += SDK_Helper.EncodeBool(use_max_value)
        binary_payload += SDK_Helper.EncodeFloat(min_value)
        binary_payload += SDK_Helper.EncodeFloat(max_value)
        binary_payload += SDK_Helper.EncodeInt(erosion_amount)
        binary_payload += SDK_Helper.EncodeInt(min_area)
        binary_payload += SDK_Helper.EncodeString(options_string)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RefineAoi')
        
        if response.status_code == 200:
            print(f"RefineAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RefinementSchemeExists(name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RefinementSchemeExists')
        
        if response.status_code == 200:
            print(f"RefinementSchemeExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RefineToMask(refinement_scheme_name, AOI_name, measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(refinement_scheme_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RefineToMask')
        
        if response.status_code == 200:
            print(f"RefineToMask: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RegenerateComponents(measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RegenerateComponents')
        
        if response.status_code == 200:
            print(f"RegenerateComponents: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RemoveAoiFromMask(AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RemoveAoiFromMask')
        
        if response.status_code == 200:
            print(f"RemoveAoiFromMask: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RemoveColorRegionsFromGroup(color_group_name, color_region_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(color_group_name)
        binary_payload += SDK_Helper.EncodeString(color_region_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RemoveColorRegionsFromGroup')
        
        if response.status_code == 200:
            print(f"RemoveColorRegionsFromGroup: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RemoveColumn(data_table_name, column_index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeInt(column_index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RemoveColumn')
        
        if response.status_code == 200:
            print(f"RemoveColumn: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RemoveCropping():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RemoveCropping')
        
        if response.status_code == 200:
            print(f"RemoveCropping: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RemoveDictionaryKey(dictionary_name, key):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(dictionary_name)
        binary_payload += SDK_Helper.EncodeString(key)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RemoveDictionaryKey')
        
        if response.status_code == 200:
            print(f"RemoveDictionaryKey: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RemoveRow(data_table_name, row_index):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeInt(row_index)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RemoveRow')
        
        if response.status_code == 200:
            print(f"RemoveRow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RemoveSelectionFromMask():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RemoveSelectionFromMask')
        
        if response.status_code == 200:
            print(f"RemoveSelectionFromMask: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RenameAoi(old_name, new_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(old_name)
        binary_payload += SDK_Helper.EncodeInt(new_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RenameAoi')
        
        if response.status_code == 200:
            print(f"RenameAoi: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RenameObject(object_type_name, old_name, new_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        binary_payload += SDK_Helper.EncodeString(old_name)
        binary_payload += SDK_Helper.EncodeString(new_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RenameObject')
        
        if response.status_code == 200:
            print(f"RenameObject: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ReportExists(report_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ReportExists')
        
        if response.status_code == 200:
            print(f"ReportExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ResetInstrumentMask():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ResetInstrumentMask')
        
        if response.status_code == 200:
            print(f"ResetInstrumentMask: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ResetWindows():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ResetWindows')
        
        if response.status_code == 200:
            print(f"ResetWindows: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ResizeDataTable(data_table_name, new_row_count, new_column_count, clear_existing_data):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeInt(new_row_count)
        binary_payload += SDK_Helper.EncodeInt(new_column_count)
        binary_payload += SDK_Helper.EncodeBool(clear_existing_data)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ResizeDataTable')
        
        if response.status_code == 200:
            print(f"ResizeDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RevertToRestorePoint():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RevertToRestorePoint')
        
        if response.status_code == 200:
            print(f"RevertToRestorePoint: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RotateAllAoi(angle_in_degrees, center_x, center_y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(angle_in_degrees)
        binary_payload += SDK_Helper.EncodeInt(center_x)
        binary_payload += SDK_Helper.EncodeInt(center_y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RotateAllAoi')
        
        if response.status_code == 200:
            print(f"RotateAllAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RotateAoi(angle_in_degrees, AOI_name, center_x, center_y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(angle_in_degrees)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeInt(center_x)
        binary_payload += SDK_Helper.EncodeInt(center_y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RotateAoi')
        
        if response.status_code == 200:
            print(f"RotateAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RunConsoleCommand(text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RunConsoleCommand')
        
        if response.status_code == 200:
            print(f"RunConsoleCommand: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RunNamedScript(script_name, parameter_values):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(script_name)

        parameter_encoding = b""
        # define this array based on the formatting in the enum in c#
        parameter_type_int_array = []
        # then we need to encode the parameter_values based on what the types are that we encounter
        for i in range(len(parameter_values)):
            # is the parameter a string or a number?
            if isinstance(parameter_values[i], str):
                # if it is a string, we need to encode it as a string
                parameter_encoding += SDK_Helper.EncodeString(parameter_values[i])
                # and add the type to the array
                parameter_type_int_array.append(ParameterType.STRING.value)
            elif isinstance(parameter_values[i], int):
                # if it is an int, we need to encode it as an int
                parameter_encoding += SDK_Helper.EncodeInt(parameter_values[i])
                # and add the type to the array
                parameter_type_int_array.append(ParameterType.INT.value)
            elif isinstance(parameter_values[i], float):
                # if it is a float, we need to encode it as a float
                parameter_encoding += SDK_Helper.EncodeFloat(parameter_values[i])
                # and add the type to the array
                parameter_type_int_array.append(ParameterType.FLOAT.value)
            elif isinstance(parameter_values[i], bool):
                # if it is a bool, we need to encode it as a bool
                parameter_encoding += SDK_Helper.EncodeBool(parameter_values[i])
                # and add the type to the array
                parameter_type_int_array.append(ParameterType.BOOL.value)
            elif isinstance(parameter_values[i], list):
                # this is not supported
                raise ValueError("List type is not supported")
            else:
                # this is not supported
                raise ValueError("Unsupported type")
        
        # Encode the parameter type array as a list of ints
        binary_payload += SDK_Helper.EncodeIntArray(parameter_type_int_array)

        # Add the parameter encoding to the binary payload
        binary_payload += parameter_encoding
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RunNamedScript')
        
        if response.status_code == 200:
            print(f"RunNamedScript: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RunScript(script_text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(script_text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RunScript')
        
        if response.status_code == 200:
            print(f"RunScript: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RunUdwCtrlScript(UDW_name, UDW_control_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RunUdwCtrlScript')
        
        if response.status_code == 200:
            print(f"RunUdwCtrlScript: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def RwuToXY(real_world_x, real_world_y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(real_world_x)
        binary_payload += SDK_Helper.EncodeDouble(real_world_y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'RwuToXY')
        
        if response.status_code == 200:
            print(f"RwuToXY: Success")

            # Decode the response
            result1 = SDK_Helper.DecodeDouble(response.content[:8])
            result2 = SDK_Helper.DecodeDouble(response.content[8:])
            return (result1, result2)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SaveGraphic(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SaveGraphic')
        
        if response.status_code == 200:
            print(f"SaveGraphic: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SaveGraphicAs():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SaveGraphicAs')
        
        if response.status_code == 200:
            print(f"SaveGraphicAs: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SaveLayout(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SaveLayout')
        
        if response.status_code == 200:
            print(f"SaveLayout: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SaveObjects(object_type_name, object_name_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        binary_payload += SDK_Helper.EncodeString(object_name_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SaveObjects')
        
        if response.status_code == 200:
            print(f"SaveObjects: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SaveObjectToFile(object_type_name, object_name, file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        binary_payload += SDK_Helper.EncodeString(object_name)
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SaveObjectToFile')
        
        if response.status_code == 200:
            print(f"SaveObjectToFile: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SavePackage(target_package_name, object_type_name_and_object_name_list, tab_delimited_requirements, tab_delimited_options):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(target_package_name)
        binary_payload += SDK_Helper.EncodeString(object_type_name_and_object_name_list)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_requirements)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_options)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SavePackage')
        
        if response.status_code == 200:
            print(f"SavePackage: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SavePDFReport(report, file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report)
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SavePDFReport')
        
        if response.status_code == 200:
            print(f"SavePDFReport: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SavePMM(file_path, use_save_as_dialog):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        binary_payload += SDK_Helper.EncodeBool(use_save_as_dialog)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SavePMM')
        
        if response.status_code == 200:
            print(f"SavePMM: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SaveRestorePoint(text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SaveRestorePoint')
        
        if response.status_code == 200:
            print(f"SaveRestorePoint: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SaveWorkspaceScheme(file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SaveWorkspaceScheme')
        
        if response.status_code == 200:
            print(f"SaveWorkspaceScheme: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SaveXLSXReport(report_name, file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SaveXLSXReport')
        
        if response.status_code == 200:
            print(f"SaveXLSXReport: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SaveXPSReport(report_name, file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(report_name)
        binary_payload += SDK_Helper.EncodeString(file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SaveXPSReport')
        
        if response.status_code == 200:
            print(f"SaveXPSReport: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ScriptExists(script_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(script_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ScriptExists')
        
        if response.status_code == 200:
            print(f"ScriptExists: Success")

            # Decode the response
            result = SDK_Helper.DecodeBool(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SelectAll():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SelectAll')
        
        if response.status_code == 200:
            print(f"SelectAll: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SelectAllAoi(include_children):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(include_children)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SelectAllAoi')
        
        if response.status_code == 200:
            print(f"SelectAllAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SelectAoi(tab_delimited_AOI_names):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(tab_delimited_AOI_names)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SelectAoi')
        
        if response.status_code == 200:
            print(f"SelectAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SelectAoiIntersection(AOI_name_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SelectAoiIntersection')
        
        if response.status_code == 200:
            print(f"SelectAoiIntersection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SelectLine(point_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(point_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SelectLine')
        
        if response.status_code == 200:
            print(f"SelectLine: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SelectObjects(object_type_name, object_name_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        binary_payload += SDK_Helper.EncodeString(object_name_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SelectObjects')
        
        if response.status_code == 200:
            print(f"SelectObjects: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SelectPolygon(point_list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(point_list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SelectPolygon')
        
        if response.status_code == 200:
            print(f"SelectPolygon: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SelectRegion(measurement_name, use_min_value, min_value, use_max_value, max_value, include_underexposed, include_overexposed, include_invalid, inside_existing_selection):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(use_min_value)
        binary_payload += SDK_Helper.EncodeFloat(min_value)
        binary_payload += SDK_Helper.EncodeBool(use_max_value)
        binary_payload += SDK_Helper.EncodeFloat(max_value)
        binary_payload += SDK_Helper.EncodeBool(include_underexposed)
        binary_payload += SDK_Helper.EncodeBool(include_overexposed)
        binary_payload += SDK_Helper.EncodeBool(include_invalid)
        binary_payload += SDK_Helper.EncodeBool(inside_existing_selection)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SelectRegion')
        
        if response.status_code == 200:
            print(f"SelectRegion: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetActiveMeasurement(measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetActiveMeasurement')
        
        if response.status_code == 200:
            print(f"SetActiveMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetActiveWhitePoint(tristimulus_X, tristimulus_Y, tristimulus_Z):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(tristimulus_X)
        binary_payload += SDK_Helper.EncodeDouble(tristimulus_Y)
        binary_payload += SDK_Helper.EncodeDouble(tristimulus_Z)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetActiveWhitePoint')
        
        if response.status_code == 200:
            print(f"SetActiveWhitePoint: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetAoiColumnVisible(column_number, boolean):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(column_number)
        binary_payload += SDK_Helper.EncodeBool(boolean)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetAoiColumnVisible')
        
        if response.status_code == 200:
            print(f"SetAoiColumnVisible: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetAoiHighlightOpacity(alpha):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeByte(alpha)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetAoiHighlightOpacity')
        
        if response.status_code == 200:
            print(f"SetAoiHighlightOpacity: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetAoiLabelProperties(show_root_AOIs, show_child_AOIs, font_size):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(show_root_AOIs)
        binary_payload += SDK_Helper.EncodeBool(show_child_AOIs)
        binary_payload += SDK_Helper.EncodeInt(font_size)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetAoiLabelProperties')
        
        if response.status_code == 200:
            print(f"SetAoiLabelProperties: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetAoiProperty(property_name, AOI_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetAoiProperty')
        
        if response.status_code == 200:
            print(f"SetAoiProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetAoiRegionProperties(alpha, r, g, b):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeByte(alpha)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetAoiRegionProperties')
        
        if response.status_code == 200:
            print(f"SetAoiRegionProperties: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetAoiSummaryProperty(property, name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property)
        binary_payload += SDK_Helper.EncodeString(name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetAoiSummaryProperty')
        
        if response.status_code == 200:
            print(f"SetAoiSummaryProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetAoiVisibleInAoiTable(boolean, tab_delimited_AOI_names):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(boolean)
        binary_payload += SDK_Helper.EncodeBool(tab_delimited_AOI_names)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetAoiVisibleInAoiTable')
        
        if response.status_code == 200:
            print(f"SetAoiVisibleInAoiTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetAoiVisibleInWorkspace(boolean, tab_delimited_AOI_names):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(boolean)
        binary_payload += SDK_Helper.EncodeBool(tab_delimited_AOI_names)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetAoiVisibleInWorkspace')
        
        if response.status_code == 200:
            print(f"SetAoiVisibleInWorkspace: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetAutoResponse(popup_ID, response_code):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(popup_ID)
        binary_payload += SDK_Helper.EncodeInt(response_code)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetAutoResponse')
        
        if response.status_code == 200:
            print(f"SetAutoResponse: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCameraProperty(property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCameraProperty')
        
        if response.status_code == 200:
            print(f"SetCameraProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCaptureExposureRange(capture_scheme_name, spectral_filter_name, range_min_value, range_max_value, padding_scalar, exposure_stepping):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(capture_scheme_name)
        binary_payload += SDK_Helper.EncodeString(spectral_filter_name)
        binary_payload += SDK_Helper.EncodeDouble(range_min_value)
        binary_payload += SDK_Helper.EncodeDouble(range_max_value)
        binary_payload += SDK_Helper.EncodeDouble(padding_scalar)
        binary_payload += SDK_Helper.EncodeInt(exposure_stepping)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCaptureExposureRange')
        
        if response.status_code == 200:
            print(f"SetCaptureExposureRange: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCaptureProperty(property_name, capture_scheme_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(capture_scheme_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCaptureProperty')
        
        if response.status_code == 200:
            print(f"SetCaptureProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCaptureSettings(property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCaptureSettings')
        
        if response.status_code == 200:
            print(f"SetCaptureSettings: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCaptureTestPattern(pattern):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(pattern)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCaptureTestPattern')
        
        if response.status_code == 200:
            print(f"SetCaptureTestPattern: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCell(data_table_name, row, column, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeInt(row)
        binary_payload += SDK_Helper.EncodeInt(column)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCell')
        
        if response.status_code == 200:
            print(f"SetCell: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetComputationProperty(property_name, computation_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(computation_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetComputationProperty')
        
        if response.status_code == 200:
            print(f"SetComputationProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetContinuousMeasuringOverlay(image_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(image_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetContinuousMeasuringOverlay')
        
        if response.status_code == 200:
            print(f"SetContinuousMeasuringOverlay: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetContinuousMeasuringProperty(property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetContinuousMeasuringProperty')
        
        if response.status_code == 200:
            print(f"SetContinuousMeasuringProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCoordinateShift(delta_x, delta_y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(delta_x)
        binary_payload += SDK_Helper.EncodeFloat(delta_y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCoordinateShift')
        
        if response.status_code == 200:
            print(f"SetCoordinateShift: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCustomFilterRegistration(spectral_filter_name, rotation_degrees, magnification_scalar, translation_x, translation_y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(spectral_filter_name)
        binary_payload += SDK_Helper.EncodeDouble(rotation_degrees)
        binary_payload += SDK_Helper.EncodeDouble(magnification_scalar)
        binary_payload += SDK_Helper.EncodeDouble(translation_x)
        binary_payload += SDK_Helper.EncodeDouble(translation_y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCustomFilterRegistration')
        
        if response.status_code == 200:
            print(f"SetCustomFilterRegistration: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCustomFilterRegistrationFromDataTable(data_table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCustomFilterRegistrationFromDataTable')
        
        if response.status_code == 200:
            print(f"SetCustomFilterRegistrationFromDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCustomFilterRegistrationFromDutMeasurement(measurement_name, threshold_percentage, threshold_Xblue, threshold_Xred, threshold_Z, Y_behavior, custom_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeDouble(threshold_percentage)
        binary_payload += SDK_Helper.EncodeDouble(threshold_Xblue)
        binary_payload += SDK_Helper.EncodeDouble(threshold_Xred)
        binary_payload += SDK_Helper.EncodeDouble(threshold_Z)
        binary_payload += SDK_Helper.EncodeInt(Y_behavior)
        binary_payload += SDK_Helper.EncodeString(custom_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCustomFilterRegistrationFromDutMeasurement')
        
        if response.status_code == 200:
            print(f"SetCustomFilterRegistrationFromDutMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetCustomWindow(user_docker_idx, user_window, caption):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(user_docker_idx)
        binary_payload += SDK_Helper.EncodeInt(user_window)
        binary_payload += SDK_Helper.EncodeString(caption)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetCustomWindow')
        
        if response.status_code == 200:
            print(f"SetCustomWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetDataTableProperty(table_name, property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(table_name)
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetDataTableProperty')
        
        if response.status_code == 200:
            print(f"SetDataTableProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetDeviceParameter(device, param_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(device)
        binary_payload += SDK_Helper.EncodeString(param_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetDeviceParameter')
        
        if response.status_code == 200:
            print(f"SetDeviceParameter: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetDictionaryValue(dictionary_name, key, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(dictionary_name)
        binary_payload += SDK_Helper.EncodeString(key)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetDictionaryValue')
        
        if response.status_code == 200:
            print(f"SetDictionaryValue: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetDocumentProperty(document_property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(document_property_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetDocumentProperty')
        
        if response.status_code == 200:
            print(f"SetDocumentProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetDocumentVariable(document_variable_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(document_variable_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetDocumentVariable')
        
        if response.status_code == 200:
            print(f"SetDocumentVariable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetEvaluationProperty(property_name, evaluation_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(evaluation_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetEvaluationProperty')
        
        if response.status_code == 200:
            print(f"SetEvaluationProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetEventScript(UDW_name, event_name, script_text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(event_name)
        binary_payload += SDK_Helper.EncodeString(script_text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetEventScript')
        
        if response.status_code == 200:
            print(f"SetEventScript: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetExportTargetExistsAction(action_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(action_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetExportTargetExistsAction')
        
        if response.status_code == 200:
            print(f"SetExportTargetExistsAction: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetFilterProperty(property_name, spatial_filter_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(spatial_filter_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetFilterProperty')
        
        if response.status_code == 200:
            print(f"SetFilterProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetFocusIndicatorProperty():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetFocusIndicatorProperty')
        
        if response.status_code == 200:
            print(f"SetFocusIndicatorProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetGlobal(global_variable_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(global_variable_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetGlobal')
        
        if response.status_code == 200:
            print(f"SetGlobal: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetGridVisible(boolean):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(boolean)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetGridVisible')
        
        if response.status_code == 200:
            print(f"SetGridVisible: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetHighlightRule(highlight_scheme_name, rule_number, rule_name, formula, r, g, b):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(highlight_scheme_name)
        binary_payload += SDK_Helper.EncodeInt(rule_number)
        binary_payload += SDK_Helper.EncodeString(rule_name)
        binary_payload += SDK_Helper.EncodeString(formula)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetHighlightRule')
        
        if response.status_code == 200:
            print(f"SetHighlightRule: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetHighlightRuleProperty(property_name, highlight_scheme_name, rule_number, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(highlight_scheme_name)
        binary_payload += SDK_Helper.EncodeInt(rule_number)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetHighlightRuleProperty')
        
        if response.status_code == 200:
            print(f"SetHighlightRuleProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetHistogramProperty(property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeFloat(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetHistogramProperty')
        
        if response.status_code == 200:
            print(f"SetHistogramProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetIsolinesVisible(boolean):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(boolean)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetIsolinesVisible')
        
        if response.status_code == 200:
            print(f"SetIsolinesVisible: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetMeasurementLogData(measurement_name, section_name, subsection_name, item_name, data, data_type_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(section_name)
        binary_payload += SDK_Helper.EncodeString(subsection_name)
        binary_payload += SDK_Helper.EncodeString(item_name)
        binary_payload += SDK_Helper.EncodeString(data)
        binary_payload += SDK_Helper.EncodeString(data_type_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetMeasurementLogData')
        
        if response.status_code == 200:
            print(f"SetMeasurementLogData: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetMeasurementProperty(measurement_name, property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetMeasurementProperty')
        
        if response.status_code == 200:
            print(f"SetMeasurementProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetMeasurementValue(measurement_name, value, restrict_to_selection):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeFloat(value)
        binary_payload += SDK_Helper.EncodeBool(restrict_to_selection)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetMeasurementValue')
        
        if response.status_code == 200:
            print(f"SetMeasurementValue: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetMeasurementValueInAoi(measurement_name, value, AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeFloat(value)
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetMeasurementValueInAoi')
        
        if response.status_code == 200:
            print(f"SetMeasurementValueInAoi: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetMetaInfo(meta_info_name, meta_info_value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(meta_info_name)
        binary_payload += SDK_Helper.EncodeString(meta_info_value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetMetaInfo')
        
        if response.status_code == 200:
            print(f"SetMetaInfo: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetMmfProperty(property_name, MMF_name, property_value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(MMF_name)
        binary_payload += SDK_Helper.EncodeString(property_value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetMmfProperty')
        
        if response.status_code == 200:
            print(f"SetMmfProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetNextCaptureMeasurementData(wpmd):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(wpmd)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetNextCaptureMeasurementData')
        
        if response.status_code == 200:
            print(f"SetNextCaptureMeasurementData: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetObjectProperty(object_type_name, property_name, object_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(object_type_name)
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(object_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetObjectProperty')
        
        if response.status_code == 200:
            print(f"SetObjectProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetOverlayGrid(spacing_x, spacing_y, center, line_style, opacity, r, g, b):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(spacing_x)
        binary_payload += SDK_Helper.EncodeInt(spacing_y)
        binary_payload += SDK_Helper.EncodeBool(center)
        binary_payload += SDK_Helper.EncodeString(line_style)
        binary_payload += SDK_Helper.EncodeByte(opacity)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetOverlayGrid')
        
        if response.status_code == 200:
            print(f"SetOverlayGrid: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetOverlayOff():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetOverlayOff')
        
        if response.status_code == 200:
            print(f"SetOverlayOff: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetOverlayPolar(ring_spacing, spoke_spacing, line_style_name, alpha, r, g, b):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(ring_spacing)
        binary_payload += SDK_Helper.EncodeInt(spoke_spacing)
        binary_payload += SDK_Helper.EncodeString(line_style_name)
        binary_payload += SDK_Helper.EncodeByte(alpha)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetOverlayPolar')
        
        if response.status_code == 200:
            print(f"SetOverlayPolar: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetPhotometricaSetting(setting_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(setting_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetPhotometricaSetting')
        
        if response.status_code == 200:
            print(f"SetPhotometricaSetting: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetPointOfView(delta_x, delta_y, delta_z, pov_direction):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(delta_x)
        binary_payload += SDK_Helper.EncodeFloat(delta_y)
        binary_payload += SDK_Helper.EncodeFloat(delta_z)
        binary_payload += SDK_Helper.EncodeString(pov_direction)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetPointOfView')
        
        if response.status_code == 200:
            print(f"SetPointOfView: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetPresentationProperty(property_name, presentation_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(presentation_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetPresentationProperty')
        
        if response.status_code == 200:
            print(f"SetPresentationProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetPreviewOverlay(image_file_path):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(image_file_path)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetPreviewOverlay')
        
        if response.status_code == 200:
            print(f"SetPreviewOverlay: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetPreviewProperty(property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetPreviewProperty')
        
        if response.status_code == 200:
            print(f"SetPreviewProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetProfileGraphProperty(property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetProfileGraphProperty')
        
        if response.status_code == 200:
            print(f"SetProfileGraphProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetRealWorldUnits(pixel_distance, real_world_distance, unit):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(pixel_distance)
        binary_payload += SDK_Helper.EncodeFloat(real_world_distance)
        binary_payload += SDK_Helper.EncodeString(unit)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetRealWorldUnits')
        
        if response.status_code == 200:
            print(f"SetRealWorldUnits: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetReferenceSlope(slope_value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(slope_value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetReferenceSlope')
        
        if response.status_code == 200:
            print(f"SetReferenceSlope: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetReferenceSlopeFromSelection():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetReferenceSlopeFromSelection')
        
        if response.status_code == 200:
            print(f"SetReferenceSlopeFromSelection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetRefinementProperty(property_name, refinement_scheme_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(refinement_scheme_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetRefinementProperty')
        
        if response.status_code == 200:
            print(f"SetRefinementProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetRulerVisible(boolean):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(boolean)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetRulerVisible')
        
        if response.status_code == 200:
            print(f"SetRulerVisible: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetSelection(shape_name, x, y, width, height):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(shape_name)
        binary_payload += SDK_Helper.EncodeInt(x)
        binary_payload += SDK_Helper.EncodeInt(y)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetSelection')
        
        if response.status_code == 200:
            print(f"SetSelection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetSelectionProperties(alpha, r, g, b):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeByte(alpha)
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetSelectionProperties')
        
        if response.status_code == 200:
            print(f"SetSelectionProperties: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetSurfacePlotProperties(detail_level, max_contours):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(detail_level)
        binary_payload += SDK_Helper.EncodeInt(max_contours)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetSurfacePlotProperties')
        
        if response.status_code == 200:
            print(f"SetSurfacePlotProperties: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetTableFailColor(r, g, b):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeByte(r)
        binary_payload += SDK_Helper.EncodeByte(g)
        binary_payload += SDK_Helper.EncodeByte(b)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetTableFailColor')
        
        if response.status_code == 200:
            print(f"SetTableFailColor: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetTableNumericFormat(number_of_significant_digits):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(number_of_significant_digits)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetTableNumericFormat')
        
        if response.status_code == 200:
            print(f"SetTableNumericFormat: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetThermometerVisible(boolean):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(boolean)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetThermometerVisible')
        
        if response.status_code == 200:
            print(f"SetThermometerVisible: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetUdw():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetUdw')
        
        if response.status_code == 200:
            print(f"SetUdw: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetUdwCtrlImage(UDW_name, UDW_control_name, image_name, width, height):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        binary_payload += SDK_Helper.EncodeString(image_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetUdwCtrlImage')
        
        if response.status_code == 200:
            print(f"SetUdwCtrlImage: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetUdwCtrlList(UDW_name, UDW_control_name, list):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        binary_payload += SDK_Helper.EncodeString(list)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetUdwCtrlList')
        
        if response.status_code == 200:
            print(f"SetUdwCtrlList: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetUdwCtrlProperty(UDW_name, UDW_control_name, property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetUdwCtrlProperty')
        
        if response.status_code == 200:
            print(f"SetUdwCtrlProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetUdwCtrlText(UDW_name, UDW_control_name, text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetUdwCtrlText')
        
        if response.status_code == 200:
            print(f"SetUdwCtrlText: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetUdwGraphCtrlData(UDW_name, UDW_control_name, data_table_name, column_data, row_data, tab_delimited_params):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(column_data)
        binary_payload += SDK_Helper.EncodeString(row_data)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_params)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetUdwGraphCtrlData')
        
        if response.status_code == 200:
            print(f"SetUdwGraphCtrlData: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetUdwTableCtrlData(UDW_name, UDW_control_name, data_table_name, column_data, row_data, tab_delimited_extra_parameters):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeString(UDW_control_name)
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeString(column_data)
        binary_payload += SDK_Helper.EncodeString(row_data)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_extra_parameters)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetUdwTableCtrlData')
        
        if response.status_code == 200:
            print(f"SetUdwTableCtrlData: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetWindowProperty(window_name, property_name, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(window_name)
        binary_payload += SDK_Helper.EncodeString(property_name)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetWindowProperty')
        
        if response.status_code == 200:
            print(f"SetWindowProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetWindowVisible(window_name, boolean, position_name, size, sibling_window_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(window_name)
        binary_payload += SDK_Helper.EncodeBool(boolean)
        binary_payload += SDK_Helper.EncodeString(position_name)
        binary_payload += SDK_Helper.EncodeInt(size)
        binary_payload += SDK_Helper.EncodeString(sibling_window_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetWindowVisible')
        
        if response.status_code == 200:
            print(f"SetWindowVisible: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetWorkingFolder(file_path, create_if_missing):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(file_path)
        binary_payload += SDK_Helper.EncodeBool(create_if_missing)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetWorkingFolder')
        
        if response.status_code == 200:
            print(f"SetWorkingFolder: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetWorkspaceProperty(workspace_property, value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(workspace_property)
        binary_payload += SDK_Helper.EncodeString(value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetWorkspaceProperty')
        
        if response.status_code == 200:
            print(f"SetWorkspaceProperty: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetWorkspaceTooltipVisible(boolean):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(boolean)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetWorkspaceTooltipVisible')
        
        if response.status_code == 200:
            print(f"SetWorkspaceTooltipVisible: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SetZoom(zoom_type_name, param):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(zoom_type_name)
        binary_payload += SDK_Helper.EncodeInt(param)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SetZoom')
        
        if response.status_code == 200:
            print(f"SetZoom: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowAboutWindow():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowAboutWindow')
        
        if response.status_code == 200:
            print(f"ShowAboutWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowAoiCreateWindow(delete_existing_AOIs, editor_style, AOI_name_prefix):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(delete_existing_AOIs)
        binary_payload += SDK_Helper.EncodeString(editor_style)
        binary_payload += SDK_Helper.EncodeString(AOI_name_prefix)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowAoiCreateWindow')
        
        if response.status_code == 200:
            print(f"ShowAoiCreateWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowAoiPropertiesWindow(AOI_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(AOI_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowAoiPropertiesWindow')
        
        if response.status_code == 200:
            print(f"ShowAoiPropertiesWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowCaptureEditorWindow(capture_scheme_name, tab_delimited_options):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(capture_scheme_name)
        binary_payload += SDK_Helper.EncodeString(tab_delimited_options)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowCaptureEditorWindow')
        
        if response.status_code == 200:
            print(f"ShowCaptureEditorWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowCustomMessage(popup_ID, text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(popup_ID)
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowCustomMessage')
        
        if response.status_code == 200:
            print(f"ShowCustomMessage: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowHelp(topic, parameter):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(topic)
        binary_payload += SDK_Helper.EncodeString(parameter)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowHelp')
        
        if response.status_code == 200:
            print(f"ShowHelp: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowMeasurementEditorWindow(measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowMeasurementEditorWindow')
        
        if response.status_code == 200:
            print(f"ShowMeasurementEditorWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowMeasurementRegistrationWindow(measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowMeasurementRegistrationWindow')
        
        if response.status_code == 200:
            print(f"ShowMeasurementRegistrationWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowMessage(text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowMessage')
        
        if response.status_code == 200:
            print(f"ShowMessage: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowModalPopupWindow(UDW_name, width, height, sizeable):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(UDW_name)
        binary_payload += SDK_Helper.EncodeInt(width)
        binary_payload += SDK_Helper.EncodeInt(height)
        binary_payload += SDK_Helper.EncodeBool(sizeable)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowModalPopupWindow')
        
        if response.status_code == 200:
            print(f"ShowModalPopupWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowPmmManager():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowPmmManager')
        
        if response.status_code == 200:
            print(f"ShowPmmManager: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowPresentationEditorWindow(presentation_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(presentation_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowPresentationEditorWindow')
        
        if response.status_code == 200:
            print(f"ShowPresentationEditorWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ShowProfileCreateWindow(delete_existing_AOIs, thickness, show_thickness_UI):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeBool(delete_existing_AOIs)
        binary_payload += SDK_Helper.EncodeInt(thickness)
        binary_payload += SDK_Helper.EncodeBool(show_thickness_UI)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ShowProfileCreateWindow')
        
        if response.status_code == 200:
            print(f"ShowProfileCreateWindow: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SolveQuadratic(x0, y0, x1, y1, x2, y2):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(x0)
        binary_payload += SDK_Helper.EncodeDouble(y0)
        binary_payload += SDK_Helper.EncodeDouble(x1)
        binary_payload += SDK_Helper.EncodeDouble(y1)
        binary_payload += SDK_Helper.EncodeDouble(x2)
        binary_payload += SDK_Helper.EncodeDouble(y2)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SolveQuadratic')
        
        if response.status_code == 200:
            print(f"SolveQuadratic: Success")

            # Decode the response
            result1 = SDK_Helper.DecodeDouble(response.content[:8])
            result2 = SDK_Helper.DecodeDouble(response.content[8:16])
            result3 = SDK_Helper.DecodeDouble(response.content[16:])
            return (result1, result2, result3)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SortAois(tab_delimited_aoi_names, order, aoi_point, rename_parent, rename_children, cluster_proximity):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(tab_delimited_aoi_names)
        binary_payload += SDK_Helper.EncodeString(order)
        binary_payload += SDK_Helper.EncodeString(aoi_point)
        binary_payload += SDK_Helper.EncodeString(rename_parent)
        binary_payload += SDK_Helper.EncodeString(rename_children)
        binary_payload += SDK_Helper.EncodeInt(cluster_proximity)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SortAois')
        
        if response.status_code == 200:
            print(f"SortAois: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def SortDataTable(data_table_name, sort_columns_instead_of_rows, skip_zeroth_row_or_column, sory_by_arr, sort_order_is_rvs_array):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeBool(sort_columns_instead_of_rows)
        binary_payload += SDK_Helper.EncodeBool(skip_zeroth_row_or_column)
        binary_payload += SDK_Helper.EncodeIntArray(sory_by_arr)
        binary_payload += SDK_Helper.EncodeBoolArray(sort_order_is_rvs_array)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'SortDataTable')
        
        if response.status_code == 200:
            print(f"SortDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def StartContinuousMeasuring(capture_scheme_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(capture_scheme_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'StartContinuousMeasuring')
        
        if response.status_code == 200:
            print(f"StartContinuousMeasuring: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def StartPreview(exposure_time):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(exposure_time)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'StartPreview')
        
        if response.status_code == 200:
            print(f"StartPreview: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def StartScriptRecording():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'StartScriptRecording')
        
        if response.status_code == 200:
            print(f"StartScriptRecording: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def StartSpectrometerPreview(exposure_time, use_bracketing, auto_minimum_signal_percent):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeFloat(exposure_time)
        binary_payload += SDK_Helper.EncodeBool(use_bracketing)
        binary_payload += SDK_Helper.EncodeInt(auto_minimum_signal_percent)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'StartSpectrometerPreview')
        
        if response.status_code == 200:
            print(f"StartSpectrometerPreview: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def StopContinuousMeasuring():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'StopContinuousMeasuring')
        
        if response.status_code == 200:
            print(f"StopContinuousMeasuring: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def StopPreview():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'StopPreview')
        
        if response.status_code == 200:
            print(f"StopPreview: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def StopScriptRecording(script_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(script_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'StopScriptRecording')
        
        if response.status_code == 200:
            print(f"StopScriptRecording: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def StopSpectrometerPreview():
        binary_payload = b""
        # No parameters to encode
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'StopSpectrometerPreview')
        
        if response.status_code == 200:
            print(f"StopSpectrometerPreview: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def TextVar(rowId, table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(rowId)
        binary_payload += SDK_Helper.EncodeString(table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'TextVar')
        
        if response.status_code == 200:
            print(f"TextVar: Success")

            # Decode the response
            result = SDK_Helper.DecodeString(response.content)
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ThresholdMeasurement(measurement_name, apply_min_value, min_value, apply_max_value, max_value):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeBool(apply_min_value)
        binary_payload += SDK_Helper.EncodeFloat(min_value)
        binary_payload += SDK_Helper.EncodeBool(apply_max_value)
        binary_payload += SDK_Helper.EncodeFloat(max_value)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ThresholdMeasurement')
        
        if response.status_code == 200:
            print(f"ThresholdMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def ThresholdToSelection(measurement_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'ThresholdToSelection')
        
        if response.status_code == 200:
            print(f"ThresholdToSelection: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def THTVToXY(theta_H, theta_V):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeDouble(theta_H)
        binary_payload += SDK_Helper.EncodeDouble(theta_V)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'THTVToXY')
        
        if response.status_code == 200:
            print(f"THTVToXY: Success")

            # Decode the response
            result1 = SDK_Helper.DecodeDouble(response.content[:8])
            result2 = SDK_Helper.DecodeDouble(response.content[8:])
            return (result1, result2)

        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def TransformMeasurement(measurement_name, rotation_in_degrees, magnification_scalar, translation_x, translation_y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeDouble(rotation_in_degrees)
        binary_payload += SDK_Helper.EncodeDouble(magnification_scalar)
        binary_payload += SDK_Helper.EncodeDouble(translation_x)
        binary_payload += SDK_Helper.EncodeDouble(translation_y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'TransformMeasurement')
        
        if response.status_code == 200:
            print(f"TransformMeasurement: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def TransformMeasurementUsingDataTable(measurement_name, data_table_name, invalidate_values_outside_intersection):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        binary_payload += SDK_Helper.EncodeBool(invalidate_values_outside_intersection)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'TransformMeasurementUsingDataTable')
        
        if response.status_code == 200:
            print(f"TransformMeasurementUsingDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def TransposeDataTable(data_table_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(data_table_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'TransposeDataTable')
        
        if response.status_code == 200:
            print(f"TransposeDataTable: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def UnloadPackage(package_name):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(package_name)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'UnloadPackage')
        
        if response.status_code == 200:
            print(f"UnloadPackage: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def WriteToConsole(text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'WriteToConsole')
        
        if response.status_code == 200:
            print(f"WriteToConsole: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def WriteToMeasurementLog(measurement_name, text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeString(measurement_name)
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'WriteToMeasurementLog')
        
        if response.status_code == 200:
            print(f"WriteToMeasurementLog: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def WriteToSerialPort(serial_port_handle, text):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(serial_port_handle)
        binary_payload += SDK_Helper.EncodeString(text)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'WriteToSerialPort')
        
        if response.status_code == 200:
            print(f"WriteToSerialPort: Success")
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def XYToPolar(x, y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(x)
        binary_payload += SDK_Helper.EncodeInt(y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'XYToPolar')
        
        if response.status_code == 200:
            print(f"XYToPolar: Success")

            # Decode the response
            result1 = SDK_Helper.DecodeDouble(response.content[:8])
            result2 = SDK_Helper.DecodeDouble(response.content[8:])
            return (result1, result2)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")

    @staticmethod
    def XYToTHTV(x, y):
        binary_payload = b""
        binary_payload += SDK_Helper.EncodeInt(x)
        binary_payload += SDK_Helper.EncodeInt(y)
        
        # Send the binary payload using PM.SendApiRequest
        response = PM.SendApiRequest(binary_payload, 'XYToTHTV')
        
        if response.status_code == 200:
            print(f"XYToTHTV: Success")

            # Decode the response
            result1 = SDK_Helper.DecodeDouble(response.content[:8])
            result2 = SDK_Helper.DecodeDouble(response.content[8:])
            return (result1, result2)
        else:
            print(f"Request failed with status code: {response.status_code}")
            raise ValueError("Request failed")