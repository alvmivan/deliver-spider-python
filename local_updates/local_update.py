import pandas as pd

from data_unification.item_repository import get_all_dataframes_for_provider


# def _transform_data_frame(update, df):
#     df[update.column_name] = df[update.column_name].apply(update.transformation)
#     return df


def perform_update(update):
    all_providers = update.providers

    if isinstance(all_providers, str):
        all_providers = [all_providers]
    for provider in all_providers:
        iterator = get_all_dataframes_for_provider(provider)
        for df, file in iterator:
            # apply transformation (dont call the old method, do it iterating)
            # first ask if delete column
            if update.should_delete_column(df):
                # only if column exists
                if update.column_name in df.columns:
                    df = df.drop(columns=[update.column_name])
            else:
                # iterate over the rows
                for index, row in df.iterrows():
                    if update.should_delete_row(row):
                        df = df.drop(index)
                    else:
                        df.at[index, update.column_name] = update.transformation(row[update.column_name])

            df.to_csv(file, index=False)


class LocalUpdate:

    # provider and column_name
    @property
    def providers(self):
        raise NotImplementedError('Not implemented')

    @property
    def column_name(self):
        raise NotImplementedError('Not implemented')

    def transformation(self, item):
        return item

    def should_delete_column(self, df):
        return False

    def should_delete_row(self, item):
        return False


class LocalAction:
    # que sea como el update pero que solo ejecute una funcion con el item como parametro
    @property
    def provider(self):
        raise NotImplementedError('Not implemented')

    @property
    def column_name(self):
        raise NotImplementedError('Not implemented')

    def action(self, item):
        raise NotImplementedError('Not implemented')

    def perform_action(self):
        iterator = get_all_dataframes_for_provider(self.provider)
        for df, file in iterator:
            # will not modify the dataframe, only apply the action to the items
            df[self.column_name].apply(self.action)


class LocalValidation:
    # similar a los otros, va a hacer validaciones sobre los items
    # vamos a retornar una lista de los que fallaron
    # si validation retorna true/false, entonces añadir a la lista si es true el row en cuestion.
    # si en su lugar reetorna un string, agregar ese tstring a la liusta
    # si retorna True o None, no agregar a la lista de errors
    # si lanza una excepcion agregar en la lista "thorws exception , la row y el mensaje de la excepcion

    @property
    def providers(self):
        raise NotImplementedError('Not implemented')

    @property
    def column_name(self):
        raise NotImplementedError('Not implemented')

    def validation(self, item):
        raise NotImplementedError('Not implemented')

    def perform_validation(self):
        all_providers = self.providers
        # if all providers is a string, convert it to a list
        if isinstance(all_providers, str):
            all_providers = [all_providers]

        for provider in all_providers:
            iterator = get_all_dataframes_for_provider(provider)

            for df, file in iterator:
                for index, row in df.iterrows():
                    try:
                        result = self.validation(row[self.column_name])
                        if result in [None, "", True]:
                            yield "OK"
                            continue
                        # si el resultado es un string, agregarlo a la lista de errores
                        if isinstance(result, str):
                            yield {'row': row, 'error': result}
                        else:
                            yield {'row': row, 'error': 'Validation failed'}
                    except Exception as e:
                        yield {'row': row, 'error': e}


class LocalUpdateForAllProviders(LocalUpdate):
    @property
    def providers(self):
        return ['changomas', 'carrefour', 'coope', 'garbarino', 'fravega', 'gili', 'hipertehuelche']
