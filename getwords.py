import argparse
import re
import urllib2

print "---------------------------------------------------------------------------------------------------"
print "            Get words from www.memrise.com         "
print "---------------------------------------------------------------------------------------------------"
print "Caution:"
print "	Command -> python getwords.py -url '<url>' -mode 'single' or 'multi'"
print "	Only write Level Url for this program"
print "	The url must contain 'http://'"
print "	Example of URL -> http://www.memrise.com/course/'courseNumber'/'courseName'/'levelNumber'/"
print " If Level contents of Memrise Site contains image file, it will not be able to get data precisely"
print "---------------------------------------------------------------------------------------------------"

parser = argparse.ArgumentParser()

parser.add_argument('-url',required=True)
parser.add_argument('-mode',required=True)

args = parser.parse_args()


if args is None:
	parser.error("You must write down URL or Mode")

httpUrl = args.url[:7]

if httpUrl != 'http://':
	print("error : you should add 'http://' in URL")
	exit()

baseUrl = args.url[7:30]

if baseUrl != 'www.memrise.com/course/':
	print("error : you should write Course URL of Memrise Site")
	exit()

urlString = args.url

urlList = urlString.split('/')

if urlList[6] == '':
	print("error : No page")
	exit()

#print urlString
#print urlList[5]
#print urlList[6]

# Get words from the site
def getWordsAndWrite(url,courseName,levelNumber):
	if type(levelNumber) == int:
		levelNumber = str(levelNumber)

	source = urllib2.urlopen(url)

	content = source.read()

	wordsdata = re.findall(r'<div class="text">(.*?)</div>',str(content))

	nextdata = re.findall(r'<span class="level-name">(.*?)</span>',str(content))

	if len(wordsdata) == 0:
		print 'error : Not found data'
		exit()
	else:
		if writeToText(wordsdata,courseName,levelNumber) == False:
			print 'error : writeToText method'
			exit()

	if len(nextdata) == 0:
		print 'error : Not found nextdata'
		exit()
	else:
		return len(nextdata)

# Write data to text
def writeToText(data,courseName,levelNumber):
	if len(data) == 0:
		print 'error : Not found wordsData'
		return False

	f = open("./wordTexts/"+courseName+"_"+levelNumber+".txt",'w+')

	for eachDiv in data:
		f.write(eachDiv)
		f.write('\n')

	f.close()
	return True

# Increase Levelnumber of course
def changeUrl(url,intNumber):
	fullUrl = url.split('/')
	fullUrl[6] = str(intNumber)
	newUrl = "/".join(fullUrl)
	return newUrl

# Main
changeUrl(urlString,2)

if args.mode == 'single':
	getWordsAndWrite(urlString,urlList[5],urlList[6])
	print 'Completed - single mode'
	exit()
elif args.mode == 'multi':
	levelNum = urlList[6]
	result = getWordsAndWrite(urlString,urlList[5],levelNum)
	
	if result == 0:
		print 'error : This course has just one level'
		exit()
	elif result == 1:
		result += 1

	intNum = int(levelNum) + 1
	varUrl = urlString	

	while result == 2:
		varUrl = changeUrl(varUrl,intNum)
		result = getWordsAndWrite(varUrl,urlList[5],intNum)
		intNum += 1

	print 'Completed - multi mode'
	exit()
else:
	print 'error : Mode Input'
	exit()
