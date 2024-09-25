from local_updates.local_update import LocalUpdate


class FixGarbarinoURLS(LocalUpdate):

    @property
    def providers(self):
        return 'garbarino'

    @property
    def column_name(self):
        return 'url'

    def transformation(self, item):
        prefix = 'https://www.garbarino.com'
        # espero : /p/parlante-bluetooth-smartlife-portatil-ipx5-55w-tws-rgb-rosa/1619a2f6-7bfb-45b9-965b-0e5fe65442bd
        # espero : https://www.garbarino.com/p/parlante-bluetooth-smartlife-portatil-ipx5-55w-tws-rgb-rosa/1619a2f6-7bfb-45b9-965b-0e5fe65442bd

        if not item.startswith(prefix):
            print(f'Fixing URL: {item} to {prefix + item}')
            return prefix + item
        return item