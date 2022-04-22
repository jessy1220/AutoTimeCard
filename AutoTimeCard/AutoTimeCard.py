from msilib.schema import RadioButton
import os
import tkinter as tk
import time
from tkinter import messagebox
from datetime import datetime
from threading import Timer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

try:
  from msedge.selenium_tools import Edge, EdgeOptions
except ImportError:
  print ("Trying to Install required module: selenium\n")
  os.system('py -3 -m pip install msedge_selenium_tools')
  from msedge.selenium_tools import Edge, EdgeOptions

CurrentPath = os.path.dirname(os.path.abspath(__file__))
TimerCardInList = list()
TimerCardOutList = list()

def ConnectVPN():
  os.chdir("C:\\Program Files (x86)\\Common Files\\Pulse Secure\\Integration")
  os.system("pulselauncher.exe -url https://vpn.insyde.com -u " + User_entry.get() + " -p " + Pw_entry.get() + " -r Insyde")

def disconnectVPN():
  os.system("pulselauncher.exe -stop")

def TimeCardIn(browser):
  browser.get('https://eas2.insyde.com/ehrportal/LoginFOrginal.asp')
  wait = WebDriverWait(browser, 3)
  input = wait.until(EC.presence_of_element_located(
      (By.XPATH, '//*[@name="username"]')))
  input.send_keys(User_entry.get())
  input = wait.until(EC.presence_of_element_located(
      (By.XPATH, '//*[@name="password"]')))
  input.send_keys(Pw_entry.get())
  login = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@name="imageField"]')))
  login.click()
  browser.switch_to.window(browser.window_handles[-1])
  browser.close()
  browser.switch_to.window(browser.window_handles[0])
  browser.get('https://eas2.insyde.com:443/ehrportal//DEPT/Personal_CardData_Default.asp')
  browser.find_element_by_css_selector("input[name='radiobutton'][type='radio'][value='0']").click()
  submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@name="Submit2"]')))
  submit.click()
  
def TimeCardOut(browser):
  browser.get('https://eas2.insyde.com/ehrportal/LoginFOrginal.asp')
  wait = WebDriverWait(browser, 3)
  input = wait.until(EC.presence_of_element_located(
      (By.XPATH, '//*[@name="username"]')))
  input.send_keys(User_entry.get())
  input = wait.until(EC.presence_of_element_located(
      (By.XPATH, '//*[@name="password"]')))
  input.send_keys(Pw_entry.get())
  login = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@name="imageField"]')))
  login.click()
  browser.switch_to.window(browser.window_handles[-1])
  browser.close()
  browser.switch_to.window(browser.window_handles[0])
  browser.get('https://eas2.insyde.com:443/ehrportal//DEPT/Personal_CardData_Default.asp')
  browser.find_element_by_css_selector("input[name='radiobutton'][type='radio'][value='1']").click()
  submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@name="Submit2"]')))
  submit.click()

def BrowserSetting():
  if BrowserIndex.get() == 1:
    DriverPath = CurrentPath + '/chromedriver.exe'
    options = webdriver.ChromeOptions()
    RunBrowser = webdriver.Chrome
  elif BrowserIndex.get() == 2:
    DriverPath = CurrentPath + '/msedgedriver.exe'
    options = EdgeOptions()
    options.use_chromium = True
    RunBrowser = Edge

  prefs = {}
  prefs["profile.default_content_settings.popups"]=0
  options.add_experimental_option("prefs", prefs)
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
  
  browser = RunBrowser(options = options, executable_path= DriverPath)
  return browser

def TimeCardInProcess():
  ConnectVPN()
  browser = BrowserSetting()
  TimeCardIn(browser)
  # browser.close()
  disconnectVPN()
  TimerCardInList.pop(0)
  ScheduleTimeCardIn()

def TimeCardOutProcess():
  ConnectVPN()
  browser = BrowserSetting()
  TimeCardOut(browser)
  # browser.close()
  disconnectVPN()
  TimerCardOutList.pop(0)
  ScheduleTimeCardOut()

