import pafy

from urllib import parse, request
import re

class music:

    def __init__(self, search):
        self.url = self.Search(search)

    def Search(self, search):
        query_string = parse.urlencode({'search_query': search})
        html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall('\"url\":\"/watch\\?v=(.{11})', html_content.read().decode())
        return 'https://www.youtube.com/watch?v=' + search_results[0]

    def Descargar(self):
        video = pafy.new(self.url)
        audio = video.audiostreams
        audio = self.Order(audio)
        name  = audio[0].generate_filename()
        name  = "./music/"+name.replace(".webm", ".mp4")
        audio[0].download(filepath= name)
        return name

    def Order(self,arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j].get_filesize() > arr[j+1].get_filesize() :
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    
if __name__ == "__main__":
    test = music()
    test.Descargar()
