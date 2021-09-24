import os
from datetime import datetime
from pathlib import Path
from typing import Tuple


def parse_name(name: str) -> Tuple[datetime, str]:
    name = name[3:]
    ext = name[name.rindex('.'):]
    date = name[:8]
    date = datetime.strptime(date, '%Y%m%d')
    return date, ext


if __name__ == '__main__':
    # List files
    files = list(os.listdir('./'))
    files.sort()

    # Filter files that starts with GMT
    files = [f for f in files if f.startswith('GMT')]

    # Videos only
    vids = [f for f in files if f.endswith('mp4')]
    for v in vids:
        # Parse name
        date, ext = parse_name(v)
        date = date.strftime('%Y %m-%d')
        os.rename(v, date + ext)
        front = v[:28]
        related = [f for f in files if f not in vids and f.startswith(front)]
        for file in related:
            ext = file[file.index('.'):]
            Path(date).mkdir(parents=True, exist_ok=True)
            os.rename(file, date + '/' + date + ext)

    print(files)
