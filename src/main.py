'''
algorithm 
1. this project is composed of 3 main parts : algorithm & cv parsing, UI, database integration

algorithm and cv parsing
1. do parsing all text from cv into a variable
2. do pattern matching using regex accroding to the inputted value of keywords and put the 
result into another variable 
3. do pattern matching KMP and bayer moore. First, do exact matching, then if not found at all, do fuzzy matching
 with similarity is counted using levenshtein distance for every word and then summed up
4. those summed up is then sorted descending
5. pick 5 of the top algorithm

UI Feature minimal
1. keyword
2. mode : kmp, bm, aho corasick
3. how many top results
3.5 tombol search
4. results : 
a. time execution (global)
b. comparison done (global)
c. applicant name
d. what matches? if using fuzzy, output the score
e. summary [new page] : name, birthdate, address, phone (personal data), skills (do parsing again), 
job history (position, year, achievements), education (bachlelor, univ, year)
f. view cv : only image (using pdf2image)

Database integration
1. basically you will check all code that correspond to searching in the database
'''

import flet as ft
from home.page import homepage
from applicants.page import applicants
from jobs.page import jobs
from results.page import results

# main program is only for changing data
def main(page : ft.Page):
    # initialization
    page.title = "CVRobin : CV Analyzer"
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 1000
    page.window.width = 1333.3
    page.expand=True

    # route changing
    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(homepage(page))
        elif page.route == "/applicants":
            page.views.append(applicants(page))
        # elif page.route == "/results":
        #     page.views.append(results(page))
        elif page.route == "/jobs":
            page.views.append(jobs(page))
        page.update()
    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__" :
    ft.app(target=main)
