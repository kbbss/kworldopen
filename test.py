
from src.osul.klsworld.person import fromLabelname as person_fromLabelname
from src.osul.klsworld.targetshape import find as targetshape_find

person = person_fromLabelname("iu")
print("person",person)

targetshape = targetshape_find( "Linaqruf/anything-v3.0" , {"id":str(person["_id"]) ,"name":"person" }   )

print("targetshape",targetshape)

#63f6ec9518983076fd4ecc29

from src.osul.dataac.image import imageShow

imageShow("63f6ec9518983076fd4ecc29")