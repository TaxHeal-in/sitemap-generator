import requests
import xml.etree.ElementTree as ET

def _dumpXML(mrnList, fileName):
	urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
	urlset.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
	urlset.set("xsi:schemaLocation", "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")
	for mrn in mrnList:
		url = ET.SubElement(urlset, "url")
		ET.SubElement(url, "loc").text = "https://taxheal.in/chartered-accountants/?mrn="+mrn
		ET.SubElement(url, "changefreq").text = "always"
		ET.SubElement(url, "priority").text = "0.6"
	tree = ET.ElementTree(urlset)
	tree.write(fileName)

def _divideList(listData, listSize):
	for index in range(0, len(listData), listSize):
		yield listData[index:index + listSize]

def _loadAPI():
	apiURL = ""
	response = requests.get(apiURL)
	if response.status_code != 200:
	    raise ApiError("GET /tasks/ {}".format(response.status_code))
	allMRNList = response.json()["data"]
	dividedMRNList = list(_divideList(allMRNList, 40000))
	currentIndex = 0
	for mrnList in dividedMRNList:
		currentIndex += 1
		_dumpXML(mrnList, "sitemaps/sitemap"+str(currentIndex)+".xml")

_loadAPI()
