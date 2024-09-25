from local_updates.local_update import LocalUpdate


class ChangomasUrlFix(LocalUpdate):
    @property
    def providers(self):
        return 'changomas'

    @property
    def column_name(self):
        return 'url'

    def transformation(self, item):
        prefix = 'https://www.changomas.com.ar'
        if not item.startswith(prefix):
            print(f'Fixing URL: {item} to {prefix + item}')
            return prefix + item
        return item


