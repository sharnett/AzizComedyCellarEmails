import urllib, re, datetime
from pymongo import Connection
from send_me_email import send_me_email

class Show:
    def __init__(self, id):
        self.id = id
    def dict(self):
        return {"_id": self.id, "date": self.date, "comedians": self.comedians}

# grab list of shows by id
i = urllib.urlopen("http://www.comedycellar.com/schedule3.cfm")
content = i.read()
pattern = r'<option value="(.*)"'
all_shows = re.findall(pattern,content)
# scary way to get a single list from a list of lists
show_list = [Show(int(show_id)) for days_shows in all_shows for show_id in days_shows.split(',')]

# open up database connection
connection = Connection()
db = connection.test
collection = db.foo

# grab date, time, and performers for given show. stash in database
# email if Aziz is performing
for show in show_list:
    i = urllib.urlopen("http://www.comedycellar.com/onedate.cfm?SH_IDS=%s" % show.id)
    content = i.read()
    pattern = r'<title> Comedy Cellar - Schedule for\s+(.+?)\s+</title>'
    d = re.search(pattern, content).group(1)
    pattern = r'\(Starting at (.+)\)'
    t = re.search(pattern, content).group(1)
    show.date = datetime.datetime.strptime(d+" "+t,"%A %d-%b-%y %I:%M %p")
    pattern = r'>\s+([\w\s]+?)\s+</font>'
    show.comedians = re.findall(pattern,content)
    collection.insert(show.dict())

    if "AZIZ ANSARI" in show.comedians:
        send_me_email(d + " " + t)

# if you want to print the database dates in a pretty format
#for doc in collection.find():
#    print doc['date'].strftime("%a %b %d %Y %I:%M%p")
