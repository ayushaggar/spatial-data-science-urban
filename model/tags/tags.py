# Classify uses according to OpenStreetMap wiki
"""
Possible tags classification:
	non_commercial: Defines a residential land use and other non-activity use
	commercial can be = shop, commercial/industrial
	we can change according to interest
"""

# Key:Value classification
key_classification = {}
# Specific activity category classification
activity_classification = {"commercial": [], "non_commercial": []}

# Amenities according to openstreetmap wiki
amenities_sustenance = [
    'bar',
    'pub',
    'restaurant',
    'biergarten',
    'cafe',
    'fast_food',
    'food_court',
    'ice_cream']
amenities_education = [
    'college',
    'kindergarten',
    'library',
    'public_bookcase',
    'school',
    'music_school',
    'driving_school',
    'language_school',
    'university']
amenities_transportation = [
    'fuel',
    'bicycle_rental',
    'bus_station',
    'car_rental',
    'taxi',
    'car_wash',
    'ferry_terminal']
amenities_financial = ['atm', 'bank', 'bureau_de_change']
amenities_healthcare = [
    'baby_hatch',
    'clinic',
    'dentist',
    'doctors',
    'hospital',
    'nursing_home',
    'pharmacy',
    'social_facility',
    'veterinary']
amenities_entertainment = [
    'arts_centre',
    'brothel',
    'casino',
    'cinema',
    'community_centre',
    'fountain',
    'gambling',
    'nightclub',
    'planetarium',
    'social_centre',
    'stripclub',
    'studio',
    'swingerclub',
    'theatre']
amenities_others = [
    'animal_boarding',
    'animal_shelter',
    'courthouse',
    'coworking_space',
    'crematorium',
    'dive_centre',
    'dojo',
    'embassy',
    'fire_station',
    'gym',
    'internet_cafe',
    'marketplace',
    'police',
    'post_office',
    'townhall']
amenities_activities = amenities_sustenance + amenities_education + amenities_transportation + \
    amenities_financial + amenities_healthcare + amenities_entertainment + amenities_others
key_classification["activity_amenity"] = amenities_activities
activity_classification["non_commercial"] += amenities_education + amenities_transportation + \
    amenities_financial + amenities_healthcare + amenities_entertainment + amenities_others
activity_classification["commercial"] += amenities_sustenance

# Shop according to openstreetmap wiki
shop_other = [
    "bookmaker",
    "copyshop",
    "dry_cleaning",
    "e-cigarette",
    "funeral_directors",
    "laundry",
    "money_lender",
    "pawnbroker",
    "pet",
    "pyrotechnics",
    "religion",
    "tobacco",
    "toys",
    "travel_agency",
    "vacant",
    "weapons",
    "user defined"]
shop_gifts = [
    "anime",
    "books",
    "gift",
    "lottery",
    "newsagent",
    "stationery",
    "ticket"]
shop_art = [
    "art",
    "collector",
    "craft",
    "frame",
    "games",
    "model",
    "music",
    "musical_instrument",
    "photo",
    "camera",
    "trophy",
    "video",
    "video_games"]
shop_sports = [
    "bicycle",
    "car",
    "car_repair",
    "car_parts",
    "fuel",
    "fishing",
    "free_flying",
    "hunting",
    "motorcycle",
    "outdoor",
    "scuba_diving",
    "sports",
    "swimming_pool",
    "tyres"]
shop_electronics = [
    "computer",
    "electronics",
    "hifi",
    "mobile_phone",
    "radiotechnics",
    "vacuum_cleaner"]
shop_furniture = [
    "antiques",
    "bed",
    "candles",
    "carpet",
    "curtain",
    "furniture",
    "interior_decoration",
    "kitchen",
    "lamps",
    "tiles",
    "window_blind"]
shop_household = [
    "agrarian",
    "bathroom_furnishing",
    "doityourself",
    "electrical",
    "energy",
    "fireplace",
    "florist",
    "garden_centre",
    "garden_furniture",
    "gas",
    "glaziery",
    "hardware",
    "houseware",
    "locksmith",
    "paint",
    "security",
    "trade"]
shop_health = [
    "beauty",
    "chemist",
    "cosmetics",
    "drugstore",
    "erotic",
    "hairdresser",
    "hairdresser_supply",
    "hearing_aids",
    "herbalist",
    "massage",
    "medical_supply",
    "nutrition_supplements",
    "optician",
    "perfumery",
    "tattoo"]
shop_charity = ["charity", "second_hand", "variety_store"]
shop_clothing = [
    "baby_goods",
    "bag",
    "boutique",
    "clothes",
    "fabric",
    "fashion",
    "jewelry",
    "leather",
    "shoes",
    "tailor",
    "watches"]
