
from wsgiref.handlers import format_date_time
import asyncio
from time import mktime
import hashlib
import hmac,time
from urllib.parse import urlencode, urlparse
import uuid
from WebsocketTest.common.utils import *
from WebsocketTest.common.WSBaseApi import WSBaseApi
from pathlib import Path

class ApiTestRunner(WSBaseApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_path = Path.cwd().resolve().joinpath("data/audio",f"{self.text}.pcm")
    def generate_v2_auth_headers(self):
        """为v2 5.4链路生成授权头"""
        url_host = urlparse(self.url).netloc
        date = format_date_time(mktime(datetime.now().timetuple()))
        authorization_headers = f"host: {url_host}\ndate: {date}\nGET /v2/autoCar HTTP/1.1"
        signature_sha = hmac.new(self.apiSecret.encode('utf-8'), authorization_headers.encode('utf-8'),
                                digestmod=hashlib.sha256).digest()
        authorization_signature = encode_base64(signature_sha,input_encoding='bytes')
        authorization = f'api_key="{self.apiKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{authorization_signature}"'
        return {
                "host": url_host,
                "date": date,
                "authorization": encode_base64(authorization),
                "appid": self.appId
            }
    def generate_v1_auth_headers(self):
        
        """为5.0链路生成参数"""
        param_iat = self.build_params()
        cur_time = int(time.time())
        param = json.dumps(param_iat, ensure_ascii=False)
        param_base64 = encode_base64(param)
        check_sum_pre = self.apiKey + str(cur_time) + param_base64
        checksum = hashlib.md5(check_sum_pre.encode("utf-8")).hexdigest()
        return {
                "appid": self.appId,
                "checksum": checksum,
                "param": param_base64,
                "curtime": str(cur_time),
                "signtype": "md5"
            }
    def assemble_ws_auth_url(self,  chain=None):
        if chain:
            # v2 5.4链路
            params = self.generate_v2_auth_headers()
        else:
            # 默认5.0链路
            params = self.generate_v1_auth_headers()

        return f"{self.url}?{urlencode(params)}"
    # @exception_decorator
    async def handle_v2_chain(self, ws):
        """
        处理v2 5.4链路逻辑：
        - 接收消息并解析
        - 检查返回码是否为0（成功）
        - 如果状态为1，则解码并返回特定的文本内容
        - 如果状态为2，则结束循环
        """
        while True:
            try:
                msg = await ws.recv()
                # print(msg)
                response_data = json.loads(msg)
                # code 返回码，0表示成功，其它表示异常
                if response_data["header"]["code"] == 0:
                    # status 整个结果的状态，0-会话起始结果，1-中间结果，2-最终结果
                    if "status" in response_data["header"]:
                        status = response_data["header"]["status"]
                        if status == 1 and "cbm_semantic" in response_data["payload"]:
                            semantic_bs64 = response_data["payload"]["cbm_semantic"]["text"]
                            semantic_str = base64.b64decode(semantic_bs64.encode('utf-8')).decode('utf-8')
                            self.response = json.loads(semantic_str)
                            return
                        elif status == 2:
                            break
                else:
                    logger.error(f"返回结果错误：{response_data['header']['message']}")
                    break
            except Exception as e:
                logger.error(f"Error in processing message: {e}")
                break
    # @exception_decorator
    async def handle_v1_chain(self, ws):
        """
        处理5.0链路逻辑：
        - 根据接收到的消息执行不同的操作
        - 当'action'为'started'时，读取文件并发送数据块
        - 发送结束标识
        - 当'action'为'result'且'sub'为'stream_tpp'时，返回内容
        """

        while True:
            _msg = await ws.recv()
            # print(_msg)
            try:
                msg = json.loads(_msg)
                if msg['action'] == "started":
                    with open(self.text_path, 'rb') as file:
                        for chunk in iter(lambda: file.read(1280), b''):
                            await ws.send(chunk)
                            await asyncio.sleep(0.04)  # 使用asyncio.sleep避免阻塞事件循环
                    await ws.send("--end--".encode("utf-8"))
                elif msg['action'] == "result":
                    data = msg['data']
                    if data.get('sub') == "stream_tpp" or data.get('sub') == "tpp":
                        self.response = json.loads(data['content'])
                        return
            except Exception as e:
                logger.error(f"error in handle_v1_chain :{e}")
                break
   
    def build_params(self,chain=None):
        if chain:  #5.4链路参数
            _textParams = {
                "sparkEnv": self.sparkEnv,
                "userId": self.userId,
                "user_data": "", 
                "attachparams": str({"nlp_params": {"vWtoken": self.token, "aiui45_intv_mode": 2, "aqua_route": "vwa"}}), # 不能传递字典，需要传str
                "scene": self.scene,
                "debugx": "true",
                "debug": "true"
            }
            # # 序列化 textParams
            textParams = json.dumps(_textParams, ensure_ascii=False)
            def get_audio():
                with open(self.text_path, "rb") as file:
                    content = file.read()
                    return encode_base64(content,input_encoding='bytes')
        

            return {
                    "header": {
                        "app_id": self.appId,
                        "uid": "efeafe5e-82d6-4922-9770-f7aaabf97548",
                        "stmid": "sid1111",
                        "status": 3,
                        "scene": self.scene
                    },
                    "parameter": {
                        "nlp": {
                            "sub_scene": "cbm_v47",
                            "new_session": False,
                            "nlp": {
                                "encoding": "utf8",
                                "compress": "raw",
                                "format": "json"
                            }
                        }
                    },
                    "payload": {
                        "cbm_semantic": {
                            "compress": "raw",
                            "format": "plain",
                            "text": encode_base64(textParams),
                            "encoding": "utf8",
                            "status": 3
                        },
                        "audio": {
                            "audio": get_audio(),
                            "status": 2,
                            "encoding": "raw",
                            "sample_rate": 16000,
                            "channels": 1,
                            "bit_depth": 16,
                            "frame_size": 0
                        }
                    }
                }
        else: #5.0链路参数
            def get_auth_id():
                """
                生成基于系统MAC地址的唯一身份验证ID。
                
                返回:
                    str: 唯一的身份验证ID。
                """
                # 获取系统MAC地址的整数表示，并转换为12位的十六进制字符串
                mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
                
                # 将MAC地址按照标准格式（使用冒号分隔）重新组合
                formatted_mac = ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
                
                # 对格式化后的MAC地址进行MD5哈希处理，并返回其十六进制表示
                auth_id = hashlib.md5(formatted_mac.encode("utf-8")).hexdigest()
                return auth_id
            trs_params = {}
            iat_params = {
                        "accent": "mandarin",
                        "language": self.language,
                        "domain": "aiui-automotiveknife",
                        "eos": "600",
                        "evl": "0",
                        "isFar": "0",
                        "svl": "50",
                        "vgap": "400"
                    }
            
            nlp_params = {
                        "devid": "LG8-LGA26.08.2420010196",
                        "city": "合肥市",
                        "user_defined_params": {},
                        "weather_airquality": "true",
                        "deviceId": "LG8-LGA26.08.2420010196",
                        "userId": "69b85a13-1434-408b-872f-1632c587dbc4",
                        "asp_did": "LG8-LGA26.08.2420010196",
                        "vWtoken": self.token,
                        "car_identity": "MP24",
                        "theme": "standard",
                        "vin": "HVWJA1ER5R1203864",
                        "interactive_mode": "fullDuplex",
                        "did": "VW_HU_ICAS3_LG8-LGA26.08.2420010196_v2.0.1_v0.0.1"
                    }
            attach_params = {
                            "trs_params": json.dumps(trs_params, ensure_ascii=False),
                            "iat_params": json.dumps(iat_params, ensure_ascii=False),
                            "nlp_params": json.dumps(nlp_params, ensure_ascii=False)
                        }
            return {
                    "auth_id": get_auth_id(),
                    "ver_type": "websocket",
                    "data_type": "audio",
                    "scene": "main",
                    "lat": "31.704187",
                    "lng": "117.239833",
                    "attach_params": json.dumps(attach_params, ensure_ascii=False),
                    "userparams": "eyJjbGVhbl9oaXN0b3J5Ijoib2ZmIiwic2tpcCI6Im5vdF9za2lwIn0=",
                    "interact_mode": "continuous",
                    "text_query": "tpp",
                    "sample_rate": "16000",
                    "aue": "raw",
                    "speex_size": "60",
                    "dwa": "wpgs",
                    "result_level": "complete",
                    "debugx": "True",
                    "debug": "true",
                    "close_delay": "100"
                }
    
    @exception_decorator
    def run(self):
        extra_headers = {'Authorization': self.token}
        # 使用split函数分割URL，并找到包含"v2"的部分
        parts = self.url.split('/')
        # "v2"正好位于倒数第二个位置, v2走5.4链路,v1走5.0链路
        version = "v2" if len(parts) > 2 and parts[-2] == 'v2' else None
        # 根据版本选择正确的assemble_ws_auth_url方法参数
        self.url = self.assemble_ws_auth_url(version)
        # 构建frame，对于v2版本添加额外参数
        if version:
            self.request = self.build_params(version)
        # WebSocket连接与消息发送
        asyncio.run(self.WebSocketApi(
            extra_headers,
            version
        ))


