import json
import requests

from project.aygio.models.calendar import Calendar, GuestInfo, Rental
from project.aygio.models.photo import Photo
from project.aygio.models.property import Property

from project.database import db
from datetime import datetime

from project.errors.custom_exceptions import ImpossibleSystemCommand, OldData, OutSystemConnect



class Manager9Flats():

    SYSTEM_ID = 1
    CLIENT_ID = 'NozfgeXqqJjvbAPCiURUrgaCMLDus7C9HYo2zMtP'

    USER_INFO_URL = "https://www.9flats.com/api/v4/users/me?client_id={}&oauth_token={}"
    ALL_PLACE_URL = "https://www.9flats.com/api/v4/places/my?client_id={}&oauth_token={}"
    UPDATE_PLACE_URL = 'https://www.9flats.com/api/v4/places/{}?client_id={}&oauth_token={}'

    NINE_FLAT_URL = 'https://www.9flats.com'
    CALENDAR_URL = "{}/api/v4/places/{}/host_calendars?client_id={}&oauth_token={}&start_date={}&end_date={}"
    ACCOMODATIONS_URL = "{}/api/v4/users/{}/accommodations?client_id={}&oauth_token={}"
    ADD_RENTAL_URL_9FLATS = '{}/api/v4/places/{}/host_calendars?client_id={}&oauth_token={}&start_date={}&end_date={}&available=false'

    def load_slug(self, oauth_token):
        answer = requests.get(self.USER_INFO_URL.format(self.CLIENT_ID, oauth_token))

        if not answer.ok:
            raise OutSystemConnect

        response_native = json.loads(answer.text)
        return response_native['slug']

    def validate_photo(self, arr_json_photo):
        return None if len(arr_json_photo) == 0 else arr_json_photo[0]['place_photo']['url']

    def all_props(self, user_id, oauth_token):
        answer = requests.get(self.ALL_PLACE_URL.format(self.CLIENT_ID, oauth_token))

        if not answer.ok:
            raise OutSystemConnect

        response_native = json.loads(answer.text)
        place_list = response_native['places']
        property_list = []

        for place in place_list:
            place_details = place['place']['place_details']
            pricing = place['place']['pricing']

            prop = Property(
                system_id=self.SYSTEM_ID,
                inner_id=place_details['id'],
                name=place_details['name'],

                country=place_details['country'],
                city=place_details['city'],
                district=place_details['district'],
                zip_code=place_details['zipcode'],

                price=pricing['price'],
                currency=pricing['currency'],

                min_stay=place_details['minimum_nights'],
                size=place_details['size'],
                photo_url=self.validate_photo(place_details['additional_photos']),
                local_user_id=user_id,
                number_of_guests=place_details['number_of_beds']

            )

            property_list.append(prop)

        return property_list

    def all_photos(self, oauth_token):

        answer = requests.get(self.ALL_PLACE_URL.format(self.CLIENT_ID, oauth_token))

        if not answer.ok:
            raise OutSystemConnect

        response_native = json.loads(answer.text)
        place_list = response_native['places']
        photo_list = []

        for place in place_list:
            place_details = place['place']['place_details']
            inner_id = place_details['id']

            props = Property.query.filter_by(inner_id=inner_id, system_id=self.SYSTEM_ID).all()
            if len(props) != 1:
                raise OldData

            prop = props[0]
            photolist = place_details['additional_photos']
            if len(photolist) == 0:
                continue

            for photo_json in photolist:
                photo = Photo(
                    file_name=photo_json['place_photo']['url'],
                    property_id=prop.id,
                    user_id=prop.local_user_id
                )

                photo_list.append(photo)

        return photo_list

    def update_prop(self, prop_inner_id, token, key, value):

        if key == 'min_stay':
            key_for_9flats = 'minimum_nights'
        elif key == 'number_of_guests':
            key_for_9flats = 'number_of_beds'
        else:
            raise ImpossibleSystemCommand


        answer = requests.put(
            self.UPDATE_PLACE_URL.format(prop_inner_id, self.CLIENT_ID, token),
            json={"place": {key_for_9flats: value}}
            )

        if not answer.ok:
            raise OutSystemConnect

    def load_calendar(self, token, flat_id, prop_id, place_id, start_date, end_date):
        req_string = self.CALENDAR_URL.format(self.NINE_FLAT_URL,
                                              place_id,
                                              self.CLIENT_ID,
                                              token,
                                              start_date,
                                              end_date)
        answer = requests.get(req_string)

        if not answer.ok:
            return OutSystemConnect
        response_native = json.loads(answer.text)

        first_day = None
        last_day = None
        calendar_list = []
        rental = None

        for item in response_native["availabilities"]:

            if rental:
                if rental.to_date == item['date']:
                    calendar_data = Calendar(
                        property_id=prop_id,
                        system_id=self.SYSTEM_ID,
                        availability='unavailable',
                        start_date=rental.from_date,
                        end_date=rental.to_date
                    )
                    calendar_list.append(calendar_data)
                    rental = None

                continue

            rental = Rental.query.filter_by(flat_id=flat_id,
                                            from_date=item['date']).first()

            if first_day is None:
                first_day = item
                last_day = item

            elif item['availability'] == first_day['availability'] and item['price'] == first_day['price']:
                last_day = item

            elif item['availability'] != first_day['availability'] or item['price'] != first_day['price']:
                calendar_data = Calendar(
                    property_id=prop_id,
                    system_id=self.SYSTEM_ID,
                    availability=last_day['availability'],
                    currency=last_day['currency'],
                    price=last_day['price'],
                    start_date=first_day['date'],
                    end_date=last_day['date']
                )
                calendar_list.append(calendar_data)

                first_day = item
                last_day = item

        if len(calendar_list) == 0 and first_day is not None:
            calendar_data = Calendar(
                property_id=prop_id,
                system_id=self.SYSTEM_ID,
                availability=last_day['availability'],
                currency=last_day['currency'],
                price=last_day['price'],
                start_date=first_day['date'],
                end_date=last_day['date']
                )
            calendar_list.append(calendar_data)

        return calendar_list

    def load_accommodation(self, slug, token):
        req_string = self.ACCOMODATIONS_URL.format(self.NINE_FLAT_URL, slug, self.CLIENT_ID, token)
        answer = requests.get(req_string)

        if not answer.ok:
            raise OutSystemConnect

        response_native = json.loads(answer.text)
        list_of_bookings = []

        for item in response_native["bookings"]:
            booking = item['booking']
            checkin_date = datetime.strptime(booking['checkin_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            checkout_date = datetime.strptime(booking['checkout_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            cal = Calendar.query.filter_by(start_date=checkin_date, end_date=checkout_date).first()
            if cal and cal.availability == 'unavailable':
                guest_json = booking['guest']
                if 'phone_number' not in guest_json:
                    guest_json['phone_number'] = None

                guest_info = GuestInfo(
                    calendar_id=cal.id,
                    system_id=self.SYSTEM_ID,
                    user_name=guest_json['name'],
                    phone_number=guest_json['phone_number'],
                    guests=booking['number_of_guests'],
                    nights=booking['nights'],
                    total_cost=booking['total']['value'],
                    currency=booking['total']['currency'],
                    from_time=None,
                    to_time=None
                )
                list_of_bookings.append(guest_info)
        return list_of_bookings

    def set_unavailable(self, place_id, token, start_date, end_date):
        req_string = self.ADD_RENTAL_URL_9FLATS.format(self.NINE_FLAT_URL,
                                                       place_id,
                                                       self.CLIENT_ID,
                                                       token,
                                                       start_date,
                                                       end_date, 'false')
        answer = requests.post(req_string)

        if not answer.ok:
            raise OutSystemConnect

