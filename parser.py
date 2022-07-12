import ujson
import os

def load_data(data_folder: str):
  data = ujson.load(open(os.path.join(data_folder, 'FoodData_Central_foundation_food_json_2022-04-28.json')))['FoundationFoods']
  for food in data:
    base = {
      'subject': {
        'description': food['description'],
        'ndbNumber': food['ndbNumber'],
        'fdcId': food['fdcId'],
        'foodCategory': food['foodCategory']['description']
      }
    }
    for n in food['foodNutrients']:
      doc = base.copy()
      doc['object'] = {
        'nutrientName': n['nutrient']['name'],
        'nutrientId': n['nutrient']['id'],
        'nutrientRank': n['nutrient']['rank']
      }
      doc['relation'] = {}

      if 'amount' in n:
        doc['object']['nutrientAmount'] = n['amount']
        doc['object']['nutrientAmountUnits'] = n['nutrient']['unitName']

      if 'code' in n['foodNutrientDerivation']:
        doc['relation']['code'] = n['foodNutrientDerivation']['code']
      if 'code' in n['foodNutrientDerivation']['foodNutrientSource']:
        doc['relation']['sourceCode'] = n['foodNutrientDerivation']['foodNutrientSource']['code']
      if 'description' in n['foodNutrientDerivation']:
        doc['relation']['description'] = n['foodNutrientDerivation']['description']
      if 'description' in n['foodNutrientDerivation']['foodNutrientSource']:
        doc['relation']['sourceDescription'] = n['foodNutrientDerivation']['foodNutrientSource']['description']

      if 'min' in n:
        doc['relation']['nutrientMinAmount'] = n['min']
      if 'max' in n:
        doc['relation']['nutrientMinAmount'] = n['max']
      if 'median' in n:
        doc['relation']['nutrientMinAmount'] = n['median']
      
      doc['_id'] = f"{doc['subject']['fdcId']}-{doc['object']['nutrientId']}"
      yield doc

def main():
  obj = {}
  for docs in load_data('./'):
    if docs['_id'] in obj:
      print(docs['_id'])
    obj[docs['_id']] = docs
  
  print('done')
  ujson.dump(obj, open('./output.json', 'w'), indent=2)

if __name__ == '__main__':
  main()