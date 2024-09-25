from local_updates.changomas_fix import ChangomasUrlFix
from local_updates.delete_columns_fix import DeleteDetailsColumn, DeleteBrandColumn
from local_updates.fix_garbarino_urls import FixGarbarinoURLS
from local_updates.local_update import LocalUpdate, perform_update

_all_updates: list[LocalUpdate] = [
    ChangomasUrlFix(),
    DeleteDetailsColumn(),
    DeleteBrandColumn(),
    FixGarbarinoURLS()
]


def run_local_updates_now():
    for update in _all_updates:
        # print update type
        print(f'Running update: {update.__class__.__name__}')
        perform_update(update)


if __name__ == '__main__':
    run_local_updates_now()
