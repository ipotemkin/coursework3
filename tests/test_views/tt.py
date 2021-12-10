from fixtures import data
import os


print(data['directors'][1])


os.environ['TESTING'] = 'TRUE'

TESTING = os.environ.get("TESTING")
print(TESTING)
