import mysql.connector
import os
import faker
import random
from algorithm.encryptionModule import encrypt

# Specification : this basically do seeding for the database

# seeding
def setup():
    data_directory = "../data/"
    password = "abrarbrianfaqih"
    print(f"Memulai proses parsing untuk semua CV di direktori: '{data_directory}'\n")
    print("Target: 100% Success Rate dengan Enhanced Parsing\n")
    
    failed_files = []
    total_files = 0
    applicant_ids = []
    all_applicant_profile_data= []
    all_application_detail_data = []

    if not os.path.isdir(data_directory):
        print(f"Error: Direktori '{data_directory}' tidak ditemukan.")
    else:

        # initialize faker data
        fake = faker.Faker("id_ID")

        for root, dirs, files in os.walk(data_directory):
            for filename in files:
                if filename.lower().endswith(".pdf"):
                    total_files += 1
                    file_path = os.path.join(root, filename)
                    
                    print(f"--- Memproses: {file_path} ---")
                    
                    try:
                        print(f"   - PARSING BERHASIL")

                        # fill all applicant profile data
                        all_applicant_profile_data.append(
                            {
                                "first_name" : encrypt(password, fake.first_name()),
                                "last_name" : encrypt(password, fake.last_name()),
                                "date_of_birth" : encrypt(password, fake.date_of_birth().isoformat()),
                                "address" : encrypt(password, fake.address().replace("\n", " ")),
                                "phone_number" : encrypt(password, fake.phone_number()),
                            }
                        )

                        # fill all application detail
                        all_application_detail_data.append(
                            {
                                "applicant_id" : None, # this is just a placeholder
                                "application_role" : encrypt(password, fake.job()),
                                "cv_path" : encrypt(password, file_path),
                            }
                        )
                    
                        print("-" * (25 + len(file_path)))
                            
                    except Exception as e:
                        print(f"ERROR pada file: {file_path}")
                        print(f"   - Pesan Error: {e}\n")
                        failed_files.append(file_path)

        

    print("\n==========================================")
    print("      PROSES PARSING SELESAI")
    print("==========================================")
    print(f"Total file PDF yang diproses: {total_files}")
    if total_files > 0:
        success_rate = ((total_files - len(failed_files)) / total_files) * 100
        print(f"Tingkat Keberhasilan: {success_rate:.2f}%")
    print(f"Jumlah file dengan error : {len(failed_files)}")

    # debug
    # print(all_application_detail_data)
    
    if all_applicant_profile_data and all_application_detail_data:

        # # get all aplicants data from the database
        conn = mysql.connector.connect(
            host="mysql-66af4eb-cvrobin.g.aivencloud.com",
            user="avnadmin",
            password="AVNS_OwS64toTSD7MkC29m2-",
            database="defaultdb",
            port = 10647
        )

        # # Create a cursor to execute queries
        cursor = conn.cursor()

        # Drop and recreate the applicant_profile table
        # cursor.execute("DELETE FROM application_detail")
        # cursor.execute("DELETE FROM applicant_profile")
        cursor.execute("DROP TABLE IF EXISTS application_detail")
        cursor.execute("DROP TABLE IF EXISTS applicant_profile")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applicant_profile (
                applicant_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                first_name VARCHAR(100) DEFAULT NULL,
                last_name VARCHAR(100) DEFAULT NULL, 
                date_of_birth VARCHAR(100) DEFAULT NULL, 
                address VARCHAR(255) DEFAULT NULL, 
                phone_number VARCHAR(100) DEFAULT NULL
            )
        ''')

        # Insert data without applicant_id (auto-generated)
        for applicant in all_applicant_profile_data:
            cursor.execute("""
                INSERT INTO applicant_profile (first_name, last_name, date_of_birth, address, phone_number)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                applicant["first_name"],
                applicant["last_name"],
                applicant["date_of_birth"],
                applicant["address"],
                applicant["phone_number"],
            ))
            applicant_id = cursor.lastrowid
            applicant_ids.append(applicant_id)

        # Drop and recreate the application_detail table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS application_detail (
                detail_id INT NOT NULL AUTO_INCREMENT, 
                applicant_id INT NOT NULL, 
                application_role TEXT DEFAULT NULL, 
                cv_path TEXT,
                PRIMARY KEY (detail_id),
                FOREIGN KEY (applicant_id) REFERENCES applicant_profile(applicant_id)
            )
        ''')

        # Insert data into application_detail
        for application_detail in all_application_detail_data:
            cursor.execute("""
                INSERT INTO application_detail (applicant_id, application_role, cv_path)
                VALUES (%s, %s, %s)
            """, (
                random.choice(applicant_ids),
                application_detail["application_role"],
                application_detail["cv_path"]
            ))


        # # commit the data into the database
        conn.commit()

        # # close the connection
        cursor.close()
        conn.close()

    # if failed_files:
    #     print(f"\n Daftar file dengan error ({len(failed_files)} files):")
    #     for f in sorted(failed_files):
    #         print(f"- {f}")
    # else:
    #     print(f"jadi boy")

if __name__ == '__main__':
    setup()