import subprocess
from subprocess import Popen
import os

import asyncio
from concurrent.futures import ThreadPoolExecutor
from time import time


def check(n):
    start = time()
    path_to_output_file = f'{n}-myoutput.txt'
    print(path_to_output_file)

    myoutput = open(path_to_output_file, 'w')

    p = Popen(["ls", "-lha"], stdout=myoutput, stderr=subprocess.PIPE, universal_newlines=True)

    end = time()
    with open("/proc/{pid}/stat".format(pid=os.getpid()), 'rb')as p:
        core = p.read().split()[-14]
    return n, end - start, f'coreNo = {core.decode(encoding="utf-8")}'


async def check_all():

    with ThreadPoolExecutor(max_workers=20) as requester:
        loop = asyncio.get_event_loop()

        task = [
            loop.run_in_executor(requester, check, num)
            for num in range(128)
        ]
        for done in await asyncio.gather(*task):
            print(done)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(check_all())
    loop.run_until_complete(future)

