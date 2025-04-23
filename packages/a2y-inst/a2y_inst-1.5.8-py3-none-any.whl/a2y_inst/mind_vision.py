from . import mvsdk
import numpy as _np


class CameraEnumerator:
	def __init__(self, max_count=1):
		self._camera_infos = mvsdk.CameraEnumerateDevice(max_count)

	def __getitem__(self, item):
		return self._camera_infos[item]

	def __len__(self):
		return len(self._camera_infos)


class Camera:
	def __init__(self, name):
		camera = mvsdk.CameraInitEx2(name)
		cap = mvsdk.CameraGetCapability(camera)
		mono_camera = (cap.sIspCapacity.bMonoSensor != 0)
		if mono_camera:
			mvsdk.CameraSetIspOutFormat(camera, mvsdk.CAMERA_MEDIA_TYPE_MONO8)
		mvsdk.CameraSetTriggerMode(camera, 0)
		mvsdk.CameraPlay(camera)
		frame_buffer_size = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax * (1 if mono_camera else 3)
		frame_buffer = mvsdk.CameraAlignMalloc(frame_buffer_size, 16)
		if frame_buffer is None:
			mvsdk.CameraStop(camera)
			mvsdk.CameraUnInit(camera)
			raise RuntimeError(f'Out of Memory: Fail to allocate frame buffer for Camera [{name}].')

		self._camera_handle = camera
		self._frame_buffer = frame_buffer

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

	def set_exposure_time(self, time_ms):
		mvsdk.CameraSetExposureTime(self._camera_handle, time_ms*1000)

	def get_exposure_time(self):
		time_us = mvsdk.CameraGetExposureTime(self._camera_handle)
		return int(time_us / 1000)

	def close(self):
		mvsdk.CameraStop(self._camera_handle)
		mvsdk.CameraUnInit(self._camera_handle)
		mvsdk.CameraAlignFree(self._frame_buffer)

	def _snap(self, timeout):
		camera = self._camera_handle
		frame_buffer = self._frame_buffer
		pRawData, FrameHead = mvsdk.CameraGetImageBuffer(camera, timeout)
		mvsdk.CameraImageProcess(camera, pRawData, frame_buffer, FrameHead)
		mvsdk.CameraReleaseImageBuffer(camera, pRawData)
		frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(frame_buffer)
		frame = _np.frombuffer(frame_data, dtype=_np.uint8)
		frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth, 1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3))
		return frame

	def snap(self, timeout: int = 1000, retry_count: int = 0):
		frame: _np.ndarray = None
		try_count = 0
		exception: Exception = None
		while try_count <= retry_count:
			try:
				frame = self._snap(timeout)
			except mvsdk.CameraException as e:
				exception = e
				try_count += 1
			else:
				break
		if frame is None:
			raise exception
		return frame

	def apply_configure_from_file(self, filename: str):
		mvsdk.CameraReadParameterFromFile(self._camera_handle, filename)
