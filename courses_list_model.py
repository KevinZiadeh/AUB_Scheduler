class Courses_list:
    def __init__(self, db_courses, db_major, courses_id):
        self.courses_id = courses_id
        self.db_courses = db_courses
        self.db_major = db_major

        #check for equivalent cours
        s = self.equivalent_check()
        print(s)

#get total number of credits given an array of courses id
    def get_number_credits(self):
        total = 0
        #loop over every course in array, search for it in database, then add the
        #number of credits to total
        for single_course_id in self.courses_id:
            course = self.db_courses.find_one({"_id" : single_course_id})
            total += int(course['credit'])
        return total

    '''
    add relevant courses to db [math, cmps, engl, arab, humanities, social sciences, technical]
    do majors db

    add special courses checking (eece3xx, eece4xx) and
    or checking (math218|math219)

    add remaining get_missing_xxx
    '''

    #get list of missing core courses
    def get_missing_core_courses(self, major, list_courses):
        '''
        returns tuple with:
        1: list of courses in courses_id that are not in this db
        2: object containing list of courses that you should take with message
        '''
        list_remaining = [] #list of remaining courses that are not core courses
        cur_major = self.db_major.find_one({"_id" : major})
        list_core = cur_major["core"] #list of all core courses
        missing = {"list": [], "message" : "", "attribute": "core"}
        num_courses = cur_major["number_courses"]["core"].to_decimal() #number of credits that we should get
        matches = 0

        for single_course_id in list_courses:
            i = self.get_index(list_core, single_course_id)
            if i == -1:
                list_remaining.append(single_course_id)
            else:
                if i >= 0:
                    del list_core[i]
                matches += int(self.db_courses.find_one({"_id": single_course_id})["credit"])
                if matches == num_courses:
                    missing["list"] = [""]
                    missing["message"] = "You took all core courses"
                    return (list_remaining, missing)

        missing["list"] = list_core
        missing["message"] = "You still need to take " + str(num_courses-matches) + " credits"
        return (list_remaining, missing)

    #get list of missing core lab courses
    def get_missing_core_lab_courses(self, major, list_courses):
        '''
        returns tuple with:
        1: list of courses in courses_id that are not in this db
        2: object containing list of courses that you should take with message
        '''
        list_remaining = [] #list of remaining courses that are not core courses
        cur_major = self.db_major.find_one({"_id" : major})
        list_core = cur_major["core_lab"] #list of all core_lab courses
        missing = {"list": [], "message" : "", "attribute": "core_lab"}
        num_courses = cur_major["number_courses"]["core_lab"].to_decimal() #number of credits that we should get
        matches = 0

        for single_course_id in list_courses:
            if single_course_id[-1] != "L":
                continue
            i = self.get_index(list_core, single_course_id)
            if i == -1:
                list_remaining.append(single_course_id)
            else:
                del list_core[i]
                matches += int(self.db_courses.find_one({"_id": single_course_id})["credit"])
                if matches == num_courses:
                    missing["list"] = [""]
                    missing["message"] = "You took all core lab courses"
                    return (list_remaining, missing)

        missing["list"] = list_core
        missing["message"] = "You still need to take " + str(num_courses-matches) + " credits"
        return (list_remaining, missing)

    #get list of missing science elective courses
    def get_missing_science_elective_courses(self, major, list_courses):
        '''
        returns tuple with:
        1: list of courses in courses_id that are not in this db
        2: object containing list of courses that you should take with message
        '''
        list_remaining = [] #list of remaining courses that are not science_elective courses
        cur_major = self.db_major.find_one({"_id" : major})
        list_core = cur_major["science_elective"] #list of all science_elective courses
        missing = {"list": [], "message" : "", "attribute": "science_elective"}
        num_courses = cur_major["number_courses"]["science_elective"].to_decimal() #number of credits that we should get
        matches = 0

        for single_course_id in list_courses:
            i = self.get_index(list_core, single_course_id)
            if i == -1:
                list_remaining.append(single_course_id)
            else:
                del list_core[i]
                matches += int(self.db_courses.find_one({"_id": single_course_id})["credit"])
                if matches == num_courses:
                    missing["list"] = [""]
                    missing["message"] = "You took all necessary science elective courses"
                    return (list_remaining, missing)

        missing["list"] = list_core
        missing["message"] = "You still need to take " + str(num_courses-matches) + " credits"
        return (list_remaining, missing)

    #get list of missing math elective courses
    def get_missing_math_elective_courses(self, major, list_courses):
        '''
        returns tuple with:
        1: list of courses in courses_id that are not in this db
        2: object containing list of courses that you should take with message
        '''
        list_remaining = [] #list of remaining courses that are not math_elective courses
        cur_major = self.db_major.find_one({"_id" : major})
        list_core = cur_major["math_elective"] #list of all math_elective courses
        missing = {"list": [], "message" : "", "attribute": "math_elective"}
        num_courses = cur_major["number_courses"]["math_elective"].to_decimal() #number of credits that we should get
        matches = 0

        for single_course_id in list_courses:
            if single_course_id[0] != "m":
                continue
            i = self.get_index(list_core, single_course_id)
            if i == -1:
                list_remaining.append(single_course_id)
            else:
                del list_core[i]
                matches += int(self.db_courses.find_one({"_id": single_course_id})["credit"])
                if matches == num_courses:
                    missing["list"] = [""]
                    missing["message"] = "You took all math elective necessary courses"
                    return (list_remaining, missing)

        missing["list"] = list_core
        missing["message"] = "You still need to take " + str(num_courses-matches) + " credits"
        return (list_remaining, missing)

    #get list of missing restricted courses
    def get_missing_restricted_courses(self, major, list_courses):
                '''
                returns tuple with:
                1: list of courses in courses_id that are not in this db
                2: object containing list of courses that you should take with message
                '''
                list_remaining = [] #list of remaining courses that are not restricted courses
                cur_major = self.db_major.find_one({"_id" : major})
                list_core = cur_major["restricted"] #list of all restricted courses
                missing = {"list": [], "message" : "", "attribute": "restricted"}
                num_courses = cur_major["number_courses"]["restricted"].to_decimal() #number of credits that we should get
                matches = 0

                for single_course_id in list_courses:
                    i = self.get_index(list_core, single_course_id)
                    if i == -1:
                        list_remaining.append(single_course_id)
                    else:
                        del list_core[i]
                        matches += int(self.db_courses.find_one({"_id": single_course_id})["credit"])
                        if matches == num_courses:
                            missing["list"] = [""]
                            missing["message"] = "You took all necessary restricted elective courses"
                            return (list_remaining, missing)

                missing["list"] = list_core
                missing["message"] = "You still need to take " + str(num_courses-matches) + " credits"
                return (list_remaining, missing)

    #get list of missing restricted lab courses
    def get_missing_restricted_lab_courses(self, major, list_courses):
        '''
        returns tuple with:
        1: list of courses in courses_id that are not in this db
        2: object containing list of courses that you should take with message
        '''
        list_remaining = [] #list of remaining courses that are not restricted_lab courses
        cur_major = self.db_major.find_one({"_id" : major})
        list_core = cur_major["restricted_lab"] #list of all restricted_lab courses
        missing = {"list": [], "message" : "", "attribute": "restricted_lab"}
        num_courses = cur_major["number_courses"]["restricted_lab"].to_decimal() #number of credits that we should get
        matches = 0

        for single_course_id in list_courses:
            if single_course_id[-1] != "L":
                continue
            i = self.get_index(list_core, single_course_id)
            if i == -1:
                list_remaining.append(single_course_id)
            else:
                del list_core[i]
                matches += int(self.db_courses.find_one({"_id": single_course_id})["credit"])
                if matches == num_courses:
                    missing["list"] = [""]
                    missing["message"] = "You took all necessary restricted lab courses"
                    return (list_remaining, missing)

        missing["list"] = list_core
        missing["message"] = "You still need to take " + str(num_courses-matches) + " credits"
        return (list_remaining, missing)

    #general get remaining courses that calls other get_remaining_xxx
    def remaining_courses(self, major):
        temp_list = []
        temp_missing = {}
        missing_array = []
        (temp_list, temp_missing) = self.get_missing_core_courses(major, self.courses_id)
        missing_array.append(temp_missing)
        (temp_list, temp_missing) = self.get_missing_core_lab_courses(major, temp_list)
        missing_array.append(temp_missing)
        (temp_list, temp_missing) = self.get_missing_science_elective_courses(major, temp_list)
        missing_array.append(temp_missing)
        (temp_list, temp_missing) = self.get_missing_restricted_courses(major, temp_list)
        missing_array.append(temp_missing)
        (temp_list, temp_missing) = self.get_missing_math_elective_courses(major, temp_list)
        missing_array.append(temp_missing)
        (temp_list, temp_missing) = self.get_missing_restricted_lab_courses(major, temp_list)
        missing_array.append(temp_missing)
        return missing_array


    def __str__(self):
        s = ""
        for course in self.courses_id:
            if len(course) > 8:
                this_list = course.split("|") #checking for "or" courses
                for e in this_list:
                    if e[-1] == "x": #checking for specific level courses
                        s += ("any " + e[:5] + "00 level course ")
                    elif len(e) < 5:
                        s += ("any " + e + " course ")
                    else:
                        s += (e + " ")
                    if e != this_list[-1]:
                        s += "or "
                    else:
                        s += ", "
            elif course[-1] == "x":
                s += ("any " + course[4] + "00 level " + course[:4] + " course, ")
            elif len(course) < 5:
                s += ("any " + course + " course, ")
            else:
                s += (course + ", ")
        return s[:-2] #remove trailing comma and space

        def remaining_courses_print(self, list_courses):
            s = ""
            for course in list_courses:
                if len(course) > 8:
                    this_list = course.split("|") #checking for "or" courses
                    for e in this_list:
                        if e[-1] == "x": #checking for specific level courses
                            s += ("any " + e[:5] + "00 level course ")
                        elif len(e) < 5:
                            s += ("any " + e + " course ")
                        else:
                            s += (e + " ")
                        if e != this_list[-1]:
                            s += "or "
                        else:
                            s += ", "
                elif course[-1] == "x":
                    s += ("any " + course[4] + "00 level " + course[:4] + " course, ")
                elif len(course) < 5:
                    s += ("any " + course + " course, ")
                else:
                    s += (course + ", ")
            return s[:-2] #remove trailing comma and space

    def or_confusion_resolution(self, list_search):
        NL = []
        index = []
        for i in range (len(list_search)):
            if len(list_search[i])>8:
                index.append(i)
                NL.extend(list_search[i].split("|"))

        for i in range(len(index)-1, -1, -1):
            del list_search[index[i]]
        list_search.extend(NL)
        return list_search

    def get_index(self, list_search, course_id):
        if list_search[0] == "":
            return -1
        for i in range(len(list_search)):
            if len(list_search[i]) > 9:
                search = list_search[i].split("|")
                try:
                    search.index(course_id)
                    return i
                except:
                    pass
            elif list_search[i][-1] == "x":
                if list_search[i][4] == course_id[4]:
                    return -int(course_id[4])
            elif list_search[i] == course_id:
                return i
        return -1

    def equivalent_check(self):
        s = ""
        for i in range(len(self.courses_id)):
            equivalen_list = self.db_courses.find_one({"_id": self.courses_id[i]})["equivalent"]
            if len(equivalen_list) == 0:
                continue
            for j in range(i+1, len(self.courses_id)):
                if self.get_index(equivalen_list, self.courses_id[j]) != -1:
                    s+= "Careful, " + self.courses_id[i] + " and " + self.courses_id[j] + " are equivalent courses \n"
        return s
