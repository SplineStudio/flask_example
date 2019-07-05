# from project.database import db
# from project.aygio.models.calendar import Calendar
# PROPERTY_ID = 27
#
#
# def update_renter(old_renter, fresh_renter):
#     resp = {}
#
#     for key, value in old_renter.__dict__.items():
#
#         if key in ['_sa_instance_state', 'id']:
#             continue
#         new_value = getattr(fresh_renter, key)
#         if value != new_value:
#             resp[key] = new_value
#     return resp
#
#
# def parse_calendar(avail_list, system_id):
#     first_day = None
#     last_day = None
#     counter = 0
#
#
#     for item in avail_list:
#
#         if first_day is None:
#             first_day = item
#             last_day = item
#
#         elif item['availability'] == first_day['availability'] and item['price'] == first_day['price']:
#             last_day = item
#
#         elif item['availability'] != first_day['availability'] or item['price'] != first_day['price']:
#             calendar_data = Calendar(
#                 property_id=PROPERTY_ID,
#                 system_id=system_id,
#                 availability=last_day['availability'],
#                 currency=last_day['currency'],
#                 price=last_day['price'],
#                 start_date=first_day['date'],
#                 end_date=last_day['date']
#             )
#             db.session.add(calendar_data)
#             db.session.commit()
#             counter += 1
#
#             first_day = item
#             last_day = item
#
#     if counter == 0 and first_day is not None:
#         calendar_data = Calendar(
#             property_id=PROPERTY_ID,
#             system_id=system_id,
#             availability=last_day['availability'],
#             currency=last_day['currency'],
#             price=last_day['price'],
#             start_date=first_day['date'],
#             end_date=last_day['date']
#         )
#         db.session.add(calendar_data)
#         db.session.commit()
