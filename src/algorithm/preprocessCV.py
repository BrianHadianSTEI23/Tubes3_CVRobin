import re
import os
import fitz

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

class Job:
    def __init__(self, position: str, range: str, description: str):
        self.position = position
        self.range = range
        self.description = description
    
    def __repr__(self):
        return f"Job(Position='{self.position}', Range='{self.range}')"

class Education:
    def __init__(self, studyProgram: str, institution: str, rangeYear: str):
        self.studyProgram = studyProgram
        self.institution = institution
        self.rangeYear = rangeYear
        
    def __repr__(self):
        return f"Education(Program='{self.studyProgram}', Institution='{self.institution}', Year='{self.rangeYear}')"

class CV:
    def __init__(self, cv_path: str):
        self.continuousText = self._read_pdf_to_text(cv_path)
        parsed_data = self._parse_text()
        
        self.summary = parsed_data.get('summary', '')
        self.skills = parsed_data.get('skills', [])
        self.jobHistory = [Job(**job) for job in parsed_data.get('jobHistory', [])]
        self.education = [Education(**edu) for edu in parsed_data.get('education', [])]

    def _read_pdf_to_text(self, file_path: str) -> str:
        try:
            with fitz.open(file_path) as doc:
                full_text = "\n".join([page.get_text("text", sort=True) for page in doc])
            return full_text
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'[ï¼�â€"â€™]+', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        return text.strip()

    def _find_sections(self, text: str) -> dict:
        section_keywords = {
            'summary': ['summary', 'profile', 'objective', 'professional profile', 'career overview', 'career summary', 'professional summary', 'overview'],
            'experience': ['experience', 'employment history', 'work history', 'professional experience', 'work experience', 'employment', 'career history', 'positions held'],
            'education': ['education', 'academic background', 'academic', 'qualifications', 'educational background', 'training', 'education and training'],
            'skills': ['skills', 'abilities', 'expertise', 'qualifications', 'technical skills', 'core competencies', 'competencies', 'key skills', 'highlights']
        }
        
        sections = {'start': text}
        section_positions = []
        
        for section_type, keywords in section_keywords.items():
            for keyword in keywords:
                patterns = [
                    rf'^{re.escape(keyword)}\s*$',
                    rf'^{re.escape(keyword)}\s*:',
                    rf'\b{re.escape(keyword)}\b\s*$',
                    rf'^[•\-*]\s*{re.escape(keyword)}',
                ]
                
                for pattern in patterns:
                    for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
                        section_positions.append((match.start(), section_type, keyword))
        
        section_positions.sort()
        
        for i, (start_pos, section_type, keyword) in enumerate(section_positions):
            end_pos = section_positions[i+1][0] if i + 1 < len(section_positions) else len(text)
            content = text[start_pos:end_pos].strip()
            
            content = re.sub(rf'^.*?{re.escape(keyword)}.*?$', '', content, count=1, flags=re.IGNORECASE | re.MULTILINE).strip()
            
            if content and len(content) > 10:
                sections[section_type] = content
                
        return sections

    def _extract_dates_enhanced(self, text: str) -> list[tuple]:
        date_patterns = [
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December)[\s,.]*\d{2,4}\b\s*[-–—to]+\s*\b(?:Present|Current|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December)[\s,.]*\d{2,4}\b',
            r'\b\d{4}\s*[-–—to]+\s*(?:\d{4}|Present|Current)\b',
            r'\b\d{1,2}[/-]\d{4}\s*[-–—to]+\s*(?:\d{1,2}[/-]\d{4}|Present|Current)\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December)\s+\d{4}\s*[-–—,to]+\s*(?:Present|Current|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December)\s+\d{4}',
            r'since\s+\d{4}|from\s+\d{4}',
        ]
        
        found_dates = []
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                found_dates.append((match.start(), match.group().strip()))
        
        return found_dates

    def _parse_experience_enhanced(self, content: str) -> list[dict[str, str]]:
        jobs = []
        content = self._clean_text(content)
        
        date_matches = self._extract_dates_enhanced(content)
        
        if date_matches:
            date_matches.sort()
            
            for i, (date_pos, date_str) in enumerate(date_matches):
                start_search = date_matches[i-1][0] + len(date_matches[i-1][1]) if i > 0 else 0
                end_search = date_matches[i+1][0] if i + 1 < len(date_matches) else len(content)
                
                before_date = content[start_search:date_pos].strip()
                after_date = content[date_pos + len(date_str):end_search].strip()
                
                lines_before = before_date.split('\n')
                position = "Position Not Specified"
                
                for line in reversed(lines_before):
                    line = line.strip()
                    if line and len(line.split()) <= 8:
                        if (re.search(r'(?i)\b(manager|director|supervisor|chef|analyst|specialist|consultant|technician|engineer|coordinator|assistant|officer|representative|developer|instructor|lecturer)\b', line) or
                            re.match(r'^[A-Z][A-Za-z\s&/\-]+$', line)):
                            position = line
                            break
                
                description_lines = after_date.split('\n')
                description_parts = []
                for line in description_lines:
                    line = line.strip()
                    if line and len(line) > 10:
                        if re.search(r'(?i)^[A-Z][A-Za-z\s&/\-]+(?:Manager|Director|Supervisor|Chef|Analyst)$', line):
                            break
                        description_parts.append(line)
                
                description = '\n'.join(description_parts[:3])
                
                if position != "Position Not Specified" or description:
                    jobs.append({
                        "position": position,
                        "range": date_str,
                        "description": description
                    })
        
        if not jobs:
            job_keywords = ['manager', 'assistant', 'coordinator', 'analyst', 'specialist', 'director', 'supervisor', 'officer', 'chef', 'consultant', 'technician', 'engineer', 'developer']
            
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            found_jobs = []
            
            for i, line in enumerate(lines):
                if any(keyword in line.lower() for keyword in job_keywords):
                    if line not in [job['position'] for job in found_jobs]:
                        date_range = "Date Not Specified"
                        for j in range(max(0, i-2), min(len(lines), i+3)):
                            if re.search(r'\b\d{4}\b', lines[j]):
                                date_range = lines[j]
                                break
                        
                        description_lines = []
                        for j in range(i+1, min(len(lines), i+4)):
                            if not any(kw in lines[j].lower() for kw in job_keywords):
                                description_lines.append(lines[j])
                        
                        found_jobs.append({
                            "position": line,
                            "range": date_range,
                            "description": '\n'.join(description_lines)
                        })
                        
                        if len(found_jobs) >= 5:
                            break
            
            jobs = found_jobs
        
        return jobs

    def _parse_education_advanced(self, content: str) -> list:
        educations = []
        
        edu_keywords = ['university', 'college', 'institute', 'school', 'academy', 'center', 'centre']
        degree_keywords = ['bachelor', 'master', 'phd', 'ph.d', 'doctorate', 'associate', 'diploma', 'certificate', 'degree', 'b.s', 'b.a', 'm.s', 'm.a', 'mba', 'bba']
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in edu_keywords):
                institution = line
                
                study_program = "Program Not Specified"
                for j in range(max(0, i-3), min(len(lines), i+3)):
                    if j != i and any(keyword in lines[j].lower() for keyword in degree_keywords):
                        study_program = lines[j]
                        break
                
                year = "Year Not Specified"
                for j in range(max(0, i-2), min(len(lines), i+3)):
                    year_match = re.search(r'\b(\d{4})\b', lines[j])
                    if year_match:
                        year = year_match.group(1)
                        break
                
                educations.append({
                    "institution": institution,
                    "studyProgram": study_program,
                    "rangeYear": year
                })
        
        if not educations:
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                if any(keyword in line_lower for keyword in degree_keywords):
                    study_program = line
                    
                    institution = "Institution Not Specified"
                    for j in range(i+1, min(len(lines), i+4)):
                        if any(keyword in lines[j].lower() for keyword in edu_keywords):
                            institution = lines[j]
                            break
                    
                    if institution == "Institution Not Specified":
                        for j in range(max(0, i-3), i):
                            if any(keyword in lines[j].lower() for keyword in edu_keywords):
                                institution = lines[j]
                                break
                    
                    year = "Year Not Specified"
                    for j in range(max(0, i-2), min(len(lines), i+3)):
                        year_match = re.search(r'\b(\d{4})\b', lines[j])
                        if year_match:
                            year = year_match.group(1)
                            break
                    
                    educations.append({
                        "institution": institution,
                        "studyProgram": study_program,
                        "rangeYear": year
                    })
        
        if not educations:
            for line in lines:
                year_match = re.search(r'\b(19\d{2}|20\d{2})\b', line)
                if year_match:
                    year = year_match.group(1)
                    
                    educations.append({
                        "institution": "Institution Not Specified",
                        "studyProgram": line,
                        "rangeYear": year
                    })
                    break
        
        return educations

    def _parse_skills_advanced(self, content: str) -> list:
        skills = []
        
        delimiters = ['\n', '•', '*', '-', '|', ',', ';']
        
        skill_text = content
        for delimiter in delimiters:
            skill_text = skill_text.replace(delimiter, '\n')
        
        potential_skills = [skill.strip() for skill in skill_text.split('\n') if skill.strip()]
        
        for skill in potential_skills:
            if len(skill.split()) <= 6 and len(skill) > 2:
                skip_words = ['skills', 'abilities', 'experience', 'knowledge', 'summary', 'profile']
                if not any(skip_word in skill.lower() for skip_word in skip_words):
                    skills.append(skill)
        
        return skills

    def _parse_text(self) -> dict:
        if not self.continuousText: 
            return {"summary": "", "skills": [], "jobHistory": [], "education": []}

        text = self.continuousText
        sections = self._find_sections(text)
        output = {"summary": "", "skills": [], "jobHistory": [], "education": []}

        summary_content = None
        for summary_key in ['summary', 'profile', 'objective', 'professional profile', 'career overview']:
            if summary_key in sections:
                summary_content = sections[summary_key]
                break
        
        if not summary_content:
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                if len(para.split()) > 20:
                    summary_content = para.strip()
                    break
        
        output['summary'] = summary_content.strip() if summary_content else ""

        exp_content = None
        for exp_key in ['experience', 'work history', 'employment history', 'professional experience']:
            if exp_key in sections:
                exp_content = sections[exp_key]
                break
        
        if exp_content:
            output['jobHistory'] = self._parse_experience_enhanced(exp_content)
        
        if not output['jobHistory']:
            output['jobHistory'] = self._parse_experience_enhanced(text)

        edu_content = None
        for edu_key in ['education', 'academic background', 'training', 'education and training']:
            if edu_key in sections:
                edu_content = sections[edu_key]
                break
        
        if edu_content:
            output['education'] = self._parse_education_advanced(edu_content)
        
        if not output['education']:
            output['education'] = self._parse_education_advanced(text)

        skills_content = None
        for skills_key in ['skills', 'abilities', 'qualifications', 'highlights', 'technical skills']:
            if skills_key in sections:
                skills_content = sections[skills_key]
                break
        
        if skills_content:
            output['skills'] = self._parse_skills_advanced(skills_content)
        
        if not output['skills']:
            skill_patterns = [
                r'Microsoft\s+Office', r'Excel', r'PowerPoint', r'Word',
                r'Python', r'Java', r'JavaScript', r'HTML', r'CSS',
                r'Project\s+Management', r'Leadership', r'Communication'
            ]
            
            for pattern in skill_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    output['skills'].append(match.group())
        
        if not output['jobHistory']:
            output['jobHistory'] = [{
                "position": "Position Not Specified",
                "range": "Date Not Specified", 
                "description": "Experience details not clearly specified in the provided CV format."
            }]
        
        if not output['education']:
            output['education'] = [{
                "institution": "Institution Not Specified",
                "studyProgram": "Program Not Specified",
                "rangeYear": "Year Not Specified"
            }]
            
        return output

