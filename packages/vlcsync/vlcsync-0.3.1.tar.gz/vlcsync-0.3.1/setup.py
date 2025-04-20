# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vlcsync']

package_data = \
{'': ['*']}

install_requires = \
['cached-property', 'click>=8.1.3,<9.0.0', 'loguru', 'psutil']

entry_points = \
{'console_scripts': ['vlcsync = vlcsync.main:main']}

setup_kwargs = {
    'name': 'vlcsync',
    'version': '0.3.1',
    'description': 'Utility for synchronize multiple instances of VLC. Supports seek, play and pause. ',
    'long_description': 'VLC Sync\n========\n\nUtility for synchronize multiple instances of VLC. Supports seek, play and pause/stop, playlist and volume sync. \n  \n\n#### Motivation\n\nStrongly inspired by F1 streams with extra driver tracking data streams. Did [not find](#alternatives) reasonable alternative for Linux for playing several videos synchronously. So decided to write my own solution.\n\n## Install\n\n```shell\npip3 install -U vlcsync\n```\n\nor \n\n- Download [binary release](https://github.com/mrkeuz/vlcsync/releases) for Windows 7/10  \n  NOTE: On some systems there are false positive Antivirus warnings [issues](https://github.com/mrkeuz/vlcsync/issues/1).\n  In this case use [alternative way](./docs/install.md#windows-detailed-instructions) to install.   \n\n## Run\n\n`Vlc` players should open with `--rc-host 127.0.0.42` option OR configured properly from gui (see [how configure vlc](./docs/vlc_setup.md)) \n\n```shell\n\n# Run vlc players \n$ vlc --rc-host 127.0.0.42 SomeMedia1.mkv &\n$ vlc --rc-host 127.0.0.42 SomeMedia2.mkv &\n$ vlc --rc-host 127.0.0.42 SomeMedia3.mkv &\n\n# vlcsync will monitor and syncing all players\n$ vlcsync\n\n# Started from version 0.2.0\n\n# For control remote vlc instances, \n# remote port should be open and rc interface listen on 0.0.0.0\n$ vlcsync --rc-host 192.168.1.100:12345 --rc-host 192.168.1.50:54321\n\n# For disable local discovery (only remote instances)\n$ vlcsync --no-local-discovery --rc-host 192.168.1.100:12345\n\n# Started from version 0.3.0 (playlists sync)\n# Support volume sync for exotic cases\n$ vlcsync --volume-sync\n\n# For help and see all options\n$ vlcsync --help\n```\n\n## Awesome \n\nAwesome [use-case](./docs/awesome.md) ideas\n\n## Demo\n\n![vlcsync](./docs/vlcsync.gif)\n\n## Limitations \n\n- Frame-to-frame sync NOT provided. `vlc` does not have precise controlling via `rc` interface out of box. \n  Difference between videos can be **up to ~0.5 seconds** in worst case. Especially when playing from network share, \n  due buffering time and network latency.\n\n- Currently, tested on:\n  - Linux (Ubuntu 20.04)\n  - Windows 7 (32-bit)\n  - Windows 10 (64-bit)\n\n## Alternatives\n\n- [vlc](https://www.videolan.org/vlc/index.ru.html) \n    - There is a [netsync](https://wiki.videolan.org/Documentation:Modules/netsync/) but seem only master-slave (tried, but not working by some reason)\n    - Open additional media. Seems feature broken in vlc 3 (also afaik limited only 2 streams)  \n- [Syncplay](https://github.com/Syncplay/syncplay) - very promised, but little [complicated](https://github.com/Syncplay/syncplay/discussions/463) for sync different videos\n- [bino](https://bino3d.org/) - working, very strange controls, file dialog not working and only fullscreen\n- [gridplayer](https://github.com/vzhd1701/gridplayer) - low fps by some reason\n- [mpv](https://github.com/mpv-player/mpv) - with [mixing multiple videos](https://superuser.com/a/1325668/1272472) in one window. Unfortunately does not support multiple screens\n- [AVPlayer](http://www.awesomevideoplayer.com/) - only Win, macOS, up to 4 videos in free version\n\n## Contributing\n\nAny thoughts, ideas and contributions welcome!\n\nA special thanks to **KorDen32** for inspiration! <img src="./docs/F1.svg" alt="F1" width="45"/>\n\nEnjoy!\n',
    'author': 'mrkeuz',
    'author_email': 'mrkeuz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrkeuz/vlcsync/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
