import wikipedia

country_content = dict()

countries = ["Cuba"]

for country in countries:
    # content = wikipedia.page(title=country, auto_suggest=False).section("Demographics") # auto_suggest=False fix problems with Cuba's and Canada's pages upload 
  
    # content_1 = wikipedia.page(title=country, auto_suggest=False).section("Administrative divisions") 

    # content_2 = wikipedia.page(title=country, auto_suggest=False).section("Government and politics") 

    content_3 = wikipedia.page(title=country, auto_suggest=False).links


    # for goverment and politics
    content_political_div[country] = wikipedia.page(title=country, auto_suggest=False).section("Political divisions")
    if content_political_div[country] == None:
        content_political_div[country] = wikipedia.page(title=country, auto_suggest=False).section("Political divisions")
    if content_political_div[country] == None:
        content_political_div[country] = wikipedia.page(title=country, auto_suggest=False).section("Provinces and territories")
    if content_political_div[country] == None:
        content_political_div[country] = wikipedia.page(title=country, auto_suggest=False).section("Administrative divisions")

    


    country_content[country] = content_3
            
print(country_content)