def ScheduleTimeCardIn():
  x = datetime.today()
  y = x.replace(day=x.day, hour=int(On_hour_entry.get()), minute=int(On_minute_entry.get()), second=0, microsecond=0)
  if (y-x).total_seconds() < 0:
    y = x.replace(day=x.day+1, hour=int(On_hour_entry.get()), minute=int(On_minute_entry.get()), second=0, microsecond=0)
  delta_t=y-x
  secs=delta_t.total_seconds()
  t = Timer(secs, TimeCardInProcess)
  TimerCardInList.append(t)
  t.start()

def ScheduleTimeCardOut():
  x = datetime.today()
  y = x.replace(day=x.day, hour=int(Off_hour_entry.get()), minute=int(Off_minute_entry.get()), second=0, microsecond=0)
  if (y-x).total_seconds() < 0:
    y = x.replace(day=x.day+1, hour=int(Off_hour_entry.get()), minute=int(Off_minute_entry.get()), second=0, microsecond=0)
  delta_t=y-x
  secs=delta_t.total_seconds()
  t = Timer(secs, TimeCardOutProcess)
  TimerCardOutList.append(t)
  t.start()

# def isTimeValid():
#   res = True
#   res &= On_hour_entry.get().isnumeric()
#   res &= On_minute_entry.get().isnumeric()
#   res &= Off_hour_entry.get().isnumeric()
#   res &= Off_minute_entry.get().isnumeric()
#   if res:
#     res &= int(On_hour_entry.get()) < 24 
#     res &= int(On_hour_entry.get()) >= 0
#     res &= int(On_minute_entry.get()) < 60 
#     res &= int(On_minute_entry.get()) >= 0
#     res &= int(Off_hour_entry.get()) < 24
#     res &= int(Off_hour_entry.get()) >= 0
#     res &= int(Off_minute_entry.get()) < 60
#     res &= int(Off_minute_entry.get()) >= 0
#   return res

def isBrowserSelect():
  if BrowserIndex.get() == 1 or BrowserIndex.get() == 2:
    return True
  else:
    messagebox.showwarning("Warning", "Please Select Browser")
    return False

def Main():
  if isBrowserSelect():
    User_entry['state'] = 'disabled'
    Pw_entry['state'] = 'disabled'
    On_hour_entry['state'] = 'disabled'
    On_minute_entry['state'] = 'disabled'
    Off_hour_entry['state'] = 'disabled'
    Off_minute_entry['state'] = 'disabled'
    TimeCard_start_button['state'] = 'disabled'
    BroweserSelect1['state'] = 'disabled'
    BroweserSelect2['state'] = 'disabled'
    ScheduleTimeCardIn()
    ScheduleTimeCardOut()
  else:
    messagebox.showwarning("Warning", "on time and off time not valid")

def StopProcess():
  while len(TimerCardInList) != 0:
    TimerCardInList[0].cancel()
    TimerCardInList.pop(0)
  while len(TimerCardOutList) != 0:
    TimerCardOutList[0].cancel()
    TimerCardOutList.pop(0)
  User_entry['state'] = 'normal'
  Pw_entry['state'] = 'normal'
  On_hour_entry['state'] = 'normal'
  On_minute_entry['state'] = 'normal'
  Off_hour_entry['state'] = 'normal'
  Off_minute_entry['state'] = 'normal'
  TimeCard_start_button['state'] = 'normal'
  BroweserSelect1['state'] = 'normal'
  BroweserSelect2['state'] = 'normal'

def OnHourValidate(d, i, S):
  if not S.isdigit():
    return False
  if d == '0':
    return True
  if i == '0':
    curStr = S + On_hour_entry.get()
  elif i == '1':
    curStr = On_hour_entry.get() + S
  else:
    return False
  if int(curStr) >= 24:
    return False
  else:
    return True

def OnMinuteValidate(d, i, S):
  if not S.isdigit():
    return False
  if d == '0':
    return True
  if i == '0':
    curStr = S + On_minute_entry.get()
  elif i == '1':
    curStr = On_minute_entry.get() + S
  else:
    return False
  if int(curStr) >= 60:
    return False
  else:
    return True

