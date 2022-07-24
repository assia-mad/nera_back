# nera_back
nera is an e-commerce web app 
# la_base_de_données:
   1-installer et configurer POSTGRESQL
   2-quelques postgres commandes:
       psql -U user -W   // connecter avec "user"   //dans repertoire bin de postgres
       \c dbName; // connecter a la bd
       \dt  // show tables
       select * from tablename;
       delete from tableName where ... // supprimer une ligne a partir d'une table
       
# python et django 
   dans le repertoire de projet : 
   py manage.py makemigrations
   py manage.py migrate
   py manage.py runserver
   pour creer un admin de projet : py manage.py createsuperuser
   
# install all packages 
pip install -r requirements.txt 
