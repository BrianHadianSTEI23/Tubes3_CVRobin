'''
algorithm
1. do read all text in cv
2. return that continuous text'''
        
# specification : read cvPath then return its continuous text
import pymupdf
import re

''' command to create database 
CREATE DATABASE cvrobin;

CREATE TABLE applicant_profile (
    applicant_id    INT NOT NULL AUTO INCREMENT PRIMARY KEY,
    first_name  VARCHAR(50) DEFAULT NULL,
    last_name  VARCHAR(50) DEFAULT NULL,
    date_of_birth   DATE    DEFAULT NULL,
    address VARCHAR(255) DEFAULT NULL,
    phone_number    VARCHAR(20) DEFAULT NULL
)

CREATE TABLE application_detail (
    detail_id   INT NOT NULL AUTO INCREMENT PRIMARY KEY,
    applicant_id    INT NOT NULL,
    application_role    VARCHAR(100) DEFAULT NULL,
    cv_path     TEXT
)
'''

class Job : 
    
    def __init__(self,
                 position : str,
                 range : tuple[int, int],
                 description : str
                 ) -> None:
        self.position = position
        self.range = range
        self.description = description

class Education : 
    
    def __init__(self,
                 studyProgram :str,
                 institution : str,
                 rangeYear : tuple[int, int]
                 ) -> None:
        self.studyProgram = studyProgram
        self.institution = institution
        self.rangeYear = rangeYear

class CV:

    '''
    name : str,
    bod : str,
    address : str,
    phone : str,
    skills : list[str]
    jobHistory : list[Job],
    education : list[Education],
    continuousText : str '''

    def __init__(self,
                 cvPath : str
                 ) -> None:
        
        # read the cv
        continuousText = ""
        targetCV = pymupdf.open(cvPath)
        
        for page in targetCV:
            continuousText += (page.get_textpage().extractText())

        targetCV.close()

        keywords = ["accomplishments", "name", "birthdate", "address", "phone", "fax", "experience", "education", "skills", ""]

        result = self.preprocessCV(continuousText, keywords)

        # assignment of each cv essentials
        self.name = result["name"]
        self.bod = result["bod"]
        self.address = result["address"]
        self.phone = result["phone"]
        self.skills = result["skills"]
        self.jobHistory = result["jobHistory"]
        self.education = result["education"]
        self.continuousText = continuousText

    @staticmethod
    def preprocessCV(continuousText : str,
                     keywords : list[str]) -> dict:
        # for keyword in keywords :
        pattern = r"|".join(re.escape(k) for k in keywords)
        matches = list(re.finditer(pattern, continuousText))
        sections = {}
        for i in range(len(matches) - 1):
            start_keyword = matches[i].group()
            start_index = matches[i].end()
            end_index = matches[i+1].start()
            sections[start_keyword] = continuousText[start_index:end_index].strip()
            
        return sections

# debug
cv = CV("data/ACCOUNTANT/10554236.pdf")
# print(cv.continuousText)
CV.preprocessCV(cv.continuousText, [])


