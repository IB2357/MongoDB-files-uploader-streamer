# files uploader & streamer for MongoDB
I created this to test my streaming pipeline that stream files from MongoDB


before use:
- rename file `.env.example` to `.env` and add to it your connection configs
- run `pip install -r requirements.txt`
- you can edit `upload.py` and `stream.py` to add your configs

> [!warning]
> you have to configure replica set in MongoDB

---

## for uploading
```bash
python upload.py
```
a new folder `source/` will be created (if not exist)

Now add files to `source/` folder and watch them upload 

## for streaming
```bash
python stream.py
```