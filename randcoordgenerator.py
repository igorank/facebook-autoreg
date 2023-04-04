import random
from shapely.geometry import Polygon, Point


class RandCoordGenerator:

    poly_ua = Polygon([(52.275507, 32.443671), (48.522214, 22.205110), (44.421358, 33.765272),
                    (48.878650, 40.030574)])  # кординаты полигона украины для генерации случ. кординат
    poly_sk = Polygon([(49.606614, 19.452105), (48.380048, 16.869988), (48.255727, 19.616170),
                    (49.036343, 22.481944)])  # кординаты полигона словакии для генерации случ. кординат
    poly_ru = Polygon([(72.324441, 102.477270), (55.654271, 36.940490), (55.529312, 70.488956),
                       (66.553490, 142.581341)])  # кординаты полигона РФ для генерации случ. кординат
    poly_gb = Polygon([(58.411640, -4.489035), (54.068595, -4.772156), (50.656964, -1.298120),
                       (54.023550, -0.532987)])  # кординаты полигона РФ для генерации случ. кординат
    poly_pl = Polygon([(54.162823, 18.641813), (52.314580, 14.955570), (50.738637, 20.165929),
                       (52.234060, 23.086302)])  # кординаты полигона Польши для генерации случ. кординат
    poly_kz = Polygon([(50.356174, 67.444436), (46.799618, 53.353441), (45.830379, 66.968906),
                       (48.100550, 79.266370)])  # кординаты полигона Казах. для генерации случ. кординат
    poly_ee = Polygon([(59.213721, 25.756249), (58.801666, 24.536126), (58.124098, 26.077515),
                       (58.701387, 27.296611)])  # кординаты полигона Казах. для генерации случ. кординат

    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(RandCoordGenerator, cls).__new__(cls)
    #     return cls.instance

    def polygon_random_points(self, country, num_points=1):
        geo_dict = {
          "UA": RandCoordGenerator.poly_ua,
          "SK": RandCoordGenerator.poly_sk,
          "RU": RandCoordGenerator.poly_ru,
          "GB": RandCoordGenerator.poly_gb,
          "PL": RandCoordGenerator.poly_pl,
          "KZ": RandCoordGenerator.poly_kz,
          "EE": RandCoordGenerator.poly_ee
        }

        min_x, min_y, max_x, max_y = geo_dict[country].bounds
        points = []
        while len(points) < num_points:
            random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
            if random_point.within(geo_dict[country]):
                points.append(random_point)
        return points

    def get_n_e_rand_points(self, points):
        rand_gps_poiunts = points
        cord_n = format(rand_gps_poiunts[0].x, '.4f')
        cord_e = format(rand_gps_poiunts[0].y, '.3f')
        return cord_n, cord_e

    def get_rand_coord(self, country):
        points = self.polygon_random_points(country)
        n_cord, e_cord = self.get_n_e_rand_points(points)
        return n_cord, e_cord
