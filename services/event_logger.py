from services import db_service


def save_event(pEvent):
    '''
    Saves event to DynamoDB
    :param obj pEvent: event instance to save
    '''
    client = db_service.DbService()
    client.put_item("Klambda_events", vars(pEvent))
