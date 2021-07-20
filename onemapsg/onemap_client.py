from requests_toolbelt.multipart.encoder import MultipartEncoder
import time
import requests
import json

class OneMapClient():
    def __init__(self, email, password):
        self.email = email
        self.password = password

        self.url_base = "https://developers.onemap.sg"

        self.expiry = 0
        self.token = None

    def get_token(self, email=None, password=None):
        if email is None:
            email = self.email
        if password is None:
            password = self.password

        json_data = {"email":email, "password":password}
        response = requests.post(
            self.url_base + "/privateapi/auth/post/getToken",
            json=json_data,
            headers={"Content-Type":"application/json"}
        )

        response_data = json.loads(response.text)

        if response.ok:
            self.token = response_data['access_token']
            self.expiry = int(response_data['expiry_timestamp'])
        else:
            print("TOKEN REFRESH FAILED!")

        return self.token, self.expiry

    def check_expired_and_refresh_token(self):
        if time.time() - self.expiry > -10:
            token, expiry = self.get_token()
            print("REFRESHING TOKEN. NEW EXPIRY:", expiry)
            return True, token, expiry
        else:
            return False, self.token, self.expiry

    def query_api(self, endpoint, param_dict):
        '''General OneMap API query with token.'''
        self.check_expired_and_refresh_token()[0]

        try:
            if not endpoint.startswith("/"):
                endpoint = "/" + endpoint

            param_dict['token'] = self.token

            return json.loads(requests.get(self.url_base + endpoint,
                                           params=param_dict).text)
        except Exception as e:
            print(e)
            return

    def search(self, search_val, return_geom=True, get_addr_details=True, page_num=1):
        '''API Documentation: https://docs.onemap.sg/#search'''
        try:
            if return_geom:
                return_geom = "Y"
            else:
                return_geom = "N"

            if get_addr_details:
                get_addr_details = "Y"
            else:
                get_addr_details = "N"

            return json.loads(requests.get(self.url_base + "/commonapi/search",
                                           params={'searchVal': search_val,
                                                   'returnGeom': return_geom,
                                                   'getAddrDetails': get_addr_details,
                                                   'pageNum': page_num}).text)
        except Exception as e:
            print(e)
            return

    def reverse_geocode_SVY21(self, coordinates, buffer=10, address_type="All", other_features=False):
        '''API Documentation: https://docs.onemap.sg/#reverse-geocode-svy21'''
        self.check_expired_and_refresh_token()[0]

        try:
            if other_features:
                other_features = "Y"
            else:
                other_features = "N"

            if buffer > 500:
                buffer = 500
            if buffer < 0:
                buffer = 0

            location = "{},{}".format(coordinates[0], coordinates[1])

            return json.loads(requests.get(self.url_base + "/privateapi/commonsvc/revgeocodexy",
                                           params={'location': location,
                                                   'token': self.token,
                                                   'buffer': buffer,
                                                   'addressType': address_type,
                                                   'otherFeatures': other_features}).text)
        except Exception as e:
            print(e)
            return

    def reverse_geocode_WGS84(self, coordinates, buffer=10, address_type="All", other_features=False):
        '''API Documentation: https://docs.onemap.sg/#reverse-geocode-wgs84'''
        self.check_expired_and_refresh_token()[0]

        try:
            if other_features:
                other_features = "Y"
            else:
                other_features = "N"

            if buffer > 500:
                buffer = 500
            if buffer < 0:
                buffer = 0

            location = "{},{}".format(coordinates[0], coordinates[1])

            return json.loads(requests.get(self.url_base + "/privateapi/commonsvc/revgeocode",
                                           params={'location': location,
                                                   'token': self.token,
                                                   'buffer': buffer,
                                                   'addressType': address_type,
                                                   'otherFeatures': other_features}).text)
        except Exception as e:
            print(e)
            return

    def WGS84_to_EPSG(self, coordinates):
        try:
            return json.loads(requests.get(self.url_base + "/commonapi/convert/4326to3857",
                                           params={'latitude': coordinates[0],
                                                   'longitude': coordinates[1]}).text)
        except Exception as e:
            print(e)
            return

    def WGS84_to_SVY21(self, coordinates):
        try:
            return json.loads(requests.get(self.url_base + "/commonapi/convert/4326to3414",
                                           params={'latitude': coordinates[0],
                                                   'longitude': coordinates[1]}).text)
        except Exception as e:
            print(e)
            return

    def SVY21_to_EPSG(self, coordinates):
        try:
            return json.loads(requests.get(self.url_base + "/commonapi/convert/3414to3857",
                                           params={'X': coordinates[0],
                                                   'Y': coordinates[1]}).text)
        except Exception as e:
            print(e)
            return

    def SVY21_to_WGS84(self, coordinates):
        try:
            return json.loads(requests.get(self.url_base + "/commonapi/convert/3414to4326",
                                           params={'X': coordinates[0],
                                                   'Y': coordinates[1]}).text)
        except Exception as e:
            print(e)
            return

    def EPSG_to_SVY21(self, coordinates):
        try:
            return json.loads(requests.get(self.url_base + "/commonapi/convert/3857to3414",
                                           params={'X': coordinates[0],
                                                   'Y': coordinates[1]}).text)
        except Exception as e:
            print(e)
            return

    def EPSG_to_WGS84(self, coordinates):
        try:
            return json.loads(requests.get(self.url_base + "/commonapi/convert/3857to4326",
                                           params={'X': coordinates[0],
                                                   'Y': coordinates[1]}).text)
        except Exception as e:
            print(e)
            return

    def check_theme_status(self, query_name, date_time):
        '''API Documentation: https://docs.onemap.sg/#check-theme-status'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/themesvc/checkThemeStatus",
                                           params={'queryName': query_name,
                                                   'token': self.token,
                                                   'dateTime': date_time}).text)
        except Exception as e:
            print(e)
            return

    def get_theme_info(self, query_name):
        '''API Documentation: https://docs.onemap.sg/#get-theme-info'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/themesvc/getThemeInfo",
                                           params={'queryName': query_name,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_all_themes_info(self, more_info=False):
        '''API Documentation: https://docs.onemap.sg/#get-all-themes-info'''
        self.check_expired_and_refresh_token()[0]

        try:
            if more_info:
                more_info = "Y"
            else:
                more_info = "N"

            return json.loads(requests.get(self.url_base + "/privateapi/themesvc/getAllThemesInfo",
                                           params={'moreInfo': more_info,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def retrieve_theme(self, query_name, extents=None):
        '''API Documentation: https://docs.onemap.sg/#retrieve_theme'''
        self.check_expired_and_refresh_token()[0]

        try:
            if extents is not None:
                extents = "{},{},{},{}".format(extents[0], extents[1], extents[2], extents[3])

            return json.loads(requests.get(self.url_base + "/privateapi/themesvc/retrieveTheme",
                                           params={'queryName': query_name,
                                                   'extents': extents,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_all_planning_areas(self, year=None):
        '''API Documentation: https://docs.onemap.sg/#planning-area'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getAllPlanningarea",
                                           params={'year': year,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_planning_area_names(self, year=None):
        '''API Documentation: https://docs.onemap.sg/#names-of-planning-area'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getPlanningareaNames",
                                           params={'year': year,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_planning_area_bounds(self, coordinates, year=None):
        '''API Documentation: https://docs.onemap.sg/#planning-area-query'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getPlanningarea",
                                           params={'year': year,
                                                   'lat': coordinates[0],
                                                   'long': coordinates[1],
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_economic_statuses(self, year, planning_area, gender=None):
        '''API Documentation: https://docs.onemap.sg/#economic-status-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getEconomicStatus",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'gender': gender,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_education_attendance(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#education-status-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getEthnicGroup",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_ethnic_groups(self, year, planning_area, gender=None):
        '''API Documentation: https://docs.onemap.sg/#ethnic-distribution-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getEthnicGroup",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'gender': gender,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_household_monthly_work_income(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#work-income-for-household-monthly'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getHouseholdMonthlyIncomeWork",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_household_sizes(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#household-size-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getHouseholdSize",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_household_structures(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#household-structure-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getHouseholdStructure",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_work_income(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#income-from-work-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getIncomeFromWork",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_industries(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#industry-of-population-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getIndustry",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_language_literacy(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#language-literacy-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getLanguageLiterate",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_marital_statuses(self, year, planning_area, gender=None):
        '''API Documentation: https://docs.onemap.sg/#marital-status-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getMaritalStatus",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'gender': gender,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_modes_of_transport_to_school(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#mode-of-transports-to-school-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getModeOfTransportSchool",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_modes_of_transport_to_work(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#mode-of-transports-to-work-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getModeOfTransportWork",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_occupations(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#occupation-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getOccupation",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_age_groups(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#age-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getPopulationAgeGroup",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_religious_groups(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#religion-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getReligion",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_spoken_languages(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#spoken-language-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getSpokenAtHome",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_tenancy(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#tenancy-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getTenancy",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_dwelling_types(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#dwelling-type-household-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getTypeOfDwellingHousehold",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_population_by_dwelling_types(self, year, planning_area):
        '''API Documentation: https://docs.onemap.sg/#dwelling-type-population-data'''
        self.check_expired_and_refresh_token()[0]

        try:
            return json.loads(requests.get(self.url_base + "/privateapi/popapi/getTypeOfDwellingPop",
                                           params={'year': year,
                                                   'planningArea': planning_area,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_route(self, start_coordinates, end_coordinates, route_type):
        '''API Documentation: https://docs.onemap.sg/#route'''
        self.check_expired_and_refresh_token()[0]

        try:
            start_coordinates = "{},{}".format(start_coordinates[0], start_coordinates[1])
            end_coordinates = "{},{}".format(end_coordinates[0], end_coordinates[1])

            return json.loads(requests.get(self.url_base + "/privateapi/routingsvc/route",
                                           params={'start': start_coordinates,
                                                   'end': end_coordinates,
                                                   'routeType': route_type,
                                                   'token': self.token}).text)
        except Exception as e:
            print(e)
            return

    def get_public_transport_route(self, start_coordinates, end_coordinates, date, time, mode, max_walk_distance=None, num_itineraries=1):
        '''API Documentation: https://docs.onemap.sg/#route'''
        self.check_expired_and_refresh_token()[0]

        try:
            start_coordinates = "{},{}".format(start_coordinates[0], start_coordinates[1])
            end_coordinates = "{},{}".format(end_coordinates[0], end_coordinates[1])

            return json.loads(requests.get(self.url_base + "/privateapi/routingsvc/route",
                                           params={'start': start_coordinates,
                                                   'end': end_coordinates,
                                                   'routeType': 'pt',
                                                   'date': date,
                                                   'time': time,
                                                   'mode': mode,
                                                   'maxWalkDistance': max_walk_distance,
                                                   'numItneraries': num_itineraries,
                                                   'token': self.token}).text)

        except Exception as e:
            print(e)
            return

    def generate_static_map(self, layer_chosen, location, zoom, width, height, polygons=None, lines=None, points=None, color=None, fill_color=None):
        '''
        API Documentation: https://docs.onemap.sg/#static-map

        Polygon Format
        --------------
        Array of Points:{Color Code} | Array of Points:{Color Code}
        Example: [[1.31955,103.84223],[1.31755,103.84223],[1.31755,103.82223],[1.31755,103.81223],[1.31955,103.84223]]:255,255,105

        Line Format
        -----------
        Array of Points:{Color Code}:{Line Thickness} | Array of Points:{Color Code}:{Line thickness}
        Example: [[1.31955,103.84223],[1.31801,103.83224]]:177,0,0:3

        Point Format
        ------------
        [Point, Color Code, Marker Symbol]|[Point, Color Code, Marker Symbol]
        Example: [1.31955,103.84223,"255,255,178","B"]|[1.31801,103.84224,"175,50,0","A"]
        '''
        try:
            if zoom < 11:
                zoom = 11
            if zoom > 19:
                zoom = 19

            if width < 128:
                width = 128
            if width > 512:
                width = 512

            if height < 128:
                height = 128
            if height > 512:
                height = 512

            if type(location) == tuple or type(location) == list:
                return requests.get(self.url_base + "/commonapi/staticmap/getStaticImage",
                                    params={'layerchosen': layer_chosen,
                                            'lat': location[0],
                                            'lng': location[1],
                                            'zoom': zoom,
                                            'width': width,
                                            'height': height,
                                            'polygons': polygons,
                                            'lines': lines,
                                            'points': points,
                                            'color': color,
                                            'fillColor': fill_color}).content
            else:
                return requests.get(self.url_base + "/commonapi/staticmap/getStaticImage",
                                    params={'layerchosen': layer_chosen,
                                            'postal': location,
                                            'zoom': zoom,
                                            'width': width,
                                            'height': height,
                                            'polygons': polygons,
                                            'lines': lines,
                                            'points': points,
                                            'color': color,
                                            'fillColor': fill_color}).content

        except Exception as e:
            print(e)
            return

if __name__ == "__main__":
    email = "EMAIL_HERE"
    password = "PASSWORD_HERE"

    Client = OneMapClient(email, password)