# if __name__ == '__main__':
#     data_directory = "data/"
#     print(f"Memulai proses parsing untuk semua CV di direktori: '{data_directory}'\n")
#     print("Target: 100% Success Rate dengan Enhanced Parsing\n")
    
#     failed_files = []
#     total_files = 0
#     detailed_results = []

#     if not os.path.isdir(data_directory):
#         print(f"Error: Direktori '{data_directory}' tidak ditemukan.")
#     else:
#         for root, dirs, files in os.walk(data_directory):
#             for filename in files:
#                 if filename.lower().endswith(".pdf"):
#                     total_files += 1
#                     file_path = os.path.join(root, filename)
                    
#                     print(f"--- Memproses: {file_path} ---")
                    
#                     try:
#                         cv_object = CV(file_path)
                        
#                         job_count = len(cv_object.jobHistory)
#                         edu_count = len(cv_object.education)
#                         skill_count = len(cv_object.skills)
#                         summary_length = len(cv_object.summary)
                        
#                         result = {
#                             'file': file_path,
#                             'jobs': job_count,
#                             'education': edu_count,
#                             'skills': skill_count,
#                             'summary_length': summary_length,
#                             'success': True
#                         }
                        
#                         print(f"   - PARSING BERHASIL: Jobs({job_count}), Edu({edu_count}), Skills({skill_count}), Summary({summary_length} chars)")
                        
