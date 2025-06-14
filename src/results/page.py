
import flet as ft
import mysql.connector
from summary.page import summary
from viewCV.page import viewCV
from algorithm.encryptionModule import decrypt
from algorithm.ahoCorasick import ahoCorasickMatch
from algorithm.boyerMoore import boyerMooreMatch
from algorithm.knuthMorrisPratt import knuthMorrisPrattMatch
from algorithm.levenshteinDistance import fuzzyMatch
from time import time
from algorithm.preprocessCV import CV

def results(page : ft.Page, keyword_list : list[str], cv_count_to_search : int, search_algorithm_to_search : str):

    # global variables
    found_count = 0
    threshold = 2
    password = "abrarbrianfaqih"

    # dummy data
    # results_data = {
    #     1: {
    #         "first_name": "Rudy",
    #         "last_name": "Boul",
    #         "date_of_birth": "1234-09-12",
    #         "address": "Ganesha St No. 39, Bandung, West Java, Indonesia",
    #         "phone_number": "0291831842",
    #         "match_keywords" : [
    #             {
    #                 "Java" : 2,
    #                 "Python" : 1,
    #                 "Programming" : 2,
    #             }
    #         ],
    #         "cv_path" : "cv_rudy_boul",
    #         "applicant_id" : 1
    #     },
    #     2: {
    #         "first_name": "Dina",
    #         "last_name": "Hartono",
    #         "date_of_birth": "1996-02-24",
    #         "address": "Jl. Asia Afrika No. 12, Bandung, West Java, Indonesia",
    #         "phone_number": "081234567890",
    #         "match_keywords" : [
    #             {
    #                 "Programming" : 2,
    #                 "Python" : 1,
    #             }
    #         ],
    #         "cv_path": "cv_dina_hartono",
    #         "applicant_id" : 2
    #     },
    #     3: {
    #         "first_name": "Andi",
    #         "last_name": "Wijaya",
    #         "date_of_birth": "1988-11-15",
    #         "address": "Jl. Braga No. 3, Bandung, West Java, Indonesia",
    #         "phone_number": "082112345678",
    #         "match_keywords" : [
    #             {
    #                 "Java" : 2,
    #                 "Python" : 1,
    #             }
    #         ],
    #         "cv_path" : "cv_andi_wijaya",
    #         "applicant_id" : 3
    #     },
    # }

    def go_to_summary(e, id_applicant : int):
        page.views.clear()
        page.views.append(summary(page, id_applicant))
        page.update()

    def view_cv(e, id_applicant: int):
        page.views.clear()
        page.views.append(viewCV(page, id_applicant))
        page.update()

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
    cursor.execute("SELECT * FROM applicant_profile NATURAL JOIN application_detail")

    # fetch all
    # cursor.fetchall = (applicant_id, first_name, last_name, dob, address, phone, detail_id, application_role, cv_path)
    start_time = time()
    results_data = {}
    for el in cursor.fetchall():
        if (found_count < int(cv_count_to_search)):

            # debug
            # print(f"applicant id : {el[0]}")
            # print(f"first name : {decrypt(password, el[1])}")
            # print(f"last_name : {decrypt(password, el[2])}")
            # print(f"date of birth : {decrypt(password, el[3])}")
            # print(f"address : {decrypt(password, el[4])}")
            # print(f"phone number : {decrypt(password, el[5])}")
            # print(f"detail id : {el[6]}")
            # print(f"application role: {decrypt(password, el[7])}")
            # print(f"cv path : {decrypt(password, el[8])}")
            # print("-" * 40)

            # update needed data
            applicant_id_data = {}
            applicant_id_data.update({"applicant_id" : el[0]})
            applicant_id_data.update({"first_name" : decrypt(password, el[1])})
            applicant_id_data.update({"last_name" : decrypt(password, el[2])})
            applicant_id_data.update({"date_of_birth" :  decrypt(password, el[3])})
            applicant_id_data.update({"address" :  decrypt(password, el[4])})
            applicant_id_data.update({"phone_number" :  decrypt(password, el[5])})
            applicant_id_data.update({"detail_id": el[6]})
            applicant_id_data.update({"application_role" :  decrypt(password, el[7])})
            applicant_id_data.update({"cv_path" :  decrypt(password, el[8])})

            # read the cv path
            keyword_match_data = {}
            cv_data = CV(decrypt(password, el[8]))
            if (search_algorithm_to_search == "Boyer-Moore"):
                # scan using boyer moore
                keyword_match_data = boyerMooreMatch(cv_data.continuousText, keyword_list)
                for keyword in keyword_list: # there are no keyword match -> fuzzy matching
                    if keyword not in keyword_match_data:
                        fuzzy_result = fuzzyMatch(list(keyword), cv_data.continuousText, threshold)
                        if fuzzy_result:
                            keyword_match_data.update({keyword : fuzzyMatch(list(keyword), cv_data.continuousText, threshold)})

                # check if all the keyword exist and if yes, add the found count
                all_exist = True
                for keyword in keyword_list:
                    if keyword not in keyword_match_data:
                        all_exist = False
                
                if all_exist : 
                    applicant_id_data.update({"match_keywords" : keyword_match_data})
                    found_count += 1
                    
            elif (search_algorithm_to_search == "Knuth-Morris-Pratt"):
                # scan using kmp
                keyword_match_data = knuthMorrisPrattMatch(cv_data.continuousText, keyword_list)
                for keyword in keyword_list: # there are no keyword match -> fuzzy matching
                    if keyword not in keyword_match_data:
                        fuzzy_result = fuzzyMatch(list(keyword), cv_data.continuousText, threshold)
                        if fuzzy_result:
                            keyword_match_data.update({keyword : fuzzyMatch(list(keyword), cv_data.continuousText, threshold)})

                # check if all the keyword exist and if yes, add the found count
                all_exist = True
                for keyword in keyword_list:
                    if keyword not in keyword_match_data:
                        all_exist = False
                
                if all_exist : 
                    applicant_id_data.update({"match_keywords" : keyword_match_data})
                    found_count += 1
            elif (search_algorithm_to_search == "Aho-Corasick"):
                # scan using ah
                keyword_match_data = ahoCorasickMatch(cv_data.continuousText, keyword_list)
                for keyword in keyword_list: # there are no keyword match -> fuzzy matching
                    if keyword not in keyword_match_data:
                        fuzzy_result = fuzzyMatch(list(keyword), cv_data.continuousText, threshold)
                        if fuzzy_result:
                            keyword_match_data.update({keyword : fuzzyMatch(list(keyword), cv_data.continuousText, threshold)})

                # check if all the keyword exist and if yes, add the found count
                all_exist = True
                for keyword in keyword_list:
                    if keyword not in keyword_match_data:
                        all_exist = False
                
                if all_exist : 
                    applicant_id_data.update({"match_keywords" : keyword_match_data})
                    found_count += 1
            results_data.update({el[0] : applicant_id_data})

    # count time
    end_time = time()
    process_time = end_time - start_time



    # ################################### THIS WILL BE CHANGED INTO REAL DATA, BUT FOR NOW IS STILL DUMMY DATA ####################################33
    # Fetch and print the results 
    result_widgets = []
    for result in results_data:
        # wrap every data from database to be displayed on to the ui
        result_widgets.append(
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
                                                results_data[result]["first_name"] + " " + results_data[result]["last_name"],
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
                                                        f"Birthdate : {results_data[result]["date_of_birth"]}",
                                                        style=ft.TextStyle(
                                                            size=15,
                                                            weight=ft.FontWeight.W_400,
                                                            color=ft.Colors.GREEN_900
                                                        )
                                                    ),

                                                # address
                                                ft.Text(
                                                        f"Address : {results_data[result]["address"]}",
                                                        style=ft.TextStyle(
                                                            size=15,
                                                            weight=ft.FontWeight.W_400,
                                                            color=ft.Colors.GREEN_900
                                                        )
                                                    ),

                                                # phone number
                                                ft.Text(
                                                        f"Phone Number : {results_data[result]["phone_number"]}",
                                                        style=ft.TextStyle(
                                                            size=15,
                                                            weight=ft.FontWeight.W_400,
                                                            color=ft.Colors.GREEN_900
                                                        )
                                                    ),
                                            ]
                                        )
                                    ),
                                    
                                    # buttons
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Container(
                                                        content = ft.ElevatedButton(
                                                        text="Summary",
                                                        bgcolor=ft.Colors.GREEN_900,
                                                        color="#efe9d9",
                                                        on_click=lambda e, applicant_id=results_data[result]["applicant_id"]: go_to_summary(e, applicant_id)
                                                    ),
                                                    padding=10
                                                ),
                                                ft.Container(
                                                        content = ft.ElevatedButton(
                                                        text="View CV",
                                                        bgcolor=ft.Colors.GREEN_900,
                                                        color="#efe9d9",
                                                        on_click=lambda e, applicant_id=results_data[result]["applicant_id"]: view_cv(e, applicant_id)
                                                    ),
                                                    padding=10
                                                ),
                                            ]
                                        ),
                                    )
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
                        "Results (" + str(process_time) + ") s",
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
                *result_widgets
                
             ],
             horizontal_alignment=ft.CrossAxisAlignment.END,
             scroll=ft.ScrollMode.AUTO
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
                ],
                expand=True,
            )
        ]
    )