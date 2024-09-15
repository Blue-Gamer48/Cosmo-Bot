import aiohttp
def random_cat():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://cataas.com/cat') as response:
            if response.status == 200:
                cat_pic = str(response.url)
            else:
                cat_pic = str("Konnte Bild nicht Holen")

