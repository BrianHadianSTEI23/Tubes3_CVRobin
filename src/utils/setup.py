import mysql.connector
import os
from algorithm.preprocessCV import CV

def setup():
    data_directory = "../data/"
    print(f"Memulai proses parsing untuk semua CV di direktori: '{data_directory}'\n")
    print("Target: 100% Success Rate dengan Enhanced Parsing\n")
    
    failed_files = []
    total_files = 0
    detailed_results = []

    if not os.path.isdir(data_directory):
        print(f"Error: Direktori '{data_directory}' tidak ditemukan.")
    else:
        for root, dirs, files in os.walk(data_directory):
            for filename in files:
                if filename.lower().endswith(".pdf"):
                    total_files += 1
                    file_path = os.path.join(root, filename)
                    
                    print(f"--- Memproses: {file_path} ---")
                    
                    try:
                        cv_object = CV(file_path)
                        
                        job_count = len(cv_object.jobHistory)
                        edu_count = len(cv_object.education)
                        skill_count = len(cv_object.skills)
                        summary_length = len(cv_object.summary)
                        
                        result = {
                            'file': file_path,
                            'jobs': job_count,
                            'education': edu_count,
                            'skills': skill_count,
                            'summary_length': summary_length,
                            'success': True
                        }
                        
                        print(f"   - PARSING BERHASIL: Jobs({job_count}), Edu({edu_count}), Skills({skill_count}), Summary({summary_length} chars)")
                        
                        detailed_results.append(result)
                        print("-" * (25 + len(file_path)))
                            
                    except Exception as e:
                        print(f"ERROR pada file: {file_path}")
                        print(f"   - Pesan Error: {e}\n")
                        failed_files.append(file_path)
                        
                        result = {
                            'file': file_path,
                            'jobs': 0,
                            'education': 0,
                            'skills': 0,
                            'summary_length': 0,
                            'success': False,
                            'error': str(e)
                        }
                        detailed_results.append(result)

    print("\n==========================================")
    print("      PROSES PARSING SELESAI")
    print("==========================================")
    print(f"Total file PDF yang diproses: {total_files}")
    if total_files > 0:
        success_rate = ((total_files - len(failed_files)) / total_files) * 100
        print(f"Tingkat Keberhasilan: {success_rate:.2f}%")
    print(f"Jumlah file dengan error : {len(failed_files)}")
    
    if detailed_results:
        successful_results = [r for r in detailed_results if r['success']]
        if successful_results:
            avg_jobs = sum(r['jobs'] for r in successful_results) / len(successful_results)
            avg_edu = sum(r['education'] for r in successful_results) / len(successful_results)
            avg_skills = sum(r['skills'] for r in successful_results) / len(successful_results)
            
            print(f"\n📊 STATISTIK PARSING:")
            print(f"   - Rata-rata Jobs per CV: {avg_jobs:.1f}")
            print(f"   - Rata-rata Education per CV: {avg_edu:.1f}")
            print(f"   - Rata-rata Skills per CV: {avg_skills:.1f}")

        # get all aplicants data from the database
        conn = mysql.connector.connect(
            host="mysql-66af4eb-cvrobin.g.aivencloud.com",
            user="avnadmin",
            password="AVNS_OwS64toTSD7MkC29m2-",
            database="defaultdb",
            port = 10647
        )

        # Create a cursor to execute queries
        cursor = conn.cursor()

        # make the table
        cursor.execute("CREATE TABLE applicant_profile ( applicant_id    INT NOT NULL AUTO INCREMENT PRIMARY KEY, first_name  VARCHAR(50) DEFAULT NULL,last_name  VARCHAR(50) DEFAULT NULL, date_of_birth   DATE    DEFAULT NULL, address VARCHAR(255) DEFAULT NULL, phone_number    VARCHAR(20) DEFAULT NULL)")

        # fill the table with data

        # commit the data into the database
        conn.commit()

        # close the connection
        cursor.close()
        conn.close()
    
    if failed_files:
        print(f"\n Daftar file dengan error ({len(failed_files)} files):")
        for f in sorted(failed_files):
            print(f"- {f}")
    else:
        print(f"jadi boy")

if __name__ == '__main__':
    setup()