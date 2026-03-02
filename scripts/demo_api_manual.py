from src.api_manual import handle_request

cases = [
    '{"iso3":" col ","year":1999}',
    '{"iso3":"CO","year":1999}',
    '{"iso3":"COL","year":"nope"}',
    '{"iso3":"COL","year":1999,"x":1}',
    "{bad json}",
]

for c in cases:
    print("IN:", c)
    print("OUT:", handle_request(c))
    print("-" * 60)