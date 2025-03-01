from google.cloud import bigquery
import requests
import json
import io


def format_schema(schema):
    formatted_schema = []
    for row in schema:
        formatted_schema.append(bigquery.SchemaField(row['name'], row['type'], row['mode']))
    return formatted_schema


doric = "https://api.scryfall.com/cards/search?q=set%3ASLD+unique%3Acards+f%3Acommander+-is%3Areprint+id%3Dg+is%3Apermanent+%28o%3A%2F%28When%7CWhenever%29+%28%5Cw%7C%5B%5Ea-zA-Z%5Cd%5D%29%2B+enters%3F+the+battlefield%2F+OR+%28keyword%3AFabricate+OR+keyword%3A%22exploit%22+OR+keyword%3A%22living+weapon%22+OR+keyword%3Achampion+OR+keyword%3Aformirrodin+OR+keyword%3A%22partner+with%22+OR+keyword%3Aevolve+OR+keyword%3Agraft+OR+keyword%3Asoulbond+OR+keyword%3Ahideaway+OR+keyword%3Aformirrodin!+OR+keyword%3Asquad+OR+o%3Abackup%29%29&unique=cards&as=grid&order=name&format=json&page="
mat = "https://api.scryfall.com/cards/search?q=set%3AMAT+unique%3Acards+f%3Acommander+id%3C%3Dbug+is%3Apermanent+%28o%3A%2F%28When%7CWhenever%29+%28%5Cw%7C%5B%5Ea-zA-Z%5Cd%5D%29%2B+enters%3F+the+battlefield%2F+OR+%28keyword%3AFabricate+OR+keyword%3A%22exploit%22+OR+keyword%3A%22living+weapon%22+OR+keyword%3Achampion+OR+keyword%3Aformirrodin+OR+keyword%3A%22partner+with%22+OR+keyword%3Aevolve+OR+keyword%3Agraft+OR+keyword%3Asoulbond+OR+keyword%3Ahideaway+OR+keyword%3Aformirrodin!+OR+keyword%3Asquad+OR+o%3Abackup%29%29&unique=cards&as=grid&order=name&format=json&page="
lotr = "https://api.scryfall.com/cards/search?q=%28set%3Altr+OR+set%3Altc%29+-is%3Areprint+unique%3Acards+f%3Acommander+id%3C%3Dbug+is%3Apermanent+%28o%3A%2F%28When%7CWhenever%29+%28%5Cw%7C%5B%5Ea-zA-Z%5Cd%5D%29%2B+enters%3F+the+battlefield%2F+OR+%28keyword%3AFabricate+OR+keyword%3A%22living+weapon%22+OR+keyword%3Achampion+OR+keyword%3A%22partner+with%22+OR+keyword%3Aevolve+OR+keyword%3Agraft+OR+keyword%3Asoulbond+OR+keyword%3Ahideaway+OR+keyword%3Asquad+OR+keyword%3Aexploit+OR+keyword%3Aformirrodin%29%29&unique=cards&as=grid&order=name&format=json&page="

# adding REX, LCI, LCC, LTC, WHO, WOC, WOE, and CMM
# also note that Ravnica Remastered has no new cards
url = "https://api.scryfall.com/cards/search?q=%28set%3Arex+or+set%3Alci+or+set%3Alcc+or+set%3Altc+or+set%3Awho+or+set%3Awoc+or+set%3Awoe+or+set%3Acmm+%29+-is%3Areprint+-is%3Adigital+unique%3Acards+f%3Acommander+id%3C%3Dbug+is%3Apermanent+%28o%3A%2F%28When%7CWhenever%29+%28%5Cw%7C%5B%5Ea-zA-Z%5Cd%5D%29%2B+enters%3F+the+battlefield%2F+OR+%28keyword%3AFabricate+OR+keyword%3A%22exploit%22+OR+keyword%3A%22living+weapon%22+OR+keyword%3Achampion+OR+keyword%3Aformirrodin+OR+keyword%3A%22partner+with%22+OR+keyword%3Aevolve+OR+keyword%3Agraft+OR+keyword%3Asoulbond+OR+keyword%3Ahideaway+OR+keyword%3Aformirrodin!+OR+keyword%3Asquad+OR+o%3Abackup%29%29&unique=cards&as=grid&order=name&format=json&page="


