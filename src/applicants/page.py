

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
        }
    }

    
    # get all aplicants data from the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cvrobin"
    )

    # Create a cursor to execute queries
    cursor = conn.cursor()

    # Execute a query
    cursor.execute("SELECT * FROM applicant_profile")

    # ################################### THIS WILL BE CHANGED INTO REAL DATA, BUT FOR NOW IS STILL DUMMY DATA ####################################33
    # Fetch and print the results 
    applicant_widgets = []
    for applicant in applicants_data:
        # wrap every data from database to be displayed on to the ui
        applicant_widgets.append(
            ft.Container(
                content= ft.Column(
                    controls=[
                        # applicant name
                        ft.Column(
                            controls=[
                                ft.Text(
                                    applicants_data[applicant]["first_name"],
                                    ),
                                ft.Text(
                                    applicants_data[applicant]["last_name"],
                                    ),
                            ],
                            col=2
                        ),

                        # applicant birthdate, address, phone number
                        ft.Column(
                            controls=[
                                # birthdate
                                ft.Text(
                                        f"Birthdate : {applicants_data[applicant]["date_of_birth"]}",
                                        size= 25,
                                    ),

                                # address
                                ft.Text(
                                        f"Address : {applicants_data[applicant]["address"]}",
                                        size= 25,
                                    ),

                                # phone number
                                ft.Text(
                                        f"Phone Number : {applicants_data[applicant]["phone_number"]}",
                                        size= 25,
                                    ),
                            ],
                            col=2
                        ),
                    ],
                    col=2
                ),
                expand=True,
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
                *applicant_widgets
                
             ],
        ),
        bgcolor="#efe9d9",
        padding=20,
        expand=True,  # Fills half the width
    )

    return ft.View(
        route = "/applicants",
        controls=[
            ft.Row(
                controls=[
                    # this is placeholder
                    left_section, 
                    right_section
                ],
                expand=True
            )
        ]
    )