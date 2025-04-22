
import random,time,binascii,os,uuid
with open("devices.txt", "r", encoding="utf-8") as f:
    devices = f.read().splitlines()
def dr():
    while 1:
        try:
            iid      = int(bin(int(time.time()) + random.randint(0, 100))[2:] + "10100110110100110000011100000101", 2)
            did      = int(bin(int(time.time()) + random.randint(0, 100))[2:] + "00101101010100010100011000000110", 2)
        
            openudid = str(binascii.hexlify(os.urandom(8)).decode())
            _rticket = int(time.time() * 1000)
            ts=str(int(time.time() * 1000))[:10]
            ts1=int(round(time.time() * 1000)) - random.randint(13999, 15555)
            uid=str(uuid.uuid4())
            v3=random.randint(1, 8)
            v2=random.randint(1, 8)
            v1=random.randint(7, 39)
            os_version = f"{v1}.{v2}.{v3}"
            return iid,did,openudid,_rticket,ts,ts1,uid,os_version
        except:continue
def device_id():
    device = random.choice(devices).split(':')
    _rticket = int(time.time() * 1000)
    ts=str(int(time.time() * 1000))[:10]
    ts1=int(round(time.time() * 1000)) - random.randint(13999, 15555)
    v3=random.randint(1, 8)
    v2=random.randint(1, 8)
    v1=random.randint(35, 37)
    os_version = f"{v1}.{v2}.{v3}"
    version = f"{v1}0{v2}0{v3}"
    return {
                'iid': device[0],
                'did': device[1],
                'device_type': device[2],
                'device_brand': device[3],
                'cdid': device[5],
                'openudid': device[4],
                'ts':ts,
                'ts1':ts1,
                '_rticket':_rticket,
                'version':version,
                'os_version':os_version,
                'user-agent': f'com.zhiliaoapp.musically/{version} (Linux; U; Android {os_version}; en_us; {device[2]}; Build/RP1A.200720.012;tt-ok/3.12.13.4-tiktok)',
            }
