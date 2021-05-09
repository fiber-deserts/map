import subprocess

for i in range(1, 57):
    filename = f"tabblock2010_{i:02d}_pophu.zip"
    subprocess.run("wget https://www2.census.gov/geo/tiger/TIGER2010BLKPOPHU/" + filename, shell=True)
    subprocess.run("unzip " + filename, shell=True)
