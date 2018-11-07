import pymongo

from model import user

PRIMARY_KEY = 'email'

class DAOUser:

    def __init__(self, MONGODB_URI, COLLECTION_NAME):
        self.mongo_client = pymongo.MongoClient(MONGODB_URI)
        self.apolo_ddbb = self.mongo_client.get_default_database() # as im using a sadxbox mlab account
        self.collection = self.apolo_ddbb[COLLECTION_NAME]

        self.set_up_ddbb()

    def insert(self, user):
        try:
            result = self.collection.insert(user.toDict())
        except pymongo.errors.DuplicateKeyError:
            return 'EMAIL_ALREADY_EXISTS'
        except:
            return 'ERROR'
        return 'SUCCESS'

    def update(self, user):
        criteria = {'email' : user.email}
        changes = {'$set': {'instrument' : user.instrument}}

        try:
            result = self.collection.update(criteria, changes)
            if result['updatedExisting']:
                return 'SUCCESS'
            else:
                return 'EMAIL_NOT_EXISTING'
        except:
            return 'ERROR'

    def readAll(self):
        cursor = self.collection.find()

        users = {}
        for doc in cursor:
            try:
                users[ doc['email'] ] = doc['instrument']
            except KeyError:
                pass

        return users

    def delete(self, user):
        criteria = {'email' : user.email}

        try:
            result = self.collection.delete_one(criteria)
        except:
            return 'ERROR'

        return 'SUCCESS'


    def set_up_ddbb(self):
        # setting up a primary key, or index in mongodb
        self.collection.create_index([(PRIMARY_KEY, pymongo.ASCENDING)], unique=True)