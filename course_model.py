class Course:
    #get info from mysql
    def __init__(self, db, query):
        print(query.split())
        db.execute("SHOW TABLES")

        for x in db:
            print(x)
        #get request to mysql
#        self.department = department
#        self.major = major
#        self.number = number
#        self.minors = minors
#        self.prerequesites = prerequesites

    def get_Minors(self):
        return self.minors

    def get_Prerequisites(self):
        return self.prerequesites

    def __str__(self):
        print(self.major + " " + self.number)