# from now on we always need special guests too SPG (but it is always reprints anyway, so we technically can ignore)
# also, etb changed to just enters, so let's change that as well

# mkm, clu, mkc, pip, otp, otj, otc, big
url = "https://api.scryfall.com/cards/search?q=%28set%3Amkm+or+set%3Aclu+or+set%3Amkc+or+set%3Apip+or+set%3Aotp+or+set%3Aotj+or+set%3Aotc+or+set%3Abig+%29+-is%3Areprint+-is%3Adigital+unique%3Acards+f%3Acommander+id%3C%3Dbug+is%3Apermanent+%28o%3A%2F%28When%7CWhenever%29+%28%5Cw%7C%5B%5Ea-zA-Z%5Cd%5D%29%2B+enters%3F%2F+OR+%28keyword%3AFabricate+OR+keyword%3A%22exploit%22+OR+keyword%3A%22living+weapon%22+OR+keyword%3Achampion+OR+keyword%3Aformirrodin+OR+keyword%3A%22partner+with%22+OR+keyword%3Aevolve+OR+keyword%3Agraft+OR+keyword%3Asoulbond+OR+keyword%3Ahideaway+OR+keyword%3Aformirrodin!+OR+keyword%3Asquad+OR+o%3Abackup%29%29&unique=cards&as=grid&order=name&format=json&page="


# m3c, mh3, acr, blc, mb2, blb, dsk, dsc,
url = "https://api.scryfall.com/cards/search?q=%28set%3Am3c+or+set%3Amh3+or+set%3Aacr+or+set%3Ablc+or+set%3Amb2+or+set%3Ablb+or+set%3Adsk+or+set%3Adsc+%29+-is%3Areprint+-is%3Adigital+unique%3Acards+f%3Acommander+id%3C%3Dbug+is%3Apermanent+%28o%3A%2F%28When%7CWhenever%29+%28%5Cw%7C%5B%5Ea-zA-Z%5Cd%5D%29%2B+enters%3F%2F+OR+%28keyword%3AFabricate+OR+keyword%3A%22exploit%22+OR+keyword%3A%22living+weapon%22+OR+keyword%3Achampion+OR+keyword%3Aformirrodin+OR+keyword%3A%22partner+with%22+OR+keyword%3Aevolve+OR+keyword%3Agraft+OR+keyword%3Asoulbond+OR+keyword%3Ahideaway+OR+keyword%3Aformirrodin!+OR+keyword%3Asquad+OR+o%3Abackup%29%29&unique=cards&as=grid&order=name&format=json&page="

# j25, fdn, fdc, inr, drc, dft, spg, pltc
url = "https://api.scryfall.com/cards/search?q=%28set%3Aj25+or+set%3Afdn+or+set%3Afdc+or+set%3Ainr+or+set%3Adrc+or+set%3Aspg+or+set%3Apltc+or+set%3Adft+%29+-is%3Areprint+-is%3Adigital+unique%3Acards+f%3Acommander+id%3C%3Dbug+is%3Apermanent+%28o%3A%2F%28When%7CWhenever%29+%28%5Cw%7C%5B%5Ea-zA-Z%5Cd%5D%29%2B+enters%3F%2F+OR+%28keyword%3AFabricate+OR+keyword%3A%22exploit%22+OR+keyword%3A%22living+weapon%22+OR+keyword%3Achampion+OR+keyword%3Aformirrodin+OR+keyword%3A%22partner+with%22+OR+keyword%3Aevolve+OR+keyword%3Agraft+OR+keyword%3Asoulbond+OR+keyword%3Ahideaway+OR+keyword%3Aformirrodin!+OR+keyword%3Asquad+OR+o%3Abackup%29%29&unique=cards&as=grid&order=name&format=json&page="

