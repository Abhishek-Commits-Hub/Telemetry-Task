import json, unittest, datetime

# Load JSON files with correct encoding
with open("./data-1.json", "r", encoding="utf-8") as f:
    jsonData1 = json.load(f)

with open("./data-2.json", "r", encoding="utf-8") as f:
    jsonData2 = json.load(f)

with open("./data-result.json", "r", encoding="utf-8") as f:
    jsonExpectedResult = json.load(f)


# ---------------- FORMAT 1 ----------------
def convertFromFormat1(jsonObject):

    locationParts = jsonObject["location"].split("/")

    result = {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': locationParts[0],
            'city': locationParts[1],
            'area': locationParts[2],
            'factory': locationParts[3],
            'section': locationParts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }

    return result


# ---------------- FORMAT 2 ----------------
def convertFromFormat2(jsonObject):

    dt = datetime.datetime.strptime(
        jsonObject['timestamp'],
        '%Y-%m-%dT%H:%M:%S.%fZ'
    )

    # FIX: force UTC to avoid timestamp shift issues
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    timestamp = int(dt.timestamp() * 1000)

    result = {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': {
            'status': jsonObject['data']['status'],
            'temperature': jsonObject['data']['temperature']
        }
    }

    return result


# ---------------- ROUTER ----------------
def main(jsonObject):

    if jsonObject.get('device') is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


# ---------------- TEST CASES ----------------
class TestSolution(unittest.TestCase):

    def test_dataType1(self):
        self.assertEqual(main(jsonData1), jsonExpectedResult)

    def test_dataType2(self):
        self.assertEqual(main(jsonData2), jsonExpectedResult)


if __name__ == '__main__':
    unittest.main()