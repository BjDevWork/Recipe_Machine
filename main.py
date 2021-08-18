import requests
import dominate
from dominate.tags import *
import re

def request_api_data():
	url = "https://api.apify.com/v2/datasets/RKONt01OyaZSQnYFI/items?limit=10&format=json"
	res = requests.get(url)

	if res.status_code != 200:
		raise RuntimeError(f'error fetching: {res.status_code}, Please check api and try again')
	return res

response = request_api_data()

def create_page():
	doc = dominate.document(title='Your Weekly Meal Plan')

	with doc.head:
		meta(charset='UTF-8')
		style("""\
			.container {
			  display: grid; 
			  grid-template-columns: 0.9fr; 
			  grid-template-rows: 0.2fr 1.9fr; 
			  gap: 0px 0px; 
			  grid-template-areas: 
			    'title'
			    'content'; 
			}
			.title {
			  justify-self: center; 
			  grid-area: title; 
			}
			.content {
			  display: grid; 
			  grid-template-columns: 1fr 1fr; 
			  grid-template-rows: 1fr; 
			  gap: 0px 0px; 
			  grid-template-areas: 
			    'recipe-info directions'; 
			  grid-area: content; 
			}
			.recipe-info {
			  display: grid; 
			  grid-template-columns: 1fr; 
			  grid-template-rows: 1.5fr 0.5fr; 
			  gap: 0px 0px; 
			  grid-template-areas: 
			    'ingredients'
			    'info'; 
			  grid-area: recipe-info; 
			}
			.ingredients { grid-area: ingredients; }
			.info { grid-area: info; }
			.directions { grid-area: directions; }

			""")

	with doc:
		h1('Your Weekly Meal Plan')

		for item in response.json():

			with div(cls='container'):
				with div(cls='title'):
					h2(item['name'])
				with div(cls='content'):
					with div(cls='recipe-info'):
						with div(cls='ingredients'):
							ingredients_list = re.split(r'[,]\s+([^a-zA-Z])', item['ingredients'])
							with ul():
								skip_next = False
								for count,food in enumerate(ingredients_list):
									if skip_next == True :
										skip_next = False
										continue
									if len(food) == 1:
										li(ingredients_list[count] + ingredients_list[count + 1])
										skip_next = True
									else:
										li(food)
							
						with div(cls='info'):
							with ul():
								li('calories: ' + item['calories'])
								li('prep time: ' + item['prep'])
								li('cook time: ' + item['cook'])
								li('ready time: ' + item['ready in'])
					with div(cls='directions'):
						directions_list = re.split(r'[0-9][.]', item['directions'])
						with ul():
							for count,direct in enumerate(directions_list[1:]):
								li(str(str(count + 1) + '. ' + direct))

				# p(item['name'])
				# p(item['ingredients'])
	return doc

def parse_card():
	pass

my_doc = create_page()


with open('index.html', 'w', encoding='utf-8', errors='ignore') as f:
	f.write(my_doc.render())