file_location = "data_frames/fail_searches.txt"

# create a set with the lines of the file
with open(file_location, "w+") as file:
    failed_searches = set(file.readlines())


def is_fail_searches(fail_search):
    return fail_search in failed_searches

def add_fail_search(fail_search):
    with open(file_location, "w+") as file:
        failed_searches.add(fail_search)
        file.write("\n".join(failed_searches))
