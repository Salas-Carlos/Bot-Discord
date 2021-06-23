import json
import discord
import datetime

class Meet:

    def __init__(self, body= "default"):
        self.body = self.convertBody(body)

    def save(self):
        f = open("./Jobs/jobs.txt", 'a+')
        f.write(self.body)
        
    def convertBody(self, body):
        body = '{"titule":'+ "\""+body[0]+"\""+ ', "descripcion":'+"\""+body[1]+"\""+ ', "date":'+"\""+body[2]+"\""+', "members":'+"\""+body[3]+"\""+ ',"new": "1"}\n'
        return body

    def addJobs(self,scheduler,bot):
        with open('./Jobs/jobs.txt') as f:
            jobs = [json.loads(job) for job in f]
        new_jobs= 0
        if (len(jobs)!=0):
            for i in range(len(jobs)):
                if(jobs[i]["new"]=="1"):
                    scheduler.add_job(lambda: self.Embed(jobs[i],bot), 'date', run_date = datetime.datetime.strptime(jobs[i]["date"], '%Y-%m-%d %H:%M'))
                    jobs[i]["new"]="0"
                    new_jobs+=1
            
        
            if(new_jobs!=0):
                cont = ""
                for job in jobs:
                    body = str(job).replace("'", "\"")
                    cont+=(body+"\n")
                f = open("./Jobs/jobs.txt", 'w')
                f.write(cont)
                f.close()
        #jobs= json.loads(jobs)
        
        return "nice"

    def Embed(self, Json, bot):
        embed = discord.Embed(title=Json["titule"], description=Json["descripcion"], color=discord.Color.blue())
        embed.add_field(name="Fecha de reunion", value=Json["date"])
        embed.add_field(name="Miembros", value=Json["members"])
        channel1 = bot.get_guild(850926065782358028).get_channel(850926066553585685)
        bot.loop.create_task(channel1.send(embed=embed))
    