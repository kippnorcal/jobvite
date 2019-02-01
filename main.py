import jobvite
import os

jobvite_key = os.getenv("JOBVITE_API_KEY")
jobvite_secret= os.getenv("JOBVITE_API_SECRET")

api = jobvite.JobviteAPI(jobvite_key, jobvite_secret)

candidates = api.candidates()

print(candidates)
