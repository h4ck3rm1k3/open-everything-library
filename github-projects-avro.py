import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

schema = avro.schema.parse(open("avro-schemas/git-hub-projects.avsc", "rb").read())

fn = "data/github-projects.avro"

writer = DataFileWriter(open(fn, "wb"), DatumWriter(), schema)
writer.append({
    "name": "Alyssa",
    "id" : 1234,
    "fork": False,
    "description" : "Test",
    "full_name" :  "goo/fsd",
    "owner_name" :  "larry",
     "html_url" : "http://fsdfs/fdsfsd"
})
#writer.append({"name": "Ben"})
writer.close()

reader = DataFileReader(open(fn, "rb"), DatumReader())
for user in reader:
    print user
reader.close()
      