shop_mall = ["department_store", "general", "kiosk", "mall", "supermarket"]
shop_food = [
    "alcohol",
    "bakery",
    "beverages",
    "brewing_supplies",
    "butcher",
    "cheese",
    "chocolate",
    "coffee",
    "confectionery",
    "convenience",
    "deli",
    "dairy",
    "farm",
    "greengrocer",
    "ice_cream",
    "organic",
    "pasta",
    "pastry",
    "seafood",
    "spices",
    "tea",
    "wine"]

shop_activities = shop_other + shop_gifts + shop_art + shop_sports + shop_electronics + shop_furniture + \
    shop_household + shop_health + shop_charity + shop_clothing + shop_mall + shop_food + ['shop']

key_classification["activity_shop"] = shop_activities
activity_classification["commercial"] += shop_activities

# Leisure according to openstreetmap wiki
leisure_activies = [
    'dog_park',
    'bird_hide',
    'bandstand',
    'firepit',
    'fishing',
    'garden',
    'golf_course',
    'marina',
    'nature_reserve',
    'park',
    'playground',
    'slipway',
    'track',
    'wildlife_hide',
    'adult_gaming_centre',
    'amusement_arcade',
    'beach_resort',
    'dance',
    'escape_game',
    'fitness_centre',
    'hackerspace',
    'horse_riding',
    'ice_rink',
    'miniature_golf',
    'pitch',
    'sauna',
    'sports_centre',
    'stadium',
    'summer_camp',
    'swimming_area',
    'swimming_pool',
    'water_park']

key_classification["activity_leisure"] = leisure_activies
activity_classification["non_commercial"] += leisure_activies

# Man made according to openstreetmap wiki
man_made_activities = [
    "offshore_platform",
    "works",
    "wastewater_plant",
    "water_works",
    "kiln",
    "monitoring_station",
    "observatory"]
man_made_other = [
    'adit',
    'beacon',
    'breakwater',
    'bridge',
    'bunker_silo',
    'campanile',
    'chimney',
    'communications_tower',
    'crane',
    'cross',
    'cutline',
    'clearcut',
    'embankment',
    'dovecote',
    'dyke',
    '	flagpole',
    'gasometer',
    'groyne',
    'lighthouse',
    'mast',
    'mineshaft',
    'obelisk',
    'petroleum_well',
    'pier',
    'pipeline',
    'pumping_station',
    'reservoir_covered',
    'silo',
    'snow_fence',
    'snow_net',
    'storage_tank',
    'street_cabinet',
    'surveillance',
    'survey_point',
    'telscope',
    'tower',
    'watermill',
    'water_tower',
    'water_well',
    'water_tap',
    'wildlife_crossing',
    'windmill']

key_classification["activity_man_made"] = man_made_activities
key_classification["other_man_made"] = man_made_other
activity_classification["non_commercial"] += man_made_activities

# Building according to openstreetmap wiki
building_infer = ['yes']
building_other = [
    'barn',
    'bridge',
    'bunker',
    'cabin',
    'cowshed',
    'digester',
    'garage',
    'garages',
    'farm_auxiliary',
    'greenhouse',
    'hut',
    'roof',
    'shed',
    'stable',
    'sty',
    'transformer_tower',
    'service',
    'ruins']
building_related_activities = [
    'hangar',
    'stable',
    'cowshed',
    'digester',
    'construction']
building_shop = ['shop', 'kiosk']
building_commercial = [
    'commercial',
    'office',
    'industrial',
    'retail',
    'warehouse'] + ['port']
building_civic_amenity = [
    'cathedral',
    'chapel',
    'church',
    'mosque',
    'temple',
    'synagogue',
    'shrine',
    'civic',
    'hospital',
    'school',
    'stadium',
    'train_station',
    'transportation',
    'university',
    'public']
building_activities = building_commercial + building_civic_amenity + \
    building_related_activities + building_shop
building_residential = [
    'hotel',
    'farm',
    'apartment',
    'apartments',
    'dormitory',
    'house',
    'residential',
    'retirement_home',
    'terrace',
    'houseboat',
    'bungalow',
    'static_caravan',
    'detached']
key_classification["activity_building"] = building_activities
key_classification["residential_building"] = building_residential
key_classification["infer_building"] = building_infer
key_classification["other_building"] = building_other
activity_classification["commercial"] += building_commercial
activity_classification["non_commercial"] += building_civic_amenity + \
    building_related_activities
activity_classification["commercial"] += building_shop
key_classification["activity_building:use"] = building_activities
key_classification["residential_building:use"] = building_residential
key_classification["activity_building:part"] = building_activities
key_classification["residential_building:part"] = building_residential
activity_classification["non_commercial"] += ['quarry',
                                              'salt_pond', 'military']
