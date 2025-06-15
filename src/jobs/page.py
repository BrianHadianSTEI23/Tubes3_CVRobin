
import flet as ft
import mysql.connector
from algorithm.encryptionModule import decrypt

def jobs(page : ft.Page):    

    # global variables
    max_jobs_to_display = 10
    password = "abrarbrianfaqih"

    # dummy data
    # format : application_role -> [total_applicant, cv_path]
    # jobs_data = {
    #     "Secretary": {
    #         "total_applicant": 4,
    #         "cv_path": [
    #             "cv_rudy_boul.pdf",
    #             "cv_andi_jaya.pdf",
    #             "cv_siti_kurnia.pdf",
    #             "cv_alex_tan.pdf"
    #         ],
    #     },
    #     "Treasurer": {
    #         "total_applicant": 3,
    #         "cv_path": [
    #             "cv_maya_halim.pdf",
    #             "cv_budi_santoso.pdf",
    #             "cv_nina_wang.pdf"
    #         ],
    #     },
    #     "Event Coordinator": {
    #         "total_applicant": 5,
    #         "cv_path": [
    #             "cv_yusuf_iswara.pdf",
    #             "cv_ina_saragih.pdf",
    #             "cv_ronaldo_tampubolon.pdf",
    #             "cv_henny_ang.pdf",
    #             "cv_dimas_rahardjo.pdf"
    #         ],
    #     },
    #     "Logistics": {
    #         "total_applicant": 2,
    #         "cv_path": [
    #             "cv_rizky_prasetyo.pdf",
    #             "cv_siska_amelia.pdf"
    #         ],
    #     },
    #     "Designer": {
    #         "total_applicant": 6,
    #         "cv_path": [
    #             "cv_joanna_lim.pdf",
    #             "cv_hendra_gunawan.pdf",
    #             "cv_felicia_tan.pdf",
    #             "cv_wahyudi_kurnia.pdf",
    #             "cv_agnes_devina.pdf",
    #             "cv_kelana_baskoro.pdf"
    #         ],
    #     }
    # }

    
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

    # Execute a query
    cursor.execute('''SELECT application_role, GROUP_CONCAT(applicant_id), GROUP_CONCAT(detail_id) AS applicant_ids
        FROM application_detail
        GROUP BY application_role;
''')

    # ################################### THIS WILL BE CHANGED INTO REAL DATA, BUT FOR NOW IS STILL DUMMY DATA ####################################33
    # Fetch and print the results 
    count = 0
    jobs_data = {}
    for el in cursor.fetchall():
        if count > max_jobs_to_display:
            break
        # debug
        # print(el)

        # init the jobs format
        job_data = {}

        # get the cv path
        cv_paths = []
        applicant_id_list = list(map(int, el[1].strip("'").split(",")))
        application_detail_list = list(map(int, el[2].strip("'").split(",")))
        for i, applicant_id in enumerate(applicant_id_list):
            # debug
            # print(f'''SELECT cv_path FROM application_detail WHERE application_detail.applicant_id = {applicant_id} AND application_detail.detail_id = {application_detail_list[i]}''') 
            
            cursor.execute(f'''SELECT cv_path FROM application_detail WHERE application_detail.applicant_id = {applicant_id} AND application_detail.detail_id = {application_detail_list[i]}''')
            cv_path_target = cursor.fetchall()
            
            # debug
            print(decrypt(password, cv_path_target[0][0]))
            cv_paths.append(decrypt(password, cv_path_target[0][0]))
        job_data.update({ "total_applicant" : len(cv_paths)})
        job_data.update({ "cv_path" : cv_paths })

        # put the job data into jobs_data
        jobs_data.update({ decrypt(password, el[0]) : job_data})
        count += 1

    cv_widgets = {}
    for job in jobs_data : 
        cv_paths_widgets = ft.Column()
        for path in jobs_data[job]["cv_path"] : 
            cv_paths_widgets.controls.append(
                ft.Container(
                    content = ft.Text(
                        path,
                        style=ft.TextStyle(
                            size=15,
                            color=ft.Colors.GREEN_900
                        ),
                    ),
                    expand=True,
                )
            )
        cv_paths_container = ft.Container(
                            content=cv_paths_widgets, 
                            bgcolor=ft.Colors.GREEN_100,
                            margin=ft.margin.Margin(left = 10, top=5, bottom=5, right= 10),
                            expand=True,
                            border_radius=20,
                            padding=10,
                            width=1000
                            )
        cv_widgets.update({f"{job}" : cv_paths_container})
    

    job_widgets = []
    for job_role in jobs_data:
        # wrap every data from database to be displayed on to the ui
        job_widgets.append(
            ft.Container(
                content= ft.Column(
                    controls=[
                        # job name
                        ft.Container(
                            content=ft.Row(
                                [
                                    # title
                                    ft.Text(
                                        job_role, 
                                        color="#efe9d9",
                                        size=20,
                                        style=ft.TextStyle(
                                                weight=ft.FontWeight.W_800,
                                                font_family="Tahoma"
                                            )
                                        ),
                                
                                    # jargon
                                    ft.Text(
                                        str(len(jobs_data[job_role]["cv_path"])), 
                                        color="#efe9d9",
                                        size =15,
                                        style=ft.TextStyle(
                                                weight=ft.FontWeight.W_300,
                                                italic=True,
                                                font_family="Consolas"
                                            )
                                        ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            expand_loose=True,
                            margin=ft.margin.Margin(left = 10, top=10, bottom=10, right=10),
                            padding=15,
                            bgcolor=ft.Colors.GREEN_900,
                            border_radius=20,
                        ),

                        # cv path texts
                        cv_widgets[job_role]

                    ],
                ),
                padding=5
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
                        "Jobs",
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
                *(job_widgets)
                
             ],
             horizontal_alignment=ft.CrossAxisAlignment.END,
             scroll=ft.ScrollMode.AUTO
        ),
        bgcolor="#efe9d9",
        padding=20,
        expand=True,  # Fills half the width
    )
    
    return ft.View(
        route = "/jobs",
        controls=[
            ft.Row(
                controls=[
                    left_section, 
                    right_section
                ],
                expand=True,
            )
        ],
    )