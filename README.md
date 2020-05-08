# Proper Plex Shuffle

Plex has an [well-documented](https://www.reddit.com/r/PleX/comments/5ic0fh/it_has_been_years_can_plex_please_fix_their/db7wdm1/) issue where when shuffling media, it seems to play repeated content. According to Plex's CTO, because of the [Birthday problem](https://en.wikipedia.org/wiki/Birthday_problem), truly random playlists don't actually "feel" random.

A solution to this problem is to create smart playlists that only show content that hasn't been viewed recently. This Python script automatically creates playlists of not-recently-watched TV episodes.

Before using it, make sure you update `plex_config_sample.ini` with the proper information about your Plex account, server, library, and TV show names and save as `plex_config.ini`.