def OffHourValidate(d, i, S):
  if not S.isdigit():
    return False
  if d == '0':
    return True
  if i == '0':
    curStr = S + Off_hour_entry.get()
  elif i == '1':
    curStr = Off_hour_entry.get() + S
  else:
    return False
  if int(curStr) >= 24:
    return False
  else:
    return True

def OffMinuteValidate(d, i, S):
  if not S.isdigit():
    return False
  if d == '0':
    return True
  if i == '0':
    curStr = S + Off_minute_entry.get()
  elif i == '1':
    curStr = Off_minute_entry.get() + S
  else:
    return False
  if int(curStr) >= 60:
    return False
  else:
    return True

if __name__ == "__main__":
  window= tk.Tk() 
  window.title('TimeCard')
  window.geometry("300x200")
  window.configure(background='white')

  User = tk.Frame(window)
  User.pack(pady=10)
  User_label = tk.Label(User, text='User:        ')
  User_label.pack(side=tk.LEFT)
  User_label.configure(background='white')
  User_entry = tk.Entry(User, width=30)
  # User_entry.insert(0, os.getlogin())
  User_entry.pack(side=tk.LEFT)

  Pw = tk.Frame(window)
  Pw.pack(pady=10)
  Pw_label = tk.Label(Pw, text='Password:')
  Pw_label.pack(side=tk.LEFT)
  Pw_label.configure(background='white')
  Pw_entry = tk.Entry(Pw, width=30, show='*')
  Pw_entry.pack(side=tk.LEFT)

  time = tk.Frame(window)
  time.pack(pady=10)
  OnHourValidation = window.register(OnHourValidate)
  OnMinuteValidation = window.register(OnMinuteValidate)
  OffHourValidation = window.register(OffHourValidate)
  OffMinuteValidation = window.register(OffMinuteValidate)

  On_label = tk.Label(time, text='on time:')
  On_label.pack(side=tk.LEFT)
  On_label.configure(background='white')
  On_hour_entry = tk.Entry(time, width=3, validate="key", validatecommand=(OnHourValidation, '%d', '%i', '%S'))
  On_hour_entry.insert(0, '8')
  On_hour_entry.pack(side=tk.LEFT)
  On_mark_label = tk.Label(time, text=':')
  On_mark_label.pack(side=tk.LEFT)
  On_minute_entry = tk.Entry(time, width=3, validate="key", validatecommand=(OnMinuteValidation, '%d', '%i', '%S'))
  On_minute_entry.insert(0, '30')
  On_minute_entry.pack(side=tk.LEFT)

  Off_label = tk.Label(time, text='off time:')
  Off_label.pack(side=tk.LEFT)
  Off_label.configure(background='white')
  Off_hour_entry = tk.Entry(time, width=3, validate="key", validatecommand=(OffHourValidation, '%d', '%i', '%S'))
  Off_hour_entry.insert(0, '18')
  Off_hour_entry.pack(side=tk.LEFT)
  Off_mark_label = tk.Label(time, text=':')
  Off_mark_label.pack(side=tk.LEFT)
  Off_minute_entry = tk.Entry(time, width=3, validate="key", validatecommand=(OffMinuteValidation, '%d', '%i', '%S'))
  Off_minute_entry.insert(0, '00')
  Off_minute_entry.pack(side=tk.LEFT)

  RadioButton = tk.Frame(window)
  RadioButton.pack(pady=10)
  BrowserIndex = tk.IntVar()
  BrowserIndex.set(1)
  BroweserSelect1 = tk.Radiobutton(RadioButton, text='Chrome', background='white', variable=BrowserIndex, value=1)
  BroweserSelect1.pack(side=tk.LEFT)
  BroweserSelect2 = tk.Radiobutton(RadioButton, text='Edge', background='white', variable=BrowserIndex, value=2)
  BroweserSelect2.pack(side=tk.LEFT)

  TimeCard_start_button = tk.Button (window, text='Start',command=Main)
  TimeCard_start_button.place(x=90, y=170)
  TimeCard_end_button = tk.Button (window, text='Stop',command=StopProcess)
  TimeCard_end_button.place(x=180, y=170)

  window.mainloop()
