from pytube import YouTube

link = input('Link: ')
video = YouTube(link)
quality = input('Quality (High/Low): ')

if quality == 'High':
    output = video.streams.get_highest_resolution()
if quality == 'Low':
    output = video.streams.get_lowest_resolution()

output.download()  