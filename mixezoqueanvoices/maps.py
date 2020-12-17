from clld.web.maps import Map


class LanguagesMap(Map):
    def get_options(self):
        return {
            'max_zoom': 13,
            'base_layer': 'Esri.DeLorme',
            'show_labels': True,
            'resize_direction': 's',
        }


def includeme(config):
    config.register_map('languages', LanguagesMap)
