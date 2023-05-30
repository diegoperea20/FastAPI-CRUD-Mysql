from sqlalchemy import create_engine, MetaData



engine = create_engine("mysql+pymysql://root:mypassword@localhost:3306/storedb")
meta=MetaData()
conn = engine.connect()



#docker run --name mymysql -e MYSQL_ROOT_PASSWORD=mypassword -p 3306:3306 -d mysql:latest
#docker exec -it mymysql bash
#mysql -u root -p
#create database storedb;