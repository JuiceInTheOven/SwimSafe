FROM osgeo/gdal:latest
EXPOSE 8081

RUN apt-get update -y
#install git
RUN apt-get install -y git 
#install python
RUN apt-get install -y python3 python3-pip python3-dev
#install dependent libraries
RUN apt-get install -y libgeos-dev libproj-dev 

#install python packages, and set entrypoint
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scraper.py .
COPY beach_datasets/ beach_datasets/
COPY sentinel2loader_lib.py .

ENTRYPOINT [ "python", "scraper.py"]