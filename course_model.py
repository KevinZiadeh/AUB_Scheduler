class Course:

    def __init__(self, db, query):
        #get request to mongodb
        this = db.find_one(query)
        self.department = this["department"]
        self.major = this["major"]
        self.num = this["num"]
        self.minors = this["minors"]
        self.prerequesites = this["prerequisites"]
        self.corequisites = this["corequisites"]
        self.tracks = this["tracks"]
        self.equivalent = this["equivalent"]
        self.credit = this["credit"]

    def get_Minors(self):
        return self.minors

    def get_Prerequisites(self):
        return self.prerequesites

    def get_Tracks(self):
        return self.tracks

    def __str__(self):
        return (str(self.major) + " " + str(self.num))
