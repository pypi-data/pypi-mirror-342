# -*- coding: utf-8 -*-
import winreg
import win32com.client
import win32process
import win32con, win32com, win32com.client, win32gui, win32api

import time, os, math, sys
import pyperclip, pywinauto
import chardet
import pygetwindow as gw
import psutil, subprocess
import ctypes

import xy_color
import xy_common
from ctypes import wintypes

from pywinauto import application
from unittest.mock import patch
with patch("ctypes.windll.user32.SetProcessDPIAware", autospec=True):
    import pyautogui

# POINT 구조체 정의
class POINT(ctypes.Structure):
	_fields_ = [("x", ctypes.c_long),
				("y", ctypes.c_long)]


class MONITORINFOEX(ctypes.Structure):
	_fields_ = [
		("cbSize", wintypes.DWORD),
		("rcMonitor", wintypes.RECT),
		("rcWork", wintypes.RECT),
		("dwFlags", wintypes.DWORD),
		("szDevice", wintypes.WCHAR * 32)
	]


# WINDOWPLACEMENT 구조체 정의
class WINDOWPLACEMENT(ctypes.Structure):
	_fields_ = [
		("length", wintypes.UINT),
		("flags", wintypes.UINT),
		("showCmd", wintypes.UINT),
		("ptMinPosition", wintypes.POINT),
		("ptMaxPosition", wintypes.POINT),
		("rcNormalPosition", wintypes.RECT)
	]


MDT_EFFECTIVE_DPI = 0


shcore = ctypes.windll.shcore
user32 = ctypes.windll.user32
GetDpiForMonitor = shcore.GetDpiForMonitor


# RECT 구조체 정의
class RECT(ctypes.Structure):
	_fields_ = [
		("left", wintypes.LONG),
		("top", wintypes.LONG),
		("right", wintypes.LONG),
		("bottom", wintypes.LONG)
	]


MonitorEnumProc = ctypes.WINFUNCTYPE(
	wintypes.BOOL,
	wintypes.HMONITOR,
	wintypes.HDC,
	ctypes.POINTER(RECT),
	wintypes.LPARAM
)


