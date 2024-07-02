from integration_utils.bitrix_robots.models import BaseRobot

from robot_weather.utils import get_coordinates_by_address, get_weather_by_coordinates, format_weather_data


class WeatherRobot(BaseRobot):
    CODE = 'robot_weather'
    NAME = 'Робот возвращает текущую погоду для конкретного адреса'
    USE_SUBSCRIPTION = True

    PROPERTIES = {
        'address': {
            'Name': {'ru': 'Адрес'},
            'Type': 'string',
            'Required': 'Y',
        },
    }

    RETURN_PROPERTIES = {
        'weather': {
            'Name': {'ru': 'Погода'},
            'Type': 'string',
            'Required': 'Y',
        },
        'ok': {
            'Name': {'ru': 'ok'},
            'Type': 'bool',
            'Required': 'Y',
        },
        'error': {
            'Name': {'ru': 'error'},
            'Type': 'string',
            'Required': 'N',
        },
    }

    def process(self) -> dict:
        try:
            coords = get_coordinates_by_address(self.props['address'])
            weather_data = get_weather_by_coordinates(*coords)
            weather_speach = format_weather_data(weather_data)

            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {"weather": weather_speach
                                                                                        }})
        except KeyError:
            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                     "return_values": {"weather": "error"
                                                                                       }})

        except Exception as exc:
            return dict(ok=False, error=str(exc))

        return dict(ok=True)
