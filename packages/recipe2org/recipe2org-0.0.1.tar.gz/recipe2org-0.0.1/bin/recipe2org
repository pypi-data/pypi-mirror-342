#!/usr/bin/env python3

from urllib.request import urlopen
from recipe_scrapers import scrape_html
import requests
import argparse
import textwrap
from datetime import datetime

def main():
   parser = argparse.ArgumentParser(
       prog='recipe-to-org', 
       formatter_class=argparse.RawDescriptionHelpFormatter,
       description=textwrap.dedent('''\
       recipe-to-org: Scrape a recipe and convert to org format
    '''))

   parser.add_argument('url', metavar='url', nargs='?', help='Recipe URL to scrape')
   parser.add_argument('-d', '--image-dir', type=str, nargs='?', default="./", help='Directory to save images')

   args = parser.parse_args()
   if not args.url:
       return print('Error: You must provide a url. See --help for usage.')
   org = recipe_to_org(args.url, args.image_dir)
   print(org)


def recipe_to_org(url: str, image_dir: str) -> str:
    html   = urlopen(url).read().decode("utf-8")  # retrieves the recipe webpage HTML
    scraper = scrape_html(html, org_url=url)

    # Extract recipe information
    title = scraper.title()
    scraped_instructions = scraper.instructions().split("\n")
    ordered_instructions_array = []

    for i in range(len(scraped_instructions)):
        instruction = scraped_instructions[i]
        ordered_instructions_array.append('{0}. {1}'.format(i + 1, instruction))

    ordered_instructions = "\n".join(ordered_instructions_array)

    try:
        cuisine = scraper.cuisine()
    except:
        cuisine = ""

    scraped_ingredients = scraper.ingredients()

    ingredients_array = []

    for ingredient in scraped_ingredients:
        ingredients_array.append('+ {0}'.format(ingredient))

    ingredients = "\n".join(ingredients_array)

    prep_time = scraper.prep_time()
    cook_time = scraper.cook_time()
    total_time = scraper.total_time()

    image_path=""

    try:
        image_url = scraper.image()
        response = requests.get(image_url)
        file_ext = image_url.split(".")[-1]
        filename = title.replace(" ", "-").lower() + "." + file_ext
        file_path = image_dir + filename
        with open(file_path, 'wb') as file:
            file.write(response.content)
        image_path = file_path
    except Exception as error:
        print("failed to download image")
        print(error)


    yields = scraper.yields()

    now = datetime.now()
    created = f"[{now.strftime('%Y-%m-%d %H:%M')}]"

    org = '''
* {title}
:PROPERTIES:
:Link: {url}
:Prep Time: {prep_time} min
:Cook Time: {cook_time} min
:Total Time: {total_time} min
:Yields: {yields}
:Created: {created}
:END:

[[file:{image_path}]]

** Ingredients
{ingredients}

** Instructions
{ordered_instructions}
    '''.format(
        title=title,
        url=url,
        created=created,
        prep_time=prep_time,
        cook_time=cook_time,
        total_time=total_time,
        image_path=image_path,
        yields=yields,
        ingredients=ingredients,
        ordered_instructions=ordered_instructions)

    return org

if __name__ == "__main__":
    main()

