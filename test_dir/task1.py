import concurrent.futures
import time
import timeit
from collections import defaultdict


def find_in_file(args):
    result = defaultdict(list)

    for (file_name, words) in args:
        with open(file_name) as file:
            content = file.read()

            for word in words:
                if word in content:
                    result[word].append(file_name)

    return result

def chunks(files, max_workers):
    per_chunk = len(files) // max_workers

    for i in range(0, len(files), per_chunk):
        yield files[i:i + per_chunk]

def main(files: list, words: list, max_workers = 2):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        result = defaultdict(list)

        args = list(chunks([(file_name, words) for file_name in files], max_workers))

        for thread_result in list(executor.map(find_in_file, args)):
            for word, file_names in thread_result.items():
                result[word].extend(file_names)

        return result


if __name__ == "__main__":
    files = [
        'league_lore_story_1.txt',
        'league_lore_story_2.txt',
        'league_lore_story_3.txt',
        'league_lore_story_4.txt',
        'league_lore_story_5.txt',
    ]

    start = time.perf_counter()
    for _ in range(10):  # Run the function 10 times
        print(timeit.timeit(lambda: main(files, ['Demacia', 'Malzahar', 'kingdom', 'was']), number=1))
    end = time.perf_counter()

    print(f"Average time per run: {(end - start) / 10} seconds")
