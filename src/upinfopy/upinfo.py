# Copyright 2024 frieda
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
import json
import urllib.parse
import base64

import requests

class UpInfo:
    pcid = ""

    def __init__(self):
        self.sid = ""
        self.cid = ""
        self.bcid = ""
        self.uname = ""
        self.mid = ""
        self.getnumber = 1000
        self.getstart = 0
        self.pars = []
        self.cols = ["all"]
        self.order = "idpk"
        self.desc = 0
        self.server = "ali"
        self.v = 24
        self.cache = ""
        self.midpk = 0
        self.api = ""
        

    def to_url_encode(self):
        params = []
        params.append(f"sid={urllib.parse.quote(self.sid)}")
        
        if self.uname:
            params.append(f"uname={urllib.parse.quote(self.uname)}")
        
        if self.cid:
            if self.cid == "cidmy":
                self.cid = "d4856531-e9d3-20f3-4c22-fe3c65fb009c"
            elif self.cid == "cidvps":
                self.cid = "28401227-bd00-a20f-c561-ddf0def881d9"
            elif self.cid == "cidguest":
                self.cid = ""
            if self.cid:
                params.append(f"cid={urllib.parse.quote(self.cid)}")

        if self.bcid:
            if self.bcid == "cidguest":
                self.bcid = "GUEST000-8888-8888-8888-GUEST00GUEST"
            elif self.bcid == "cidmy":
                self.bcid = ""
            elif self.bcid == "cidvps":
                self.bcid = "28401227-bd00-a20f-c561-ddf0def881d9"
            if self.bcid:
                params.append(f"bcid={urllib.parse.quote(self.bcid)}")

        if self.cache:
            params.append(f"cache={self.cache}")
        if self.mid:
            params.append(f"mid={urllib.parse.quote(self.mid)}")
        #if Upinfo.pcid:
            #params.append(f"pcid={Upinfo.pcid}")
        
        order_str = f"{self.order} desc" if self.desc == 1 else self.order
        if order_str != "idpk":
            params.append(f"order={urllib.parse.quote(order_str)}")
        
        if self.getnumber != 15:
            params.append(f"getnumber={self.getnumber}")
        if self.getstart != 0:
            params.append(f"getstart={self.getstart}")
        if self.midpk != 0:
            params.append(f"midpk={self.midpk}")

        if self.pars:
            if self.v == 22:
                tmp = ",~".join(self.pars)
                tmp = base64.b64encode(tmp.encode()).decode()
                tmp = tmp.replace('+', '*').replace('/', '-').replace('=', '.')
            else:
                tmp = json.dumps(self.pars)
            params.append(f"pars={urllib.parse.quote(tmp)}")
        
        if self.cols != ["all"]:
            params.append(f"cols={urllib.parse.quote(json.dumps(self.cols))}")

        return "&".join(params)

    def set_par(self, *args):
        self.pars.extend(args)
        return
    
    async def send_back(self, endpoint, backtype="json"):
        if(self.api==""):
            #print("api not set")
            return
        url = f"{self.api}/{endpoint}"
        params = self.to_url_encode()
        back = None
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查响应状态码
            res= response.json()  # 返回JSON格式的数据
            if(res["res"]!=0):
                print(f"{url} 请求失败 : {res['errmsg']}")
                return res    
                  
            if(res["kind"]=="json"):
                try:
                    back = json.loads(res["back"])
                except json.JSONDecodeError as json_err:
                    #return {"error": f"JSON decode error: {json_err}"}
                    back=res["back"]
           
            else:
                back=res["back"]
            return back
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except Exception as err:
            return {"error": f"An error occurred: {err}"} 

    @staticmethod
    def getGuest():
        up2 = UpInfo()
        up2.sid = 'GUEST888-8888-8888-8888-GUEST88GUEST'
        up2.cid = 'GUEST000-8888-8888-8888-GUEST00GUEST'
        up2.bcid = 'd4856531-e9d3-20f3-4c22-fe3c65fb009c'        
        up2.uname = 'guest'
        up2.pars = []            
        up2.api="http://api.778878.net"
        return up2
    
    @staticmethod
    def setMaster(up):
        UpInfo._masterInstance = up

    @staticmethod
    def getMaster():
      if UpInfo._masterInstance is None:
        return None
      else:
        UpInfo._masterInstance.pars = []
        return UpInfo._masterInstance
    
    def clone(self):
        clonedUpInfo = UpInfo()
        clonedUpInfo.sid = self.sid
        clonedUpInfo.uname = self.uname
        clonedUpInfo.bcid = self.bcid
        return clonedUpInfo

if __name__ == "__main__":
    # Create an instance of UpInfo
    up = UpInfo()
    
    # Set master instance
    up.sid = "some-sid"  # initial sid
    up.uname = "guest"
    UpInfo.setMaster(up)
    
    # Get master instance and modify its attributes
    up = UpInfo.getMaster()
    if up is not None:
        up.sid = "f41917268"
        up.getnumber = 500  # Set custom attribute for debugging (if necessary)
        up.api="http://192.168.31.181:30005"
        
        # Call the asynchronous method
        async def main():
            dtTrade = await up.send_back("apistock/stock/stock_mine/get", up)
            print(dtTrade)

        asyncio.run(main())  # Run the async method
        
