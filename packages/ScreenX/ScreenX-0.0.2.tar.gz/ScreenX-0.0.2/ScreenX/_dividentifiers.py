import time
import requests as rs

def extract_elements(Main_header, webcontent):
    scanner = "https://screenx-api.onrender.com/secure"
    headers = {"Header": Main_header, 'webcontent': webcontent}
    rst = rs.get(scanner, headers=headers)
    return rst

def implicit():
	time.sleep(3)
	return None

def explicit():
	time.sleep(30)
	return None


