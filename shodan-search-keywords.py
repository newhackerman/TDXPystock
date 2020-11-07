import shodan as sd
import requests
import re,regcheck

def shodanSearch(keywords,key):
	SHODAN_API_KEY="YVI56aNU4iV6ylHaLp56eQxeBhZ4QJul"
	api=sd.Shodan(SHODAN_API_KEY)
	iplist=[]
	total=0
	CHECKLIST=[]
	try:
		result=api.search(keywords,limit=None)
		total=int(result['total'])
		for results in result['matches']:iplist.append({"ip":results['ip_str'],"country":results['location']['country_name'],"port":results['port'],"os":results['os']})
		print("total is :",total,"ip is :",iplist)
		return  total,iplist
	except sd.APIError as e:
		print("shodan api return error:",e)

def checkStatus(host):
	CHECKLIST=[]
	aimurl = "http://"+host['ip']+"/admin/firmwareupdate.html"
	try:
		req = requests.get(url = aimurl,timeout = 10)
		html_code = req.content

		title = re.findall(r'<title>(.+?)</title>',html_code)[0]
		code = re.findall(r'<dd>(.+?)</dd>',html_code)[1]
		version = re.findall(r'<dd>(.+?)</dd>',html_code)[2].replace('&nbsp;','')

		if "Brother" in title:
			CHECKLIST.append(host['ip'])
			print(aimurl," ---> ",title," code:",code," version:",version)
	except Exception as e1:
		print ("checkStatusis  error:", e1)

searchword="default+password+country：‘CN’+port：‘8081’";
shodanSearch('HTTP/1.1 200 OK',searchword)
hosts=["120.12.132.98"]
#checkStatus(hosts)


