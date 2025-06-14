
import flet as ft
import mysql.connector
from algorithm.preprocessCV import CV
from algorithm.encryptionModule import decrypt

def summary(page : ft.Page, id_applicant : int):

    # global variable
    password = "abrarbrianfaqih"

    # dummy data
    summary_data = {
        "first_name": "Rudy",
        "last_name": "Boul",
        "date_of_birth": "1234-09-12",
        "address": "Ganesha St No. 39, Bandung, West Java, Indonesia",
        "phone_number": "0291831842",
        "match_keywords" : [
            {
                "Java" : 2,
                "Python" : 1,
                "Programming" : 2,
            }
        ],
        "cv_path" : "cv_rudy_boul",
        "applicant_id" : 1,
        "application_role" : "Designer",
        "skills" : [
            "React",
            "Java",
            "DevOps",
        ],
        "jobHistory" : [
            {
                "position" : "CTO",
                "range" : "2003-2013",
                "description": "leading technology"
            },
            {
                "position" : "CEO",
                "range" : "2001",
                "description" : "lead nothing"
            }
        ],
        "skills" : [
            "React",
            "Java",
            "DevOps",
        ],
        "education" : [
            {
                "institution": "ITB",
                "studyProgram": "IF",
                "rangeYear": "2000-2003"
            },
            {
                "institution": "Harvard",
                "studyProgram": "Math",
                "rangeYear": "1999-2000"
            }
        ]
    }
    
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

    # # Execute a query
    cursor.execute(f"SELECT * FROM applicant_profile NATURAL JOIN application_detail WHERE applicant_profile.applicant_id = {id_applicant}")

    # fetch all
    # cursor.fetchall = (applicant_id, first_name, last_name, dob, address, phone, detail_id, application_role, cv_path)
    summary_data = {}
    for el in cursor.fetchall():
        cv_data = CV(decrypt(password, el[8]))

        # update everything that can be updated 
        summary_data = {}
        summary_data.update({"applicant_id" : el[0]})
        summary_data.update({"first_name" : decrypt(password, el[1])})
        summary_data.update({"last_name" : decrypt(password, el[2])})
        summary_data.update({"date_of_birth" :  decrypt(password, el[3])})
        summary_data.update({"address" :  decrypt(password, el[4])})
        summary_data.update({"phone_number" :  decrypt(password, el[5])})
        summary_data.update({"detail_id": el[6]})
        summary_data.update({"application_role" :  decrypt(password, el[7])})
        summary_data.update({"cv_path" :  decrypt(password, el[8])})

        # update summary
        # summary_content = cv_data._parse_text()["summary"]

        # update skills
        skills_content = cv_data._parse_text()["skills"]
        summary_data.update({"skills" : skills_content})

        # update jobhistory
        jobHistory_content = cv_data._parse_text()["jobHistory"]
        summary_data.update({"jobHistory" : jobHistory_content})

        # update education
        education_content = cv_data._parse_text()["education"]
        summary_data.update({"education" : education_content})


    # skill widget
    skills_widget = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(
                    "Skills",
                    color="#efe9d9",
                )
            ]
        ),
        bgcolor=ft.Colors.GREEN_900,
        padding=10,
        border_radius=15,
    )
    for skill in summary_data["skills"]:
        skills_widget.content.controls.append(
            ft.Container(
                content=ft.Text(
                    skill,
                    color="#efe9d9",
                ),
                bgcolor=ft.Colors.GREEN_500,
                padding=10,
                border_radius=15,
            ),
        )

    # job history widget
    jobHistory_widget = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Job History",
                    color="#efe9d9",
                )
            ]
        ),
        bgcolor=ft.Colors.GREEN_900,
        padding=10,
        expand=True,
        width=1000,
        border_radius=15,
    )
    for jobHistory in summary_data["jobHistory"]:
        jobHistory_widget.content.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            jobHistory["position"],
                            color="#efe9d9",
                        ),

                        ft.Text(
                            jobHistory["range"],
                            color="#efe9d9",
                        ),

                        ft.Text(
                            jobHistory["description"],
                            color="#efe9d9",
                        )
                    ]
                ),
                bgcolor=ft.Colors.GREEN_500,
                padding=10,
                border_radius=15,
                width=1000,
            ),
        )

    # education widget
    education_widget = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Education",
                    color="#efe9d9",
                )
            ]
        ),
        bgcolor=ft.Colors.GREEN_900,
        padding=10,
        width=1000,
        border_radius=15,
    )
    for education in summary_data["education"]:
        education_widget.content.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            education["institution"],
                            color="#efe9d9",
                        ),

                        ft.Text(
                            education["studyProgram"],
                            color="#efe9d9",
                        ),

                        ft.Text(
                            education["rangeYear"],
                            color="#efe9d9",
                        )
                    ]
                ),
                bgcolor=ft.Colors.GREEN_500,
                padding=10,
                border_radius=15,
                width=1000,
            ),
        )
    
    # Fetch and print the results 
    summary_widgets = []
    # for key in summary_data:
        # wrap every data from database to be displayed on to the ui
    summary_widgets.append(
        ft.Container(
            content= ft.Column(
                controls=[
                    # applicant name
                    ft.Container(
                        content = ft.Column(
                            controls=[
                                ft.Row(
                                    controls = [
                                        ft.Text(
                                            summary_data["first_name"] + " " + summary_data["last_name"],
                                            style=ft.TextStyle(
                                                    size=20,
                                                    weight=ft.FontWeight.W_500,
                                                    word_spacing=5,
                                                    color="#efe9d9"
                                                )
                                            ),
                                    ]
                                )
                            ],
                            expand=True,
                        ),
                        padding=ft.padding.Padding(left=15, right=15, top=10, bottom=5),
                        bgcolor=ft.Colors.GREEN_900,
                        expand=True,
                        border_radius=15,
                    ),

                    # applicant birthdate, address, phone number
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content = ft.Column(
                                        controls = [
                                            # birthdate
                                            ft.Text(
                                                    f"Birthdate : {summary_data["date_of_birth"]}",
                                                    style=ft.TextStyle(
                                                        size=15,
                                                        weight=ft.FontWeight.W_400,
                                                        color=ft.Colors.GREEN_900
                                                    )
                                                ),

                                            # address
                                            ft.Text(
                                                    f"Address : {summary_data["address"]}",
                                                    style=ft.TextStyle(
                                                        size=15,
                                                        weight=ft.FontWeight.W_400,
                                                        color=ft.Colors.GREEN_900
                                                    )
                                                ),

                                            # phone number
                                            ft.Text(
                                                    f"Phone Number : {summary_data["phone_number"]}",
                                                    style=ft.TextStyle(
                                                        size=15,
                                                        weight=ft.FontWeight.W_400,
                                                        color=ft.Colors.GREEN_900
                                                    )
                                                ),
                                        ]
                                    )
                                ),
                                
                                # skills
                                skills_widget,

                                # job history
                                jobHistory_widget,

                                # education
                                education_widget,
                            ],
                        ),
                        bgcolor=ft.Colors.GREEN_100,
                        border_radius=20,
                        padding=10,
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),
            expand=True,
            padding=5,
        )
    )


    # Close the cursor and connection
    cursor.close()
    conn.close()

    # left section construct (dark green)
    left_section = ft.Container(
        content=ft.Column(
            controls= [
                    ft.Container(
                        content = ft.Row(
                            controls = [
                                ft.ElevatedButton(
                                    text="Home",
                                    color=ft.Colors.GREEN_900,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(size=20),
                                        padding=20,  # internal padding (vertical, horizontal)
                                        bgcolor=ft.Colors.GREEN_100,
                                        alignment=ft.alignment.top_left
                                    ),
                                    expand=True,  # allows button to grow inside expanding parent
                                    on_click=lambda e: page.go("/")
                                ),
                            ],
                            expand=True,  # allows container to grow horizontally
                            spacing=20,
                        ),
                        margin=ft.margin.symmetric(horizontal=20, vertical=20),
                    ),
                    ft.Container(
                        content = ft.Row(
                            controls = [
                                ft.ElevatedButton(
                                    text="Jobs",
                                    color=ft.Colors.GREEN_900,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(size=20),
                                        padding=20,  # internal padding (vertical, horizontal)
                                        bgcolor=ft.Colors.GREEN_100,
                                        alignment=ft.alignment.top_left
                                    ),
                                    expand=True,  # allows button to grow inside expanding parent
                                    on_click=lambda e: page.go("/jobs")
                                ),
                            ],
                            expand=True,  # allows container to grow horizontally
                            spacing=20,
                        ),
                        margin=ft.margin.symmetric(horizontal=20, vertical=20),
                    ),
                    ft.Container(
                        content = ft.Row(
                            controls = [
                                ft.ElevatedButton(
                                    text="Applicants",
                                    color=ft.Colors.GREEN_900,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(size=20),
                                        padding=20,  # internal padding (vertical, horizontal)
                                        bgcolor=ft.Colors.GREEN_100,
                                        alignment=ft.alignment.top_left
                                    ),
                                    expand=True,  # allows button to grow inside expanding parent
                                    on_click=lambda e: page.go("/applicants")
                                ),
                            ],
                            expand=True,  # allows container to grow horizontally
                            spacing=20,
                        ),
                        margin=ft.margin.symmetric(horizontal=20, vertical=20),
                    )
                ],
        ),
        bgcolor=ft.Colors.GREEN_900,
        padding=ft.padding.Padding(left = 30, right = 30, top = 200, bottom=30),
        width=333.3,
    )

    # right section construct (cream)
    right_section = ft.Container(
        content=ft.Column(
            [
                # BANNER + JARGON
                ft.Container(
                    content=ft.Row(
                        [
                            # title
                            ft.Text(
                                "CVRobin", 
                                color=ft.Colors.GREEN_900,
                                size=50,
                                style=ft.TextStyle(
                                        weight=ft.FontWeight.W_800,
                                        font_family="Tahoma"
                                    )
                                ),
                        
                            # jargon
                            ft.Text(
                                "Your reliable HRD substitute", 
                                color=ft.Colors.GREEN_900,
                                size =30,
                                style=ft.TextStyle(
                                        weight=ft.FontWeight.W_100,
                                        italic=True,
                                        font_family="Consolas"
                                    )
                                ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    expand_loose=True,
                    margin=30,
                    padding=10,
                ),

                # BANNER SECTION 
                ft.Container(
                    content=ft.Text(
                        "Summary",
                        color="#efe9d9",
                        size=25,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    bgcolor=ft.Colors.GREEN_900,
                    padding=20,
                    margin=ft.margin.symmetric(vertical=10),
                    alignment=ft.alignment.center_right,  # align content inside container
                    width=800
                ),

                # applicants
                *summary_widgets
                
             ],
             horizontal_alignment=ft.CrossAxisAlignment.END,
             scroll=ft.ScrollMode.AUTO
        ),
        bgcolor="#efe9d9",
        padding=20,
        expand=True,  # Fills half the width
    )
    
    
    return ft.View(
        route = "/summary",
        controls=[
            ft.Row(
                controls=[
                    left_section,
                    right_section
                ],
                expand=True,
            )
        ]
    )