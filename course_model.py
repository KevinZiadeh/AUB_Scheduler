class Course:
    #get info from mongodb
    def __init__(self, db, query):
        this = db.find_one(query)
        #get request to mongodb
        self.department = this["department"]
        self.major = this["major"]
        self.num = this["num"]
        self.minors = this["minors"]
        self.prerequesites = this["prerequisites"]
        self.tracks = this["tracks"]

    def get_Minors(self):
        return self.minors

    def get_Prerequisites(self):
        return self.prerequesites

    def get_Tracks(self):
        return self.tracks

    def __str__(self):
        return (str(self.major) + " " + str(self.num))
