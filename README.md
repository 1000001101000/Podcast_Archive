# Podcast_Archive

A quick way to maintain a local copy of your podcasts in case they disapear from the internet someday. 

This was designed to be run via a cron job periodically and will only download episodes that have not been previously downloaded. It can also be run manually as desired. It was developed on Debian Linux but should work on any OS with Python3 installed.

To Setup:
- Download PyPodcastArchive.py
- Create a text file with the URLs of the podcasts you would like to archive (see feed_urls.txt for an example)
- Install the podcast parser using pip
`pip3 install podcastparser`
- Edit PyPodcastArchive.py, set feed_list to the path of your URL text file, set base_directory to the path you would like the podcasts downloaded to. (I'll move these to a config file in a future version) 
- run PyPodcastArchive.py using Python3