class xy_auto:
	"""
	마우스를 클릭하고 키보드를 자동으로 작동이 가능하게 만든 모듈

	파일이름 : xy_auto
	코드안에서 사용할때의 이름 : xauto
	객체로 만들었을때의 이름 : auto
	"""

	def __history(self):
		"""
		2024-09-11 : 전체적으로 유사한것들을 변경함
		"""
		pass
	def __init__(self):
		self.varx = xy_common.xy_common().varx
		self.colorx = xy_color.xy_color()

	def all_infomation_for_handle_no(self, handle_no):
		"""
		핸들 번호로 열려있는 프로그램일 경우, 일반 정보들을 돌려주는것

		:param handle_no:
		:return:
		"""
		result = {}
		if handle_no is not None:
			hwnd_title = win32gui.GetWindowText(handle_no)
			# 윈도우 클래스명 (개발 시점에 적용된 고유값이라고 보면 됨)
			hwnd_class_name = win32gui.GetClassName(handle_no)

			# 사용자가 볼 수 있는지 있는지 여부 (보이면 1, 안보이면 0)
			# (최소화된 상태라도) 사용자가 볼 수 있는 창이면 이 값은 1 임
			hwnd_is_visible = win32gui.IsWindowVisible(handle_no)

			# 좌표 정보
			result["pxywh"] = win32gui.GetWindowRect(handle_no)
			result["px"] = result["pxyxy"][0] # 만약 hwnd_rect_x 값이 -32000 이면 최소화된 상태라고 보면 됨
			result["py"] = result["pxyxy"][1] # 만약 hwnd_rect_y 값이 -32000 이면 최소화된 상태라고 보면 됨
			result["w"] = result["pxyxy"][2]
			result["title"] = hwnd_title
			result["class_name"] = hwnd_class_name
			result["is_visible"] = str(hwnd_is_visible)
			result["h"] = result["pxyxy"][3]
			result["h"] = result["pxyxy"][3]
			result["h"] = result["pxyxy"][3]

			print(result)
		return result

	def bring_window_to_front(self,pid):
		"""

		:param pid:
		:return:
		"""
		for window in gw.getWindowsWithTitle(""):
			if window._hWnd == pid:
				window.activate()
				break

	def calc_angled_xy_in_box(self, x, y, angle, width, height, status):
		"""
		사각 상자(width * height)안에서 x, y 좌표에서 angle의 각도로 이동하는 공의 다음위치를 계산하는 것
		만약 벽에 부딛히면, 입사각과 같은 반사각으로 다음위치를 계산해서 돌려주는 것이다

		:param x: 현재의 x
		:param y: 현재의 y
		:param angle: 각도
		:param width: 가로셀의 갯수
		:param height: 세로셀의 갯수
		:param status: 임의적으로 벽에 부뒷힌것으로 설정
		:return:
		"""
		angle_rad = math.radians(angle)
		# 이동 방향 설정
		dx = math.cos(angle_rad)
		dy = math.sin(angle_rad)
		# 새로운 위치 계산
		new_x = x + dx
		new_y = y + dy
		# 벽에 부뒷히면 반사
		if status == 1 or new_x >= width or new_x <= 1:
			dx = -dx
			#angle = math.degrees(math.atan2(dy, dx))
		if status == 1 or new_y >= height or new_y <= 1:
			dy = -dy
			#angle = math.degrees(math.atan2(dy, dx))
		# 새로운 위치 계산 (반사 후)
		new_x = x + dx
		new_y = y + dy
		# 새로운 각도 계산
		new_angle = math.degrees(math.atan2(dy, dx))
		status = 0
		return new_x, new_y, new_angle, status

	def calc_pixel_size_for_input_text_2(self, input_text, target_pixel, font_name="malgun.ttf", font_size=12, fill_char=" "):
		"""
		원하는 길이만큼 텍스트를 근처의 픽셀값으로 만드는것
		원래자료에 붙이는 문자의 픽셀값
		"""
		fill_px = self.calc_pixel_size_for_input_text_2(fill_char, font_size, font_name)[0]
		total_length =0
		for one_text in input_text:
			#한글자씩 필셀값을 계산해서 다 더한다
			one_length = self.calc_pixel_size_for_input_text_2(fill_char, font_size, font_name)[0]
			total_length = total_length + one_length

		# 원하는 길이만큼 부족한 것을 몇번 넣을지 게산하는것
		times = round((target_pixel - total_length)/fill_px)
		result = input_text + " "*times

		#최종적으로 넣은 텍스트의 길이를 한번더 구하는것
		length = self.calc_pixel_size_for_input_text_2(result, font_size, font_name)[0]

		#[최종변경문자, 총 길이, 몇번을 넣은건지]
		return [result, length, times]

	def check_input_action_key(self, input_value):
		"""
		키보드의 액션을 하기위해 사용해야할 용어를 확인하는 부분이다

		:param input_value:
		:return:
		"""
		input_value = str(input_value).lower()
		if input_value in self.varx["keyboard_action_list_all"]:
			result = input_value
		else:
			result = ""
		return result

	def click_mouse_with_type_times_interval(self, click_type="click", input_clicks=1, input_interval=0.25):
		"""

		:param click_type:
		:param input_clicks:
		:param input_interval:
		:return:
		"""
		pyautogui.click(button=click_type, clicks=input_clicks, interval=input_interval)

	def click_mouse_left_with_n_times(self, click_times = 1):
		"""
		왼쪽 마우스 버튼을 누르는 것

		:param click_times: 누르는 횟수
		:return:
		"""
		pyautogui.click(button="left", clicks= click_times)

	def click_mouse_left_down(self):
		"""
		왼쪽 마우스 버튼 눌른상태로 멈춤
		드리그등을 위한것
		"""
		pyautogui.mouseDown(button='left')

	def click_mouse_left_up(self):
		"""
		왼쪽 마우스 버튼 눌럿다 올린것
		"""
		pyautogui.mouseUp(button='left')

	def click_mouse_right_with_n_times(self, click_times = 1):
		"""
		오른쪽 마우스 클릭
		:param click_times:
		"""
		pyautogui.click(button="right", clicks=click_times)

	def click_mouse_right_down(self):
		"""
		오른쪽 마우스 눌름
		"""
		pyautogui.mouseDown(button='right')

	def click_mouse_right_up(self):
		"""
		오른쪽 마우스 올림
		:return:
		"""
		pyautogui.mouseUp(button='right')

	def copy_current_top_page(self):
		"""
		최상위의 프로그램을 전체를 선택하고 값을 복사하는 것

		:return:
		"""

		pyautogui.hotkey("ctrl", "a")
		pyautogui.hotkey("ctrl", "c")
		text_value = pyperclip.paste()
		return text_value

	def check_value_in_dic_key(self, input_dic, input_key):
		try:
			result = input_dic[input_key]
		except:
			result = False
		return result

	def get_monitor_rate_by_hwnd(self, hwnd):
		"""
		현재 모니터의 hwnd에 해당하는 모니터의 비율을 알려주는 것입니다

		:param hwnd:
		:return:
		"""
		all_inform_for_monitors = self.get_all_monitor_infomation()
		if self.is_in_primary_monitor(hwnd) == "first":
			result = all_inform_for_monitors[0]["rate"]
		else:
			result = all_inform_for_monitors[1]["rate"]
		return result

	def get_current_monitor_information(self, hwnd):
		"""
		모니터의 hwnd에 대한 정보들을 갖고오는 것

		:param hwnd:
		:return:
		"""
		all_inform_for_monitors = self.get_all_monitor_infomation()
		if self.is_in_primary_monitor(hwnd) == "first":
			result = all_inform_for_monitors[0]
		else:
			result = all_inform_for_monitors[1]
		return result

	def get_monitor_dpi_by_hwnd(self, hwnd):
		"""
		모니터의 hwnd에대한 dpi를 갖고오는 것이다

		:param hwnd:
		:return:
		"""
		all_inform_for_monitors = self.get_all_monitor_infomation()
		if self.is_in_primary_monitor(hwnd) == "first":
			result = all_inform_for_monitors[0]["dpi"][0]
		else:
			result = all_inform_for_monitors[1]["dpi"][0]
		return result

	def get_monitor_dpi_by_hwnd_01(self, monitor_hwnd):
		"""
		모니터의 hwnd에대한 dpi를 갖고오는 것이다

		:param monitor_hwnd:
		:return:
		"""
		dpi_x = ctypes.c_uint()
		dpi_y = ctypes.c_uint()
		result = GetDpiForMonitor(monitor_hwnd, MDT_EFFECTIVE_DPI, ctypes.byref(dpi_x), ctypes.byref(dpi_y))
		if result != 0:
			raise ctypes.WinError(result)
		return dpi_x.value, dpi_y.value

	def copy(self):
		"""
		현재 선택된 것을 복사하기
		"""
		pyautogui.hotkey('ctrl', "c")

	def data_for_keyboard_action_list_short(self):
		"""
		키보드 액션의 종류들
		:return:
		"""
		result = self.varx["keyboard_action_list_short"]
		return result

	def data_for_keyboard_action_list(self):
		"""
		키보드 액션의 종류들
		:return:
		"""
		result = self.varx["keyboard_action_list_all"]
		return result

	def dclick_mouse(self):
		"""
		double click
		:return:
		"""
		pyautogui.click(button="left", clicks=2, interval=0.25)

	def dclick_mouse_left_with_interval(self, interval_time=0.25):
		"""
		왼쪽 마우스 더블 클릭
		:param interval_time: 클릭 시간 간격
		:return:
		"""
		pyautogui.click(button="left", clicks=2, interval=interval_time)

	def dclick_mouse_right_with_interval(self, interval_time=0.25):
		"""
		오른쪽 마우스 더블 클릭
		:param interval_time:클릭 시간 간격
		:return:
		"""
		pyautogui.click(button="right", clicks=2, interval=interval_time)

	def drag_mouse_from_pxy1_to_pxy2(self, pxy1, pxy2, drag_speed=0.5):
		"""
		마우스 드레그

		:param pxy1:
		:param pxy2:
		:param drag_speed:
		:return:
		"""
		pyautogui.moveTo(pxy1[0], pxy1[1])
		pyautogui.dragTo(pxy2[0], pxy2[1], drag_speed)

	def drag_mouse_to_pwh(self, phw, drag_speed=0.5):
		"""
		현재 마우스위치에서 상대적인 위치인 pxy로 이동
		상대적인 위치의 의미로 width 와 height 의 개념으로 pwh 를 사용 duration 은 드레그가 너무 빠를때 이동하는 시간을 설정하는 것이다

		:param phw:
		:param drag_speed: 드레그 속도
		"""
		pyautogui.drag(phw[0], phw[1], drag_speed)

	def drag_mouse_to_pxy(self, pxy, drag_speed=0.5):
		"""
		현재 마우스위치에서 절대위치인 머이로 이동	duration 은 드레그가 너무 빠를때 이동하는 시간을 설정하는 것이다

		:param pxy:
		:param drag_speed: 드레그 속도
		"""
		pyautogui.dragTo(pxy[0], pxy[1], drag_speed)

	def draw_box_by_pxyxy(self, left, top, right, bottom, xcolor="red50"):
		"""
		윈도우에 박스크리기

		:param left:
		:param top:
		:param right:
		:param bottom:
		:param xcolor:
		:return:
		"""

		user32 = ctypes.windll.user32
		gdi32 = ctypes.windll.gdi32
		hwnd = user32.GetDesktopWindow()
		hdc = user32.GetDC(hwnd)  # 디바이스 컨텍스트 가져오기
		null_brush = gdi32.GetStockObject(5)  # 투명한 브러시 생성
		hex_color = self.colorx.change_xcolor_to_rgb(xcolor)
		red_pen = gdi32.CreatePen(0, 2, self.colorx.change_rgb_to_hex_rgb(hex_color[0],hex_color[1],hex_color[2]))  # 빨간색 펜 생성
		# 이전 브러시와 펜 저장
		old_brush = gdi32.SelectObject(hdc, null_brush)
		old_pen = gdi32.SelectObject(hdc, red_pen)
		# 빨간색 테두리 사각형 그리기
		gdi32.Rectangle(hdc, int(left), int(top), int(right), int(bottom))
		# 이전 브러시와 펜 복원
		gdi32.SelectObject(hdc, old_brush)
		gdi32.SelectObject(hdc, old_pen)
		# 펜 삭제
		gdi32.DeleteObject(red_pen)
		# 디바이스 컨텍스트 해제
		user32.ReleaseDC(hwnd, hdc)

	def get_all_child_window_hwnd_by_parent_hwnd(self, parent_hwnd):
		"""
		엑셀 창의 자식 윈도우(시트 영역) 핸들 가져오기

		:param parent_hwnd:
		:return:
		"""
		child_windows = []
		def callback(hwnd, lparam):
			child_windows.append(hwnd)
			return True
		win32gui.EnumChildWindows(parent_hwnd, callback, None)
		return child_windows

	def find_child_window(self, parent_hwnd, class_name):
		child_hwnds=[]
		def enum_child_proc(hwnd, lparam):
			if win32gui. GetClassName(hwnd) == class_name:
				child_hwnds.append(hwnd)
				return True

			win32gui.EnumChildWindows(parent_hwnd, enum_child_proc, None)
		return child_hwnds

	def focus_previous_window(self):
		global previous_window
		if previous_window:
			# pywinauto 를 사용하여 이전 윈도우에 포커스를 줌
			app = application.Application().connect(handle=previous_window._hWnd)
			app.window(handle=previous_window._hWnd).set_focus()

	def change_file_ecoding_type(self, path, filename, original_type="EUC-KR", new_type="UTF-8", new_filename=""):
		"""
		텍스트가 안 읽혀져서 확인해보니 인코딩이 달라서 안되어져서
		이것으로 전체를 변경하기위해 만듦

		:param path:
		:param filename:
		:param original_type:
		:param new_type:
		:param new_filename:
		:return:
		"""
		full_path = path + "\\" + filename
		full_path_changed = path + "\\" + new_filename + filename
		try:
			aaa = open(full_path, 'rb')
			result = chardet.detect(aaa.read())
			print(result['encoding'], filename)
			aaa.close()

			if result['encoding'] == original_type:
				print("화일의 인코딩은 ======> {}, 화일이름은 {} 입니다".format(original_type, filename))
				aaa = open(full_path, "r", encoding=original_type)
				file_read = aaa.readlines()
				aaa.close()

				new_file = open(full_path_changed, mode='w', encoding=new_type)
				for one in file_read:
					new_file.write(one)
				new_file.close()
		except:
			print("화일이 읽히지 않아요=====>", filename)

		path = "C:\Python39-32\Lib\site-packages\myez_xl\myez_xl_test_codes"
		file_lists = os.listdir(path)
		for one_file in file_lists:
			self.change_file_ecoding_type(path, one_file, "EUC-KR", "UTF-8", "_changed")

	def focus_at_pxy(self, original_xy, move_xy=[10, 10]):
		"""
		많이 사용하는 마우스와 키보드의 기능을 다시 만들어 놓은 것이다

		:param original_xy:
		:param move_xy:
		:return:
		"""
		pyautogui.moveTo(original_xy[0] + move_xy[0], original_xy[1] + move_xy[1])
		pyautogui.mouseDown(button='left')

	def focus_to_window_by_title(self, window_title="Excel.Application"):
		"""

		:param window_title:
		:return:
		"""
		window = gw.getWindowsWithTitle(window_title)
		print()
		if window.isActive == False:
			try:
				pywinauto.application.Application().connect(handle=window._hWnd).top_window().set_focus()
			except:
				print('No permission')

	def focus_by_handle_no(self, handle_no):
		"""
		특정 윈도우 핸들을 포커스/포커싱 처리하기

		:param handle_no:
		:return:
		"""
		result = False
		if handle_no is not None:
			while True:
				win32gui.ShowWindow(handle_no, 9) # 최소화 되어있을 경우 복원
				win32gui.SetForegroundWindow(handle_no)
				if str(handle_no) == str(win32gui.GetForegroundWindow()):
					break
				else:
					time.sleep(1)
			result = True
		return result

	def get_information_for_monitor(self):
		"""

		:return:
		"""
		result = []
		monitor = win32api.EnumDisplayMonitors()
		result = list()

		for info in monitor:
			# 주 모니터와 서브 모니터 구분
			if info[2][0] == 0 and info[2][1] == 0:
				monitorType = "주모니터"
			else:
				monitorType = "서브모니터"

			result.append({'type': monitorType, '모니터의 영역(왼쪽위, 오른쪽아래)': info[2]})

		result.append({'총모니터갯수': len(monitor)})
		return result

	def get_information_for_mouse(self):
		"""
		[(PyHANDLE:65537, PyHANDLE:0, (0, 0, 1920, 1080)), (PyHANDLE:65539, PyHANDLE:0, (-1920, 1, 0, 1081))]
		1 : 모니터의 핸들값
		2 : unknown
		3 : 위치와 해상도, ( left, top, width, height )
		0, 0 이 주모니터
		left : - 일 경우 주 모니터 왼쪽에 위치, 모니터가 상하로 위치할 경우 top 의 +- 로 판단

		:return:
		"""
		result = []
		pxy = self.get_pxy_for_mouse()
		result.append({"마우스의 현재 위치":pxy})
		monitors = win32api.EnumDisplayMonitors()

		for info in monitors:
			# 주 모니터와 서브 모니터 구분
			if info[2][0] == 0 and info[2][1] == 0:
				monitorType = "주모니터"
			else:
				monitorType = "서브모니터"

			if info[2][0] <= pxy[0] <= info[2][2] and info[2][1] <= pxy[1] <= info[2][3]:
				result.append({"모니터에서의 위치":monitorType})
				break

		return result

	def get_monitor_size(self):
		"""
		모니터의 해상도를 읽어오는 것

		:return:
		"""
		result = pyautogui.size()
		return result

	def get_pos_for_mouse(self):
		# 현재 마우스의 위치를 읽어온다
		result = win32api.GetCursorPos()
		return result

	def get_pxy_for_mouse(self):
		"""
		마우스 위치
		:return:
		"""
		pxy = pyautogui.position()
		return [pxy.x, pxy.y]

	def get_pxy_for_mouse_rev1(self):
		"""
		현재 마우스의 위치를 읽어온다

		:return:
		"""
		result = win32api.GetCursorPos()
		return result

	def get_center_pxy_for_selected_image(self, input_file_name):
		"""
		화면에서 저장된 이미지랑 같은 위치를 찾아서 돌려주는 것

		:param input_file_name:
		:return:
		"""
		button5location = pyautogui.locateOnScreen(input_file_name)
		center = pyautogui.center(button5location)
		return center

	def get_rgb_for_pxy_in_monitor(self, input_pxy=""):
		"""
		입력으로 들어오는 pxy위치의 rgb값을 갖고온다
		만약 "" 이면, 현재 마우스가 위치한곳의 rgb를 갖고온다
		:param input_pxy:
		:return:
		"""
		if input_pxy:
			x, y = input_pxy
		else:
			x, y = pyautogui.position()
		r, g, b = pyautogui.pixel(x, y)
		return [r,g,b]

	def get_screen_size(self):
		"""
		화면 사이즈

		:return:
		"""
		px =  win32api.GetSystemMetrics(0)
		py =  win32api.GetSystemMetrics(1)
		return [px, py]

	def get_xy_for_mouse(self, ):
		"""
		많이 사용하는 마우스와 키보드의 기능을 다시 만들어 놓은 것이다

		:return:
		"""
		xy = pyautogui.position()
		return (xy.x, xy.y)

	def get_hwnd_by_partial_title(self, input_text):
		"""
		현재 열려져있는 프로그램들의 제목을 가지고 handle을 구하는 것이며
		전체 이름이 아닌 일부분만 같아도 돌려주도록 한다

		:param input_text:
		:return:
		"""
		result = None
		all_data = self.get_title_n_hwnd_all_for_opened_windows()
		for title, handle_no in all_data:
			if str(input_text).lower() in str(title).lower():
				return [title, handle_no]
		return result

	def get_title_n_hwnd_all_for_opened_windows(self):
		"""
		현재 열려져있는 프로그램들의 제목과 윈도우핸들값을 구하는 것

		:return:
		"""
		def callback(hwnd, hwnd_list: list):
			title = win32gui.GetWindowText(hwnd)
			if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
				hwnd_list.append((title, hwnd))
			return True
		output = []
		win32gui.EnumWindows(callback, output)
		return output

	def get_hwnd_for_focused_program(self):
		"""
		현재 제일 앞부분에 활성화된 프로그램의 핸들값을 주는 것

		:return:
		"""
		result = win32gui.GetForegroundWindow()
		return result

	def get_process_id_for_focused_program(self):
		"""
		현재 제일 앞부분에 활성화된 프로그램의 process 번호를 돌려주는 것

		:return:
		"""
		process_id = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
		print(process_id)
		return process_id

	def get_all_running_process_id(self):
		"""
		현재 윈도우 화면에 있는 프로세스 목록 리스트를 반환한다.
		리스트의 각 요소는 element 객체로 프로세스 id, 핸들값, 이름 등의 정보를 보유한다.

		:return:
		"""
		result = []
		procs = pywinauto.findwindows.find_elements()
		for proc in procs:
			result.append([proc, proc.process_id])
		return result

	def get_all_installed_program_id(self):
		"""
		현재 컴퓨터안에 설치된 모든 프로그램의 ID

		:return:
		"""
		result = []
		try:
			# 레지스트리 키 열기
			key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "")
			i = 0
			while True:
				try:
					# 레지스트리 키 열거
					subkey_name = winreg.EnumKey(key, i)
					i += 1
					# ProgID는 일반적으로 '.'을 포함하지 않음
					# #if '.' not in subkey_name:
					result.append(subkey_name)
				except OSError:
					break
		except Exception as e:
			print(f"Error: {e}")
		return result

	def get_all_information_for_all_working_program(self):
		"""
		모든 실행중인 프로그램에대한 정보를 사전형으로 갖고온다

		:return:
		"""
		result = []
		programs = gw.getWindowsWithTitle("")
		for one in programs:
			dic_data =self.get_information_for_program_as_dic(one)
			result.append(dic_data)
		return result

	def get_all_information_for_titled_working_program_(self):
		"""
		제목이있는것들만 돌려주는 것

		:return:
		"""
		result = []
		programs = gw.getWindowsWithTitle("")
		for one in programs:
			dic_data =self.get_information_for_program_as_dic(one)
			if dic_data["title"]:
				result.append(dic_data)
		return result

	def set_maximize_by_program_title(self, input_title):
		"""
		제목이있는것들만 돌려주는 것

		:param input_title:
		:return:
		"""
		result = []
		programs = gw.getWindowsWithTitle("")
		for one_program in programs:
			dic_data =self.get_information_for_program_as_dic(one_program)
			if str(input_title).lower() in str(dic_data["title"]).lower():
				one_program.maximize()
		return result

	def get_information_for_hwnd(self, input_hwnd):
		"""
		프로그램의 hwnd 로 정보를 찾는것

		:param input_hwnd:
		:return:
		"""
		result = self.get_program_information_by_key_n_value("hwnd", input_hwnd)
		return result

	def get_program_information_by_title(self, input_title):
		"""
		프로그램의 제목으로 정보를 찾는것

		:param input_title:
		:return:
		"""
		result = self.get_program_information_by_key_n_value("title", input_title)
		return result

	def get_program_information_by_key_n_value(self, input_key, input_value):
		"""
		프로그램의 제목으로 정보를 찾는것

		:param input_key:
		:param input_value:
		:return:
		"""
		programs = gw.getWindowsWithTitle("")
		result =[]
		for one in programs:
			dic_data =self.get_information_for_program_as_dic(one)
			if str(input_value).lower() in str(dic_data[input_key]).lower():
				result.append(dic_data)
		return result

	def get_all_title_for_working_program(self, ):
		"""
		현재 활성화된 윈도우 리스트를 가져옴

		:return:
		"""
		programs = gw.getWindowsWithTitle('')
		return programs

	def get_process_name_by_pid(self, pid):
		"""
		pid값으로 프로세스 이름을 갖고오는 것

		:param pid:
		:return:
		"""
		try:
			process = psutil.Process(pid)
			return process.name()
		except psutil.NoSuchProcess:
			return None

	def get_pid_from_hwnd(self, hwnd):
		"""
		핸들값으로 pid값을 구하는 것

		:param hwnd:
		:return:
		"""
		pid = ctypes.wintypes.DWORD()
		# WinAPI 함수 정의
		user32 = ctypes.WinDLL('user32', use_last_error=True)
		user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
		return pid.value

	def get_information_for_program_as_dic(self, input_program):
		"""
		현재 활성화된 윈도우 리스트를 가져옴

		:param input_program:
		:return:
		"""
		result = {}
		result["ismaximised"] = input_program.isMaximized
		result["isminimized"] = input_program.isMinimized
		result["isvisible"] = input_program.visible
		result["hwnd"] = input_program._hWnd
		result["pid"] = self.get_pid_from_hwnd(result["hwnd"])
		result["process_name"] = self.get_process_name_by_pid(result["pid"])
		result["title"] = input_program.title
		return result

	def get_next_window(self):
		"""
		현재 활성화된 윈도우 리스트를 가져온

		:return:
		"""
		windows = gw.getWindowsWithTitle("")
		active_window = gw.getActiveWindow()
		if active_window:
			active_index = windows.index(active_window)
			# 다음으로 포커스를 받을 윈도우를 찾음
			next_window = None
			for i in range(active_index + 1, len(windows)):
				if windows[i].visible:
					next_window = windows[i]
					break
			if not next_window:
				for i in range(0, active_index):
					if windows[i].visible:
						next_window = windows[i]
						break
			return next_window
		return None

	def get_program_name_by_hwnd(self, input_hwnd):
		# 현재 활성화된 윈도우 리스트를 가져옴
		result = {}
		result["pid"] = self.get_pid_from_hwnd(input_hwnd)
		result["process_name"]=self.get_process_name_by_pid(result["pid"])
		return result

	def get_previous_window(self, ):
		# 현재 활성화된 윈도우 리스트를 가져옴
		windows = gw.getWindowsWithTitle("") #결과 print(windows)
		if len(windows) > 1:
			return windows[1]

	def get_all_title_n_hwnd_for_opened_windows(self, ):
		#현재 열려져있는 프로그램들의 제목과 윈도우핸들값을 구하는 것
		def callback(hwnd, hwnd_list: list):
			title = win32gui. GetWindowText(hwnd)
			if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
				hwnd_list.append((title, hwnd))
			return True
		output = []
		win32gui.EnumWindows(callback, output)
		return output

	def get_hwnd_from_pid(self, pid):
		"""

		:param pid:
		:return:
		"""
		hwnd_list = []
		def callback(hwnd, hwnd_list):
			_, found_pid = win32process.GetWindowThreadProcessld(hwnd)
			if found_pid == pid and  win32gui.isWindowVisible(hwnd):
				hwnd_list.append(hwnd)
			return True

		win32gui.EnumWindows(callback, hwnd_list)
		return hwnd_list

	def get_text_for_next_program(self):
		aa = self.get_next_window()
		bb = self.get_information_for_program_as_dic(aa)
		self.set_top_window_by_hwnd(bb["hwnd"])
		result = self.copy_current_top_page()
		return result

	def get_system_dpi(self):
		# 사용자 32.dl 에서 GetDpiForSystem 함수를 호출하여 시스템 DP| 값을 가져옵니다.
		try:
			## Windows 10 버전 1703 이상에서 사용 가능
			dpi = ctypes.windll.user32.GetDpiForSystem()
		except AttributeError:
			## Windows 10 버전 1703 미만에서는 GetDevicecaps 함수를 사용하여 DP| 값을 가져옵니다.
			hdc = ctypes.windll.user32.GetDC(0)
			dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
			#88은 LOGPIXELSX 상수입니다
			ctypes.windll.user32.ReleaseDC(0, hdc)
		return dpi

	def write_formula_bar_text_in_excel(self, excel_hwnd, text):
		# 엑셀에는 여러개의 하부 클래스들이 존재한다 그 클래스중에서 수식입력창을 갖고와서 값을 넣는 방법을 보여준다
		app = pywinauto.Application().connect(handle=excel_hwnd)
		excel_window = app.window(handle=excel_hwnd)
		child_class_name = "EXCEL<"
		child_window = excel_window.child_window(class_name=child_class_name)
		if not child_window.exists():
			print("Formula bar window not found.")
			return
		child_window.set_focus()
		child_window.type_keys(text, with_spaces=True)

	def get_hwnd_for_top_window(self):
		# 최상위 윈도우의 hwnd를 갖는 것
		result = ctypes.windll.user32.GetDesktopWindow()
		return result

	def set_maximize_for_hwnd(self, hwnd):
		"""
		입력으로 들어오는 hwnd의 어플리케이션이 최대화인지를 확인하는 것
		창이 최대화되어 있는지 확인
		:param hwnd:
		:return:
		"""
		placement = WINDOWPLACEMENT()
		placement.length = ctypes.sizeof(WINDOWPLACEMENT)
		ctypes.windll.user32.GetWindowPlacement(hwnd, ctypes.byref(placement))
		return placement.showCmd == 3  # SW_SHOWMAXIMIZED

	def get_hwnd_by_pid(self, pid):
		"""

		:param pid:
		:return:
		"""
		hwnd_list = []
		def callback(hwnd, hwnd_list):
			_, found_pid = win32process.GetWindowThreadProcessld(hwnd)
			if found_pid == pid and  win32gui.isWindowVisible(hwnd):
				hwnd_list.append(hwnd)
			return True

		win32gui.EnumWindows(callback, hwnd_list)
		return hwnd_list

	def get_all_hwnd(self):
		result = []
		for window in gw.getWindowsWithTitle(""):
			result.append(window._hWnd)
		return result

	def get_information_for_all_program(self):
		result = []
		for window in gw.getWindowsWithTitle(""):
			temp = {}
			temp["hwnd"] = window._hWnd
			temp["title"] = window.title
			temp["visible"] = win32gui.isWindowVisible(window._hWnd)
			result.append(temp)
		return result

	def get_all_hwnd_for_visible_program_by_zorder(self):
		# Z-order 순서대로 윈도우 핸들을 갖고오는 것
		user32api = ctypes.windll.user32
		result = []
		hwnd = user32api.GetTopWindow(None)
		while hwnd:
			if user32api.IsWindowVisible(hwnd):
				result.append(hwnd)
			hwnd = user32api.GetWindow(hwnd, 2)
		return result

	def get_all_installed_package_list(self):
		"""
		현재 설치된 패키지의 목록을 버전과 함께 돌려주는 것이다
		:return:
		"""
		result = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True, check=True)
		temp = result.stdout
		lines = temp.strip().split('\n')
		result = []
		for one_line in lines[2:]:
			temp2 = str(one_line).strip().split(" ")
			result.append([temp2[0], temp2[-1]]) #[패키지이름, 버전]
		return result

	def get_virtual_screen_size(self):
		"""시스템의 가상 화면 크기를 반환합니다."""
		width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
		height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
		return width, height

	def get_primary_screen_size(self):
		"""주 모니터의 크기를 반환합니다."""
		width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
		height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
		return width, height

	def get_all_monitor_infomation(self):
		"""
		모든 모니터에대한 모든 정보를 사전의 형태로 돌려주는 것
		:return:
		"""
		monitors = []

		def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
			monitors.append(hMonitor)

			return True

		MonitorEnumProc = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HMONITOR, wintypes.HDC, ctypes.POINTER(wintypes.RECT),
											 ctypes.c_double)
		user32.EnumDisplayMonitors(None, None, MonitorEnumProc(monitor_enum_proc), 0)
		result = []

		for monitor in monitors:
			info = {}
			monitor_info = MONITORINFOEX()
			info["dpi"] = self.get_monitor_dpi_by_hwnd(monitor)
			monitor_info.cbSize = ctypes.sizeof(monitor_info)
			user32.GetMonitorInfoW(monitor, ctypes.byref(monitor_info))
			info['Monitor'] = (monitor_info.rcMonitor.left, monitor_info.rcMonitor.top, monitor_info.rcMonitor.right,
							   monitor_info.rcMonitor.bottom)
			info['Work'] = (
			monitor_info.rcWork.left, monitor_info.rcWork.top, monitor_info.rcWork.right, monitor_info.rcWork.bottom)

			scale_x = info["dpi"][0] / 96.0
			scale_y = info["dpi"][1] / 96.0
			info['scale'] = [scale_x, scale_y]

			actual_width = (info['Monitor'][2] - info['Monitor'][0]) / scale_x
			actual_height = (info['Monitor'][3] - info['Monitor'][1]) / scale_y

			info['actual_resolution'] = [actual_width, actual_height]
			info['is_in_program'] = False
			if len(result) == 0:
				info['rate'] = 1
			else:
				info['rate'] = actual_width / result[0]["actual_resolution"][0]
			result.append(info)
		return result

	def get_primary_monitor_info(self):
		"""
		현재 자신의 모니터가 여러개일때 주모니터에 대한 정보들을 돌려주는 것
		:return:
		"""

		user32 = ctypes.windll.user32
		monitor_info = MONITORINFOEX()
		monitor_info.cbSize = ctypes.sizeof(MONITORINFOEX)
		primary_monitor = user32.MonitorFromWindow(user32.GetDesktopWindow(), 1)
		user32.GetMonitorInfoW(primary_monitor, ctypes.byref(monitor_info))
		return monitor_info

	def get_dpi(self):
		"""
		현재 장치의 dpi를 구하는 코드

		:return:
		"""
		hdc = ctypes.windll.user32.GetDC(0)
		dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88) #LOGPIXELSX
		ctypes.windll.user32.ReleaseDC(0, hdc)
		return dpi

	def get_pxyxy_for_program_hwnd(self, hwnd):
		"""
		프로그램의 윈도우 좌표를 갖고오는 것
		어떤 프로그램의 핸들을 넣으면 윈도우의 좌표를 돌려준다

		:param hwnd:
		:return:
		"""
		rect = win32gui.GetWindowRect(hwnd)
		return rect

	def get_pxyxy_for_excel_hwnd(self, hwnd):
		"""

		:param hwnd:
		:return:
		"""
		# RECT 구조체를 정의합니다
		rect = wintypes.RECT()
		# GetWindowRect 함수를 사용하여 창의 위치와 크기를 가져옵니다.
		ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
		return rect.left, rect.top, rect.right - rect.left, rect.bottom-rect.top

	def get_excel_pid(self):
		"""

		:return:
		"""
		for proc in psutil.process_iter(['pid', 'name']):
			print(proc.info['name'])
			if proc.info['name'] == "EXCEL.EXE":
				return proc.info['pid']
		return None

	def is_com_accessible_for_program_id(self, prog_id):
		"""
		현재 열려있는 프로그램중에서 win32com의 가상 함수가 있는것을 확인하는 것

		:param prog_id:
		:return:
		"""
		try:
			# COM 객체 생성 시도
			app = win32com.client.GetActiveObject(prog_id)
			print("win32com 적용가능 => ", prog_id)
		except:
			return False

	def is_in_primary_monitor(self, hwnd):
		"""
		현재 모니터의 hwnd가 오면, 그것이 주모니터인지를 확인해 주는 것

		:param hwnd:
		:return:
		"""
		class RECT(ctypes.Structure):
			_fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

		# RECT 구조체를 정의합니다
		rect = RECT()
		# GetWindowRect 함수를 사용하여 창의 위치와 크기를 가져옵니다.
		ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
		x1, y1, x2, y2 = rect.left, rect.top, rect.right, rect.bottom

		# 중간지점의 x좌표를 기준으로 주모니터인지 아닌지를 판단하자
		primary_monitor_info = self.get_primary_monitor_info()
		primary_monitor_rect = primary_monitor_info.rcMonitor
		if primary_monitor_rect.left <= int(x2 + x1) / 2 <= primary_monitor_rect.right:
			result = "first"
		else:
			result = "second"
		return result

	def check_maximized_by_program_hwnd(self, hwnd):
		"""
		입력으로 들어오는 hwnd의 어플리케이션이 최대화인지를 확인하는 것
		창이 최대화되어 있는지 확인
		:param hwnd:
		:return:
		"""
		placement = WINDOWPLACEMENT()
		placement.length = ctypes.sizeof(WINDOWPLACEMENT)
		ctypes.windll.user32.GetWindowPlacement(hwnd, ctypes.byref(placement))
		return placement.showCmd == 3  # SW_SHOWMAXIMIZED

	def click_mouse(self, x, y):
		"""
		좌표로 이동해서 마우스 왼쪽을 클릭
		mouse_click(300, 300)

		:param x:
		:param y:
		:return:
		"""
		win32api.SetCursorPos((x, y))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

	def minimize_and_focus_next(self):
		active_window = gw.getActiveWindow()
		next_window = self.get_next_window()
		if active_window:
			# 현재 활성화된 윈도우를 최소화
			active_window.minimize()
			time.sleep(0.5) # 최소화가 완료될 때까지 잠시 대기

		if next_window: # 다음 윈도우에 포커스를 줌
			app = application.Application().connect(handle=next_window._hWnd)
			app.window(handle=next_window._hWnd).set_focus()

	def move_cursor(self, direction, press_times = 1):
		"""
		마우스커서를 기준으로 이동하는것

		:param direction:
		:param press_times:
		:return:
		"""
		for no in range(press_times):
			pyautogui.press(direction)

	def move_mouse_to_pos(self, xy_list):
		"""
		원하는 위치로 마우스를 이동시킨다

		:param xy:
		:return:
		"""
		pos = (xy_list[0], xy_list[1])
		win32api.SetCursorPos(pos)

	def move_mouse_to_pwh_as_delta(self, pwh):
		"""
		마우스의 위치를 이동시킨다

		:param pwh:
		:return:
		"""
		pyautogui.move(pwh[0], pwh[1])

	def move_mouse_to_pxy(self, pxy):
		"""
		마우스의 위치를 이동시킨다

		:param pxy:
		:return:
		"""
		pyautogui.moveTo(pxy[0], pxy[1])

	def move_mouse_xy_as_delta(self, x1, y1):
		"""
		move_mouse_xy
		현재있는 위치에서 x1, y1만큼 이동

		:param x1:
		:param y1:
		:return:
		"""
		pyautogui.move(x1, y1)

	def move_screen_by_scroll(self, input_no):
		"""
		현재 위치에서 상하로 스크롤하는 기능 #위로 올리는것은 +숫자，내리는것은 -숫자로 사용

		:param input_no:
		:return:
		"""
		pyautogui.scroll(input_no)

	def move_xy_by_degree_n_distance(self, degree, distance):
		"""
		move_degree_distance( degree="입력필요", distance="입력필요")
		현재 위치 x,y에서 30도로 20만큼 떨어진 거리의 위치를 돌려주는 것
		메뉴에서 제외

		:param degree:
		:param distance:
		:return:
		"""
		degree = degree * (3.141592 / 180)
		y = distance * math.cos(degree)
		x = distance * math.sin(degree)
		return [x, y]

	def paste(self):
		"""
		복사후 붙여넣기

		:return:
		"""
		pyautogui.hotkey('ctrl', "v")

	def paste_clipboard_data(self):
		"""
		클립보드에 저장된 텍스트를 붙여넣습니다.

		:return:
		"""
		pyperclip.paste()

	def paste_text_from_clipboard(self):
		"""
		클립보드에서 입력된 내용을 복사를 하는 것이다

		:return:
		"""
		result = pyperclip.paste()
		return result

	def popup_for_input(self, button_list):
		"""
		메세지박스의 버튼을 만드는 것

		:param button_list:
		:return:
		"""
		press_button_name = pyautogui.confirm('Enter option', buttons=['A', 'B', 'C'])
		return press_button_name

	def popup_for_input_with_password_style(self, input_text, input_title="", input_default_text =""):
		"""
		메세지박스 : 암호 입력용
		:param input_text:
		:param input_title:
		:param input_default_text:
		:return:
		"""
		a = pyautogui.password(text=input_text, title=input_title, default=input_default_text, mask='*')
		print(a)

	def popup_for_show_message(self):
		"""

		:return:
		"""
		pyautogui.alert(text='내용입니다', title='제목입니다', button='OK')

	def popup_for_show_message_box(self, input_text, input_title="", input_default_text =""):
		"""
		일반 메세지 박스

		:param input_text:
		:param input_title:
		:param input_default_text:
		:return:
		"""
		a = pyautogui.prompt(text=input_text, title=input_title, default=input_default_text)
		print(a)

	def press_key_down(self, one_key):
		"""
		어떤키의 키보드를 눌름

		:param one_key:
		:return:
		"""
		pyautogui.keyDown(one_key)

	def press_key_up(self, one_key):
		"""
		어떤키의 키보드를 눌렀다 땜

		:param one_key:
		:return:
		"""
		pyautogui.keyUp(one_key)

	def press_one_key(self, input_key="enter"):
		"""
		기본적인 키를 누르는 것을 설정하는 것이며
		기본값은 enter이다
		press의 의미는 down + up이다

		:param input_key:
		:return:
		"""
		pyautogui.press(input_key)

	def save(self):
		"""
		저장하기

		:return:
		"""
		pyautogui.hotkey('ctrl', "s")

	def screen_capture(self, file_name="D:Wtemp_101.jpg"):
		"""
		스크린 캡쳐를 해서, 화면을 저장하는 것

		:param file_name:
		:return:
		"""
		pyautogui.screenshot(file_name)
		return file_name

	def screen_capture_with_file_name_n_size(self, file_name, pxyxy):
		"""
		화면캡쳐를 지정한 크기에서 하는것

		:return:
		"""
		region_data = (pxyxy[0], pxyxy[1], pxyxy[2], pxyxy[3])
		im3 = pyautogui.screenshot(file_name, region=region_data)

	def screen_capture_for_full_screen(self, input_full_path=""):
		"""
		스크린샷

		:param input_full_path:
		:return:
		"""
		result = pyautogui.screenshot()
		if input_full_path:
			result.save(input_full_path)
		return result

	def screen_capture_with_pxywh(self, input_pxywh, input_full_path=""):
		"""
		스크린샷

		:param input_pxywh:
		:param input_full_path:
		:return:
		"""
		x,y,w,h  = input_pxywh
		result = pyautogui.screenshot(region=(x,y,w,h))
		if input_full_path:
			result.save(input_full_path)
		return result

	def scroll_screen_by_click_num(self, input_no):
		"""
		현재 위치에서 상하로 스크롤하는 기능 #위로 올리는것은 +숫자，내리는것은 -숫자로 사용

		:param input_no:
		:return:
		"""
		pyautogui.scroll(input_no)

	def scroll_mouse_down(self, input_click_count=10):
		"""
		scroll down 10 "clicks"

		:param input_click_count:
		:return:
		"""
		pyautogui.scroll(input_click_count*-1)

	def scroll_mouse_up(self, input_click_count=10):
		"""
		scroll up 10 "clicks"

		:param input_click_count:
		:return:
		"""
		pyautogui.scroll(input_click_count)

	def search_same_position_for_input_picture_in_monitor(self, input_file_path):
		"""
		화면에서 같은 그림의 위치 찾기

		:param input_file_path:
		:return:
		"""
		result = []
		for pos in pyautogui.locateAllOnScreen(input_file_path):
			result.append(pos)
		return result

	def search_same_position_for_input_picture_in_monitor_by_gray_scale(self, input_file_path):
		"""
		그레이 스케일로 변경해서 찾기

		:param input_file_path:
		:return:
		"""
		result = []
		for pos in pyautogui.locateAllOnScreen(input_file_path, grayscale=True):
			result.append(pos)
		return result

	def search_center_of_same_position_for_input_picture_in_monitor(self, input_picture):
		"""
		화면위에서 들어온 그림의 위치를 찾아서 중간 위치를 알려주는 것

		:param input_picture:
		:return:
		"""

		pxywh = pyautogui.locateOnScreen(input_picture)
		pxy = pyautogui.center(pxywh)
		result = [pxy[0], pxy[1]]
		return result

	def select_from_curent_cursor(self, direction, press_times):
		"""
		현재위치에서 왼쪽이나 오른쪽으로 몇개를 선택하는 것

		:param direction:
		:param press_times:
		:return:
		"""
		pyautogui.keyDown("shift")
		for one in range(press_times):
			self.press_key_down(direction)
		pyautogui.keyUp("shift")

	def set_top_window_by_hwnd(self, input_hwnd):
		"""
		hwnd 값으로 프로그램을 최상위로 올리는것

		:param input_hwnd:
		:return:
		"""
		win32gui.SetForegroundWindow(input_hwnd)
		win32gui.BringWindowToTop(input_hwnd)

	def type_hotkey_n_char(self, input_hotkey, input_key):
		"""
		pyautogui.hotkey('ctrl', 'c') ==> ctrl-c to copy

		:param input_hotkey:
		:param input_key:
		:return:
		"""
		pyautogui.hotkey(input_hotkey, input_key)

	def type_action_key(self, action='enter', times=1, input_interval=0.1):
		"""
		키타이핑

		:param action:
		:param times:
		:param input_interval:
		:return:
		"""
		pyautogui.press(action, presses=times, interval=input_interval)

	def type_letter(self, input_text):
		"""
		암호나 글자를 입력하는 데 사용하는것이다
		이것은 대부분 마우스를 원하는 위치에 옮기고, 클릭을 한번한후에 사용하는것이 대부분이다
		그저 글자를 타이핑 치는 것이다
		"""
		pyperclip.copy(input_text)
		pyautogui.hotkey("ctrl", "v")

	def type_delete_n_times(self, input_no = 1000):
		"""
		현재위치에서 자료를 지우는것
		최대 한줄의 자료를 다 지워서 x 의 위치가 변거나 textbox 안의 자료가 다지워져 위치이동이 없으면 종료

		:return:
		"""
		for no in range(0, int(input_no)):
			position = pyautogui.position()
			pxy_old = [position.x, position.y]
			pyautogui.press('delete')
			position = pyautogui.position()
			pxy_new = [position.x, position.y]
			if pxy_old == pxy_new or pxy_old[1] != pxy_new[1]:
				break

	def type_backspace_n_times(self, input_no = 10):
		"""
		현재위치에서 자료를 지우는것
		죄대 한줄의 자료를 다 지워서 x 의 위지가 변거나 textbox 안의 자료가 다지워져 위지이동이 없으면 종료

		:param input_no:
		:return:
		"""
		for no in range(0, input_no):
			pyautogui.press('backspace')
			time.sleep(0.2)

	def type_ctrl_n_char(self, input_char):
		"""
		ctrl + 키를 위한것

		:param input_text:
		:return:
		"""
		pyautogui.hotkey('ctrl', input_char)

	def type_arrow_key_with_n_times(self, input_char, n_times = 1, interval=None):
		"""
		방향키를 n번 누르는것

		:param input_char:
		:return:
		"""
		base_data = {"left":"left", "왼쪽":"left", "right":"right", "오른쪽":"right", "up":"up", "위":"up", "down":"down", "아래":"down", }
		checked_char = base_data[input_char]
		for num in range(n_times):
			if not interval:
				time.sleep(interval)
			pyautogui.press(checked_char)  # press the left arrow key

	def type_text_with_interval(self, input_text, input_interval=0.1):
		"""
		그저 글자를 타이핑 치는 것이다
		pyautogui.pressfenter', presses=3z interval=3) # enter 키를 3 초에 한번씩 세번 입력합니다.

		:param input_text:
		:param input_interval:
		:return:
		"""
		#pyautogui.typewrite(input_text, interval=input_interval)

		for one_letter in input_text:
			time.sleep(input_interval)
			pyperclip.copy(one_letter)
			pyautogui.hotkey("ctrl", "v")

	def type_text_for_hangul(self, input_text):
		"""
		영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		pyautogui 가 unicode 는 입력이 안됩니다

		:param input_text:
		:return:
		"""
		pyperclip.copy(input_text)
		pyautogui.hotkey('ctrl', "v")

	def type_text_one_by_one(self, input_text):
		"""
		영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		어떤경우는 여러개는 않되어서 한개씩 들어가는 형태로 한다

		:param input_text:
		:return:
		"""
		for one_letter in input_text:
			pyperclip.copy(one_letter)
			pyautogui.hotkey("ctrl", "v")

	def type_2_key(self, input_key1, input_key2):
		"""

		:param input_key1:
		:param input_key2:
		:return:
		"""
		win32api.keybd_event(self.key_dic[str(input_key1).lower()], 0, 0, 0)
		win32api.keybd_event(self.key_dic[str(input_key2).lower()], 0, 0, 0)
		time.sleep(0.1)
		win32api.keybd_event(self.key_dic[str(input_key2).lower()], 0, 2, 0) # 2: key_up
		win32api.keybd_event(self.key_dic[str(input_key1).lower()], 0, 2, 0) # 2: key_up

	def write_text_at_cursor(self, input_text):
		"""
		암호나 글자를 입력하는 데 사용하는것이다
		이것은 대부분 마우스를 원하는 위치에 옮기고, 클릭을 한번한후에 사용하는것이 대부분이다
		그저 글자를 타이핑 치는 것이다
		"""
		time.sleep(1)
		pyperclip.copy(input_text)
		pyautogui.hotkey("ctrl", "v")

	def write_text_at_previous_window(self, input_text ="가나다라abcd$^&*", start_window_no=1, next_line = 0):
		"""
		바로전에 활성화 되었던 윈도우에 글씨 써넣기

		:param input_text:
		:param start_window_no:
		:param next_line:
		:return:
		"""
		window_list = []
		for index, one in enumerate(gw.getAllTitles()):
			if one:
				window_list.append(one)
		previous_window = gw.getWindowsWithTitle(window_list[start_window_no])[0]
		previous_window.activate()
		if next_line==1:
			self.type_text_for_hangul(input_text)
			pyautogui.press('enter')
		else:
			self.type_text_for_hangul(input_text)