# force add these
# "Cao Ren, Wei Commander",
# "Círdan the Shipwright",
# "Loamcrafter Faun",
# "Mu Yanling, Wind Rider",
# "Paleontologist's Pick-Axe // Dinosaur Headdress",
# "Twists and Turns // Mycoid Maze",
# "Vampiric Spirit",
# "Xolatoyac, the Smiling Flood"
url = 'https://api.scryfall.com/cards/search?q=%22Cao+Ren%2C+Wei+Commander%22+or+%22C%C3%ADrdan+the+Shipwright%22+or+%22Loamcrafter+Faun%22+or+%22Mu+Yanling%2C+Wind+Rider%22+or+%22Paleontologist%27s+Pick-Axe+%2F%2F+Dinosaur+Headdress%22+or+%22Twists+and+Turns+%2F%2F+Mycoid+Maze%22+or+%22Vampiric+Spirit%22+or+%22Xolatoyac%2C+the+Smiling+Flood%22&unique=cards&as=grid&order=name'

r = requests.get(url)

js = r.json()
# print(r.json())
cards = []
page = 1
cards = cards + js['data']
for thing in cards:
    print(thing["name"])
    delete_these = ['object', 'id', 'oracle_id', 'multiverse_ids', 'mtgo_id', 'arena_id', 'tcgplayer_id',
                    'cardmarket_id',
                    'lang', 'released_at', 'layout', 'image_status', 'games', 'foil', 'nonfoil', 'finishes',
                    'oversized',
                    'promo', 'reprint', 'variation', 'set_id', 'set_type', 'set_uri',
                    'set_search_uri', 'scryfall_set_uri', 'rulings_uri', 'prints_search_uri', 'collector_number',
                    'digital', 'rarity', 'card_back_id', 'artist', 'artist_ids', 'illustration_id', 'border_color',
                    'frame', 'full_art', 'textless', 'booster', 'story_spotlight', 'edhrec_rank', 'penny_rank',
                    'related_uris', 'purchase_uris', 'legalities', 'color_indicator', 'tcgplayer_etched', 'promo_types',
                    'security_stamp', 'produced_mana', 'previewed_at', 'preview', 'loyalty', 'watermark',
                    'highres_image',
                    'card_faces', 'mtgo_foil_id', 'frame_effects', 'tcgplayer_etched_id', 'all_parts']
    for field in delete_these:
        try:
            del thing[field]
        except KeyError:
            # print(f"Key not found: {field} for the card {thing['name']} ")
            pass
    thing['set_code'] = thing['set']
    del thing['set']

    print("toughness" in thing)
    if "toughness" in thing:
        print(f"the toughness is {thing['toughness']}")
        print(type(thing['toughness']))
        if isinstance(thing['toughness'], int):
            thing['toughness'] = str(thing['toughness'])

    # None=None
    thing["in_collection"] = False

json_cards = cards

# move the cards to a json file
with open("json_cards.json", "w") as outfile:
    # changing to 'a' so we only append at the end of the file
    # with open("cards.json", "a") as outfile:
    for card in cards:
        json.dump(card, outfile)
        outfile.write('\n')

with open("json_cards.json") as f:
    for line in f:
        json_object = json.loads(line)
# json_object = json.loads("json_cards.json")

project_id = 'card-database-381500'
dataset_id = 'etb'
table_id = 'cards'

client = bigquery.Client(project=project_id)
dataset = client.dataset(dataset_id)
table = dataset.table(table_id)
table_client = client.get_table(table)

f = io.StringIO("")
client.schema_to_json(table_client.schema, f)
table_schema = json.loads(f.getvalue())
# print(f.getvalue())


job_config = bigquery.LoadJobConfig()
job_config.write_disposition = 'WRITE_APPEND'
job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
# job_config.autodetect = True
# adding custom schema
# job_config.schema = format_schema(table_schema)
# TRY without the format schema function because it isn't handling records properly
job_config.schema = table_schema
job_config.ignore_unknown_values = True

# job = client.load_table_from_json(
#         json_object,
#         table,
#         location='US',
#         job_config=job_config
#     )

with open("json_cards.json", "rb") as source_file:
    job = client.load_table_from_file(
        source_file,
        table,
        location='US',
        job_config=job_config,
    )

print(job.result())
print(f"Loaded {job.output_rows} rows into {dataset_id}:{table_id}")