#                         detailed_results.append(result)
#                         print("-" * (25 + len(file_path)))
                            
#                     except Exception as e:
#                         print(f"ERROR pada file: {file_path}")
#                         print(f"   - Pesan Error: {e}\n")
#                         failed_files.append(file_path)
                        
#                         result = {
#                             'file': file_path,
#                             'jobs': 0,
#                             'education': 0,
#                             'skills': 0,
#                             'summary_length': 0,
#                             'success': False,
#                             'error': str(e)
#                         }
#                         detailed_results.append(result)

#     print("\n==========================================")
#     print("      PROSES PARSING SELESAI")
#     print("==========================================")
#     print(f"Total file PDF yang diproses: {total_files}")
#     if total_files > 0:
#         success_rate = ((total_files - len(failed_files)) / total_files) * 100
#         print(f"Tingkat Keberhasilan: {success_rate:.2f}%")
#     print(f"Jumlah file dengan error : {len(failed_files)}")
    
#     if detailed_results:
#         successful_results = [r for r in detailed_results if r['success']]
#         if successful_results:
#             avg_jobs = sum(r['jobs'] for r in successful_results) / len(successful_results)
#             avg_edu = sum(r['education'] for r in successful_results) / len(successful_results)
#             avg_skills = sum(r['skills'] for r in successful_results) / len(successful_results)
            
#             print(f"\n📊 STATISTIK PARSING:")
#             print(f"   - Rata-rata Jobs per CV: {avg_jobs:.1f}")
#             print(f"   - Rata-rata Education per CV: {avg_edu:.1f}")
#             print(f"   - Rata-rata Skills per CV: {avg_skills:.1f}")
    
#     if failed_files:
#         print(f"\n Daftar file dengan error ({len(failed_files)} files):")
#         for f in sorted(failed_files):
#             print(f"- {f}")
#     else:
#         print(f"jadi boy")