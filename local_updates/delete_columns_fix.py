from local_updates.local_update import LocalUpdateForAllProviders


class DeleteDetailsColumn(LocalUpdateForAllProviders):
    @property
    def column_name(self):
        return 'details'

    def should_delete_column(self,df):
        return True


class DeleteBrandColumn(LocalUpdateForAllProviders):
    @property
    def column_name(self):
        return 'brand'

    def should_delete_column(self,df):
        return True
