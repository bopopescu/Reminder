from .dbORMS.dbConn import Session, engine, Base
from .dbORMS.tasks import Tasks, TasksSchema
from sqlalchemy import and_, update
from flask import Flask, jsonify, request
from .dbORMS.eventNotification import EventNotificationSchema, EventNotification
from .main import get_object, app, HEADER_AUTH, JWT_SECRET, JWT_ALGORITHM, get_user_idJWT


@app.route('/event/<int:id_calendar>', methods=['GET'])
def get_event(id_calendar):
    id_user = get_user_idJWT()

    if id_user:
        sess = Session()
        events = sess.query(Tasks).filter(
            Tasks.id_calendar == id_calendar).all()
        events = TasksSchema(many=True).dump(events)
        sess.close()
        return jsonify(events), 201
    return ''


@app.route('/event', methods=['PUT'])
def update_event():
    id_user = get_user_idJWT()
    if id_user:
        posted_Event = TasksSchema(
            only=('title', 'date', 'time', 'color', 'id_calendar','id'),unknown="EXCLUDE").load(request.get_json())
        print (posted_Event)

        event = Tasks(**posted_Event)
        if event.time == 0:
            event.time = None
        sess = Session()
        event_from_db = sess.query(Tasks).filter(Tasks.id == event.id).first()
        event_from_db.time=event.time
        event_from_db.date=event.date
        sess.commit()
        sess.close()

        return '', 201
    return ''

@app.route('/event', methods=['POST'])
def add_event():
    id_user = get_user_idJWT()
    if id_user:
        posted_Event = TasksSchema(
            only=('title', 'date', 'time', 'color', 'id_calendar')).load(request.get_json())
        event = Tasks(**posted_Event)
        if event.time == 0:
            event.time = None
        sess = Session()
        sess.add(event)
        new_event = TasksSchema().dump(event)
        sess.commit()
        sess.close()

        return jsonify(new_event), 201
    return ''

@app.route('/event/<int:id>', methods=['DELETE'])
def delete_event(id):
    id_user = get_user_idJWT()
    if id_user:
        sess = Session()
        sess.query(Tasks).filter(
            and_(Tasks.id == id, Tasks.id_user == id_user)).delete()
        sess.commit()
        sess.close()
        return '', 201
    return ''

@app.route('/event/notyfication/<int:id_event>/<int:time>', methods=['DELETE'])
def remove_eventnotyfication(id_event,time):
    id_user = get_user_idJWT()
    if id_user:
        sess = Session()
        sess.query(EventNotification).filter(and_(EventNotification.id_event == id_event,EventNotification.time_before_in_milisec == time)).delete()    
        sess.commit()
        sess.close()
        return '', 201
    return ''


@app.route('/event/notyfication/<int:id_event>', methods=['POST'])
def add_eventnotyfication(id_event):
    id_user = get_user_idJWT()
    if id_user:

        posted_Event_notyfication = EventNotificationSchema(only=('id_event', 'time_before_in_milisec')).load(request.get_json())
        event_notyfication = EventNotification(**posted_Event_notyfication)
        sess = Session()
        sess.add(event_notyfication)
        sess.commit()
        sess.close()

        return '', 201
    return ''


@app.route('/event/notyfication',methods=["PUT"])
def update_eventnotyfication():
    id_user = get_user_idJWT()
    if id_user:
        posted_Event_notyfication = EventNotificationSchema().load(request.get_json())
        print(posted_Event_notyfication)
        event_n = EventNotification(**posted_Event_notyfication)
        sess = Session()
        if event_n.id !=None:
            
            event_nDB = sess.query(EventNotification).filter(EventNotification.id == event_n.id).first()
            print(event_nDB)
            if event_nDB !=None:
                event_nDB.time_before_in_milisec = event_n.time_before_in_milisec
                sess.commit()
                sess.close()    
                return '',201
    return '',200    
     


@app.route('/event/notyfication/<int:id_event>', methods=['GET'])
def get_eventnotyfication(id_event):
    id_user = get_user_idJWT()
    if id_user:
        sess = Session()
        events_notyfication_query = sess.query(EventNotification).filter(EventNotification.id_event == id_event).all()    
        events_notyfication = EventNotificationSchema(many=True).dump(events_notyfication_query)
        sess.close()
        return jsonify(events_notyfication), 201
    return ''

