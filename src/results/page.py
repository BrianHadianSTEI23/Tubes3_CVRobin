
import flet as ft
import mysql.connector

def results(page : ft.Page):

    # dummy data
    # format : application_role -> [total_applicant, cv_path]
    jobs_data = {
        "Secretary": {
            "total_applicant": 4,
            "cv_path": [
                "cv_rudy_boul.pdf",
                "cv_andi_jaya.pdf",
                "cv_siti_kurnia.pdf",
                "cv_alex_tan.pdf"
            ],
        },
        "Treasurer": {
            "total_applicant": 3,
            "cv_path": [
                "cv_maya_halim.pdf",
                "cv_budi_santoso.pdf",
                "cv_nina_wang.pdf"
            ],
        },
        "Event Coordinator": {
            "total_applicant": 5,
            "cv_path": [
                "cv_yusuf_iswara.pdf",
                "cv_ina_saragih.pdf",
                "cv_ronaldo_tampubolon.pdf",
                "cv_henny_ang.pdf",
                "cv_dimas_rahardjo.pdf"
            ],
        },
        "Logistics": {
            "total_applicant": 2,
            "cv_path": [
                "cv_rizky_prasetyo.pdf",
                "cv_siska_amelia.pdf"
            ],
        },
        "Designer": {
            "total_applicant": 6,
            "cv_path": [
                "cv_joanna_lim.pdf",
                "cv_hendra_gunawan.pdf",
                "cv_felicia_tan.pdf",
                "cv_wahyudi_kurnia.pdf",
                "cv_agnes_devina.pdf",
                "cv_kelana_baskoro.pdf"
            ],
        }
    }

    
    # get all aplicants data from the database
    # conn = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="",
    #     database="cvrobin"
    # )

    # # Create a cursor to execute queries
    # cursor = conn.cursor()

    # # Execute a query
    # cursor.execute("SELECT * FROM application_detail")

    # ################################### THIS WILL BE CHANGED INTO REAL DATA, BUT FOR NOW IS STILL DUMMY DATA ####################################33
    # Fetch and print the results 
    cv_widgets = {}
    for job in jobs_data : 
        cv_paths = []
        for path in jobs_data[job]["cv_path"] : 
            cv_paths.append(ft.Text(path))
        cv_widgets.update({f"{job}" : cv_paths})

    job_widgets = []
    for job in jobs_data:
        # wrap every data from database to be displayed on to the ui
        job_widgets.append(
            ft.Container(
                content= ft.Column(
                    controls=[
                        # job name
                        ft.Column(
                            controls=[
                                ft.Text(job),
                                ft.Text(jobs_data[job]["total_applicant"])
                            ],
                            col= 2
                        ),

                        # cv path texts
                        *(cv_widgets[job])

                    ],
                    col=2
                ),
                expand=True,
                padding=5
            )
        )


    # Close the cursor and connection
    # cursor.close()
    # conn.close()

    # left section construct (dark green)
    left_section = ft.Container(
        content=ft.Column(
            controls= [
                ft.Text("Home", color="#efe9d9"),
                ft.Text("Applicants", color="#efe9d9"),
                ft.Text("Jobs", color="#efe9d9")
                ],
        ),
        bgcolor=ft.Colors.GREEN_900,
        padding=20,
        width=333.3,
    )


    # right section construct (cream)
    right_section = ft.Container(
        content=ft.Column(
            [
                # BANNER + JARGON
                ft.Row(
                    [
                        # title
                        ft.Text(
                            "CVRobin", 
                            color=ft.Colors.GREEN_900,
                            size=50
                            ),
                     
                        # jargon
                        ft.Text(
                            "Your reliable HRD substitute", 
                            color=ft.Colors.GREEN_900,
                            size =30
                            ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # BANNER SECTION 
                ft.Text(
                    "Applicants", 
                    color=ft.Colors.GREEN_900,
                    rtl = True,
                    size=25
                    ),

                # applicants
                *job_widgets
                
             ],
        ),
        bgcolor="#efe9d9",
        padding=20,
        expand=True,  # Fills half the width
    )
    
    
    return ft.View(
        route = "/results",
        controls=[
            ft.Row(
                controls=[
                    left_section,
                    right_section
                ]
            )
        ]
    )