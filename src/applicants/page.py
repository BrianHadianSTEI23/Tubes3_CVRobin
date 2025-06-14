

import flet as ft
import mysql.connector

def applicants(page : ft.Page) :

    # dummy data
    # format : appicant_id -> [first_name, last_name, dob, address, phone_number]
    applicants_data = {
        1: {
            "first_name": "Rudy",
            "last_name": "Boul",
            "date_of_birth": "1234-09-12",
            "address": "Ganesha St No. 39, Bandung, West Java, Indonesia",
            "phone_number": "0291831842"
        },
        2: {
            "first_name": "Dina",
            "last_name": "Hartono",
            "date_of_birth": "1996-02-24",
            "address": "Jl. Asia Afrika No. 12, Bandung, West Java, Indonesia",
            "phone_number": "081234567890"
        },
        3: {
            "first_name": "Andi",
            "last_name": "Wijaya",
            "date_of_birth": "1988-11-15",
            "address": "Jl. Braga No. 3, Bandung, West Java, Indonesia",
            "phone_number": "082112345678"
        },
        4: {
            "first_name": "Siti",
            "last_name": "Rahmawati",
            "date_of_birth": "1992-05-08",
            "address": "Jl. Dago Atas No. 45, Bandung, West Java, Indonesia",
            "phone_number": "081987654321"
        },
        5: {
            "first_name": "Budi",
            "last_name": "Santoso",
            "date_of_birth": "2000-07-30",
            "address": "Jl. Setiabudi No. 18, Bandung, West Java, Indonesia",
            "phone_number": "083812341234"
        },
        6: {
            "first_name": "Budi",
            "last_name": "Santoso",
            "date_of_birth": "2000-07-30",
            "address": "Jl. Setiabudi No. 18, Bandung, West Java, Indonesia",
            "phone_number": "083812341234"
        },
        7: {
            "first_name": "Budi",
            "last_name": "Santoso",
            "date_of_birth": "2000-07-30",
            "address": "Jl. Setiabudi No. 18, Bandung, West Java, Indonesia",
            "phone_number": "083812341234"
        },
        8: {
            "first_name": "Budi",
            "last_name": "Santoso",
            "date_of_birth": "2000-07-30",
            "address": "Jl. Setiabudi No. 18, Bandung, West Java, Indonesia",
            "phone_number": "083812341234"
        },
        9: {
            "first_name": "Budi",
            "last_name": "Santoso",
            "date_of_birth": "2000-07-30",
            "address": "Jl. Setiabudi No. 18, Bandung, West Java, Indonesia",
            "phone_number": "083812341234"
        },
        10: {
            "first_name": "Budi",
            "last_name": "Santoso",
            "date_of_birth": "2000-07-30",
            "address": "Jl. Setiabudi No. 18, Bandung, West Java, Indonesia",
            "phone_number": "083812341234"
        },
        11: {
            "first_name": "Budi",
            "last_name": "Santoso",
            "date_of_birth": "2000-07-30",
            "address": "Jl. Setiabudi No. 18, Bandung, West Java, Indonesia",
            "phone_number": "083812341234"
        },
    }

    
    # get all aplicants data from the database
    # conn = mysql.connector.connect(
    #     host="mysql-66af4eb-cvrobin.g.aivencloud.com",
    #     user="avnadmin",
    #     password="AVNS_OwS64toTSD7MkC29m2-",
    #     database="defaultdb",
    #     port = 10647
    # )

    # # Create a cursor to execute queries
    # cursor = conn.cursor()

    # # Execute a query
    # cursor.execute("SELECT * FROM applicant_profile")

    # ################################### THIS WILL BE CHANGED INTO REAL DATA, BUT FOR NOW IS STILL DUMMY DATA ####################################33
    # Fetch and print the results 
    applicant_widgets = ft.Container(
        content= ft.GridView(
                max_extent=333 + 10,  # each cell's max width
                child_aspect_ratio=1.7,  # width/height ratio
                spacing=15,
                run_spacing=10,
                expand=True,
                auto_scroll=True
            ),
        margin=ft.margin.symmetric(horizontal=20),
        expand=True,
    )
    for applicant in applicants_data:
        widget = ft.Container(
                content= ft.Column(
                    controls=[
                        # applicant name
                        ft.Container(
                            content = ft.Column(
                                controls=[
                                    ft.Text(
                                        applicants_data[applicant]["first_name"] + " " + applicants_data[applicant]["last_name"],
                                        style=ft.TextStyle(
                                                size=20,
                                                weight=ft.FontWeight.W_500,
                                                word_spacing=5,
                                                color="#efe9d9"
                                            )
                                        ),
                                ],
                            ),
                            padding=ft.padding.Padding(left=15, right=15, top=10, bottom=5)
                        ),

                        # applicant birthdate, address, phone number
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    # birthdate
                                    ft.Text(
                                            f"Birthdate : {applicants_data[applicant]["date_of_birth"]}",
                                            style=ft.TextStyle(
                                                size=15,
                                                weight=ft.FontWeight.W_400,
                                                color=ft.Colors.GREEN_900
                                            )
                                        ),

                                    # address
                                    ft.Text(
                                            f"Address : {applicants_data[applicant]["address"]}",
                                            style=ft.TextStyle(
                                                size=15,
                                                weight=ft.FontWeight.W_400,
                                                color=ft.Colors.GREEN_900
                                            )
                                        ),

                                    # phone number
                                    ft.Text(
                                            f"Phone Number : {applicants_data[applicant]["phone_number"]}",
                                            style=ft.TextStyle(
                                                size=15,
                                                weight=ft.FontWeight.W_400,
                                                color=ft.Colors.GREEN_900
                                            )
                                        ),
                                ],
                            ),
                            bgcolor=ft.Colors.GREEN_100,
                            border_radius=20,
                            padding=10
                        )
                    ],
                ),
                expand=True,
            )
        # wrap every data from database to be displayed on to the ui
        applicant_widgets.content.controls.append(  # Append to the GridView!
                ft.Container(
                    content=ft.Row(
                        controls=[widget],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    bgcolor=ft.Colors.GREEN_800,
                    border_radius=20,
                    expand=True,
                )
            )


    # Close the cursor and connection
    # cursor.close()
    # conn.close()

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

    # right bottom section construct (inside right section)
    right_bottom_section = ft.Container(
                        content=ft.Column(
                            controls=[
                                    applicant_widgets,
                                ],
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=10,
                    alignment=ft.alignment.center_left,
                    expand=True,
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
                    margin=30,
                    padding=10,
                ),

                # BANNER SECTION 
                ft.Container(
                    content=ft.Text(
                        "Applicants",
                        color="#efe9d9",
                        size=25,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    bgcolor=ft.Colors.GREEN_900,
                    padding=20,
                    margin=ft.margin.symmetric(vertical=20),
                    alignment=ft.alignment.center_right,  # align content inside container
                    width=800
                ),

                # Applicants
                right_bottom_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
            # scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        bgcolor="#efe9d9",
        expand=True,  # Fills half the width
        height=1000,
    )

    return ft.View(
        route="/applicants",
        controls=[
            ft.Column(  
                controls=[
                    ft.Row(
                        controls=[
                            left_section,
                            right_section,
                        ],
                        expand=True,
                    )
                ],
                expand=True ,
            )
        ],
    )
